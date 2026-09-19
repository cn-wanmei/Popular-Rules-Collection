#!/usr/bin/env python3
"""Phase I: close acceptance-system gaps without claiming data migration completion."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", type=Path, default=ROOT / "config/phase_i_gate_closure.yaml")
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    contract = load_yaml(args.contract)
    errors: list[str] = []

    p0 = load_yaml(ROOT / "config/p0_materialization.yaml").get("services") or []
    identity = load_yaml(ROOT / "config/p0_service_identity.yaml").get("services") or []
    matrix = load_yaml(ROOT / "config/p0_service_production.yaml").get("services") or {}
    p0_ids = [str(x.get("id")) for x in p0 if isinstance(x, dict) and x.get("id")]
    identity_ids = [str(x.get("id")) for x in identity if isinstance(x, dict) and x.get("id")]

    if len(p0_ids) != int((contract.get("p0") or {}).get("queue_size", 50)) or len(set(p0_ids)) != len(p0_ids):
        errors.append("P0 queue is not exactly the contracted 50 unique services")
    if set(identity_ids) != set(p0_ids):
        errors.append("P0 identity keys do not exactly match P0 queue")
    if set(matrix) != set(p0_ids):
        errors.append("P0 production matrix keys do not exactly match P0 queue")

    intentional = load_yaml(ROOT / "config/intentional_unmaterialized.yaml").get("services") or {}
    expected = contract.get("intentional") or {}
    expected_total = int(expected.get("registry_total", -1))
    expected_intentional_only = int(expected.get("intentional_only", -1))
    expected_mixed_ids = set(map(str, expected.get("materialized_and_intentional_ids") or []))
    if len(intentional) != expected_total:
        errors.append(f"intentional registry count={len(intentional)}, expected {expected_total}")
    mixed_ids = {
        sid for sid in intentional if sid in expected_mixed_ids
    }
    intentional_only = len(intentional) - len(mixed_ids)
    if intentional_only != expected_intentional_only:
        errors.append(
            f"intentional-only count={intentional_only}, expected {expected_intentional_only}"
        )
    if mixed_ids != expected_mixed_ids:
        errors.append("materialized-and-intentional service set does not match contract")

    migration = load_yaml(ROOT / "config/canonical_root_migration.yaml")
    directories = load_yaml(ROOT / "config/service_model/directories.yaml")
    canonical = contract.get("canonical") or {}
    if migration.get("current_runtime_root") != canonical.get("current_runtime_root"):
        errors.append("migration current root disagrees with Phase I contract")
    if migration.get("target_runtime_root") != canonical.get("target_runtime_root"):
        errors.append("migration target root disagrees with Phase I contract")
    target = migration.get("target_layout") or {}
    layout = canonical.get("target_layout") or {}
    for key in ("aggregate", "service", "china", "rule_file"):
        if target.get(key) != layout.get(key):
            errors.append(f"target layout mismatch for {key}")
    directory_layout = directories.get("layout") or {}
    if directory_layout.get("aggregate") != layout.get("aggregate"):
        errors.append("directory policy aggregate layout mismatch")
    if directory_layout.get("service") != layout.get("service"):
        errors.append("directory policy service layout mismatch")
    if directory_layout.get("china_aggregate") != layout.get("china"):
        errors.append("directory policy China layout mismatch")

    loader = (ROOT / "src/engine/ingest/v1_loader.py").read_text(encoding="utf-8")
    if not re.search(r'Path\(["\']rule/["\']\)|rule/ _index|rule/_index|\brule/\b', loader):
        errors.append("V1 loader no longer exposes a detectable current runtime root contract")
    if "rules/" in loader and "rule/" not in loader:
        errors.append("V1 loader appears switched to target before Phase N")

    det_path = ROOT / "reports/v1/V3_DETERMINISM_FINAL.json"
    det = load_json(det_path) if det_path.is_file() else {}
    if det.get("all_pass") is not True or det.get("match") is not True:
        errors.append("determinism evidence is not green")
    builds = det.get("builds") or []
    if len(builds) < 3:
        errors.append("determinism evidence must contain production + two replays")
    else:
        artifacts = {str(b.get("artifacts")) for b in builds}
        overall = {str(b.get("overall")) for b in builds}
        if len(artifacts) != 1 or len(overall) != 1:
            errors.append("determinism artifact/overall digests differ across builds")
    if not det.get("source_run_id") or not det.get("snapshot_id"):
        errors.append("determinism report is missing run/snapshot binding fields")

    payload = {
        "schema": "phase_i_gate_closure_report_v1",
        "head": git_head(),
        "p0_queue_size": len(p0_ids),
        "intentional_registry_total": len(intentional),
        "intentional_only": intentional_only,
        "materialized_and_intentional": sorted(mixed_ids),
        "determinism": {
            "source_run_id": det.get("source_run_id"),
            "snapshot_id": det.get("snapshot_id"),
            "all_pass": det.get("all_pass"),
            "match": det.get("match"),
        },
        "pass": not errors,
        "errors": errors,
    }
    output = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    print(output, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output, encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
