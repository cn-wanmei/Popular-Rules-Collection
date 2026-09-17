#!/usr/bin/env python3
"""Execute Batch 01 semantic false-positive and cross-service overlap audits."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
# Running ``python scripts/<tool>.py`` puts ``scripts/`` (not the repository
# root) on sys.path. Make the repository-local ``src`` package importable in
# both CI and direct developer execution without relying on PYTHONPATH.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.engine.audit.matcher import matching_rules
from src.engine.ingest.rule_parser import iter_rules
from src.engine.ingest.normalizer import normalize_record

SEMANTIC = ROOT / "config/p0_batch01_semantic_audit.yaml"
OVERLAP = ROOT / "config/p0_batch01_overlap_audit.yaml"


def load_snapshot_rules(path: Path, service: str) -> list[dict[str, Any]]:
    records = []
    for typ, value in iter_rules(path):
        records.append(normalize_record(service, typ, value))
    if not records:
        raise ValueError(f"snapshot produced no canonical rules: {path}")
    return records


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_semantic(doc: dict[str, Any]) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    results: dict[str, list[dict[str, Any]]] = {}
    service_rules: dict[str, list[dict[str, Any]]] = {}
    any_blocked = False
    for service, spec in (doc.get("services") or {}).items():
        snapshot = ROOT / spec["snapshot"]
        if not snapshot.exists():
            raise FileNotFoundError(f"semantic snapshot missing for {service}: {snapshot}")
        rules = load_snapshot_rules(snapshot, service)
        service_rules[service] = rules
        probes = []
        service_blocked = False
        for probe in spec.get("probes") or []:
            actual = bool(matching_rules(rules, probe["input"]))
            expected = probe["expected"]
            expected_ok = (actual and expected == "match") or ((not actual) and expected == "no_match")
            if expected == "review":
                expected_ok = True
                service_blocked = True
            probes.append({**probe, "actual": "match" if actual else "no_match", "result": "pass" if expected_ok else "fail"})
            if not expected_ok:
                service_blocked = True
        status = "blocked" if service_blocked else "pass"
        results[service] = probes
        spec["executed_rule_count"] = len(rules)
        spec["probes"] = probes
        spec["status"] = status
        if status == "blocked":
            any_blocked = True
    doc["execution_status"] = "executed"
    doc["overall_status"] = "blocked" if any_blocked else "pass"
    doc["matcher"] = "src.engine.audit.matcher.rule_matches"
    return doc, service_rules


def run_overlap(doc: dict[str, Any], service_rules: dict[str, list[dict[str, Any]]], semantic: dict[str, Any]) -> dict[str, Any]:
    services = list(service_rules)
    collisions: list[dict[str, Any]] = []
    tested = 0
    for service in services:
        for probe in semantic["services"][service].get("probes") or []:
            if probe.get("result") != "pass":
                continue
            host = probe["input"]
            matched = [other for other in services if matching_rules(service_rules[other], host)]
            tested += 1
            if len(matched) > 1:
                collisions.append({"input": host, "services": matched, "source_service": service})
    doc["status"] = "pass" if not collisions and all(len(service_rules[s]) > 0 for s in services) else "blocked"
    doc["runtime_matcher"] = "src.engine.audit.matcher.rule_matches"
    doc["runtime_probe_count"] = tested
    doc["runtime_collisions"] = collisions
    doc["semantic_overlap"] = {
        "status": "pass" if not collisions else "fail",
        "tested_probe_count": tested,
        "collisions": collisions,
    }
    return doc


def main() -> int:
    semantic = yaml.safe_load(SEMANTIC.read_text(encoding="utf-8"))
    overlap = yaml.safe_load(OVERLAP.read_text(encoding="utf-8"))
    semantic, service_rules = run_semantic(semantic)
    overlap = run_overlap(overlap, service_rules, semantic)
    SEMANTIC.write_text(yaml.safe_dump(semantic, sort_keys=False, allow_unicode=True), encoding="utf-8")
    OVERLAP.write_text(yaml.safe_dump(overlap, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(json.dumps({"semantic": semantic["overall_status"], "overlap": overlap["status"], "runtime_probe_count": overlap["runtime_probe_count"]}, ensure_ascii=False))
    return 0 if semantic["overall_status"] != "fail" and overlap["status"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
