#!/usr/bin/env python3
"""Phase 2 content-level Source <-> Collection reconciliation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError(f"expected YAML object: {path}")
    return value


def _domains_from_file(path: Path) -> list[str]:
    values = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        values.append(value)
    return sorted(set(values))


def _snapshot(source_root: Path, service_id: str, snapshot_id: str) -> tuple[Path, dict[str, Any]]:
    candidates = []
    for path in (source_root / "snapshots").glob("*/manifest.json"):
        manifest = _load_json(path)
        if manifest.get("schema") != "source_snapshot_v2":
            continue
        if manifest.get("service_id") != service_id:
            continue
        if snapshot_id and manifest.get("snapshot_id") != snapshot_id:
            continue
        candidates.append((path.parent, manifest))
    if not candidates:
        raise RuntimeError(f"{service_id}: source snapshot not found for {snapshot_id or 'latest'}")
    return max(candidates, key=lambda item: str(item[1].get("created_at", "")))


def _ir_domain_rules(path: Path) -> list[str]:
    data = _load_json(path)
    values = []
    for rule in data.get("rules") or []:
        if not isinstance(rule, dict):
            continue
        if str(rule.get("type") or "").strip().lower().replace("-", "_") != "domain":
            continue
        value = str(rule.get("value") or "").strip()
        if value:
            values.append(value)
    return sorted(set(values))


def reconcile_service(
    service_id: str,
    source_root: Path,
    canary_root: Path,
    source_commit: str,
    v3_run_id: str,
    snapshot_id: str = "",
) -> dict[str, Any]:
    snapshot_dir, snapshot = _snapshot(source_root, service_id, snapshot_id)
    effective_snapshot_id = str(snapshot.get("snapshot_id") or "")
    content_digest = str(snapshot.get("content_digest") or "")
    if not effective_snapshot_id or not content_digest:
        raise RuntimeError(f"{service_id}: snapshot identity is incomplete")

    domains_path = snapshot_dir / "domains.txt"
    if not domains_path.is_file():
        raise RuntimeError(f"{service_id}: domains.txt missing")
    source_domains = _domains_from_file(domains_path)
    manifest_domains = sorted(
        set(str(value).strip() for value in (snapshot.get("domains") or []) if str(value).strip())
    )
    if source_domains != manifest_domains:
        raise RuntimeError(
            f"{service_id}: snapshot domains.txt != manifest domains "
            f"(file={len(source_domains)}, manifest={len(manifest_domains)})"
        )
    if int(snapshot.get("domain_count", 0) or 0) != len(source_domains):
        raise RuntimeError(
            f"{service_id}: snapshot domain_count mismatch "
            f"(manifest={snapshot.get('domain_count')}, actual={len(source_domains)})"
        )

    release_file = source_root / "releases" / service_id / effective_snapshot_id / "release.json"
    if not release_file.is_file():
        raise RuntimeError(f"{service_id}: source release artifact missing")
    release = _load_json(release_file)
    if release.get("snapshot_id") != effective_snapshot_id:
        raise RuntimeError(f"{service_id}: release snapshot binding mismatch")
    if release.get("content_digest") != content_digest:
        raise RuntimeError(f"{service_id}: release content_digest mismatch")

    registry = _load_yaml(ROOT / "sources" / "registry.yaml")
    prs = next(
        (item for item in registry.get("sources") or [] if item.get("id") == "popular-rules-source"),
        None,
    )
    if not prs:
        raise RuntimeError(f"{service_id}: PRS registry entry missing")
    if prs.get("enabled") is not False:
        raise RuntimeError(f"{service_id}: PRS must remain globally disabled")
    registration = next(
        (
            item for item in prs.get("rules") or []
            if str(item.get("service") or item.get("name") or "") == service_id
        ),
        None,
    )
    if not registration:
        raise RuntimeError(f"{service_id}: PRS service registration missing")
    if registration.get("enabled") is not True:
        raise RuntimeError(f"{service_id}: PRS service registration must be enabled for its immutable Phase 2 binding")
    expected_path = f"generated/source/{service_id}/domains.txt"
    if registration.get("path") != expected_path:
        raise RuntimeError(
            f"{service_id}: registry path mismatch: {registration.get('path')} != {expected_path}"
        )

    binding_file = canary_root / "input" / "source-binding.json"
    if not binding_file.is_file():
        raise RuntimeError(f"{service_id}: source binding artifact missing")
    binding = _load_json(binding_file)
    expected_binding = {
        "repository": "cn-wanmei/Popular-Rules-Source",
        "source_commit": source_commit,
        "service_id": service_id,
        "snapshot_id": effective_snapshot_id,
        "content_digest": content_digest,
        "domain_count": len(source_domains),
    }
    for key, expected in expected_binding.items():
        if binding.get(key) != expected:
            raise RuntimeError(
                f"{service_id}: source binding mismatch for {key}: "
                f"{binding.get(key)!r} != {expected!r}"
            )

    input_file = canary_root / "input" / "services" / f"{service_id}.yaml"
    if not input_file.is_file():
        raise RuntimeError(f"{service_id}: Collection input missing")
    input_doc = _load_yaml(input_file)
    input_domains = sorted(
        set(
            str(rule.get("value") or "").strip()
            for rule in (input_doc.get("rules") or [])
            if isinstance(rule, dict)
            and str(rule.get("type") or "").strip().lower() == "domain"
            and str(rule.get("value") or "").strip()
        )
    )
    if input_domains != source_domains:
        raise RuntimeError(
            f"{service_id}: Collection input domain set mismatch "
            f"(source={len(source_domains)}, collection={len(input_domains)})"
        )

    ir_file = canary_root / "data" / "runs" / v3_run_id / "ir" / "ir.json"
    if not ir_file.is_file():
        raise RuntimeError(f"{service_id}: V3 IR missing for {v3_run_id}")
    ir_domains = _ir_domain_rules(ir_file)
    if ir_domains != source_domains:
        raise RuntimeError(
            f"{service_id}: V3 IR domain set mismatch "
            f"(source={len(source_domains)}, ir={len(ir_domains)})"
        )

    domain_digest = hashlib.sha256(
        json.dumps(source_domains, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    identity = {
        "service_id": service_id,
        "source_commit": source_commit,
        "snapshot_id": effective_snapshot_id,
        "content_digest": content_digest,
        "domain_digest": domain_digest,
        "v3_run_id": v3_run_id,
    }
    run_id = "reconcile-" + service_id + "-" + hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]

    return {
        "schema": "phase2_collection_reconciliation_v1",
        "status": "PASS",
        "run_id": run_id,
        "service_id": service_id,
        "source_commit": source_commit,
        "snapshot_id": effective_snapshot_id,
        "content_digest": content_digest,
        "domain_digest": domain_digest,
        "v3_run_id": v3_run_id,
        "checks": {
            "source_snapshot_domain_set": True,
            "source_release_binding": True,
            "registry_registered": True,
            "prs_global_disabled": True,
            "prs_service_enabled": True,
            "source_binding_exact": True,
            "collection_input_exact": True,
            "v3_ir_exact": True,
        },
        "counts": {
            "domains": len(source_domains),
            "ir_domain_rules": len(ir_domains),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service", required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--v3-run-id", required=True)
    parser.add_argument("--snapshot-id", default="")
    parser.add_argument("--canary-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = reconcile_service(
        args.service,
        args.source_root.resolve(),
        args.canary_root.resolve(),
        args.source_commit,
        args.v3_run_id,
        args.snapshot_id,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
