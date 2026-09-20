#!/usr/bin/env python3
"""Build a non-promoting Phase 2 canary attestation report."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "source_release",
    "snapshot_id",
    "content_digest",
    "reconciliation_run_id",
    "v3_run_id",
    "semantic_run_id",
    "rollback_run_id",
    "observation_started_at",
)

def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value

def build_attestation(summary: dict[str, Any]) -> dict[str, Any]:
    services = summary.get("services") or {}
    out: dict[str, Any] = {
        "schema": "phase2_canary_attestation_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_commit": summary.get("source_commit"),
        "services": {},
    }
    for service_id, report in sorted(services.items()):
        source = report.get("source") or {}
        canary = report.get("canary") or {}
        rollback = report.get("rollback") or {}
        fields = {
            "source_release": source.get("release_artifact"),
            "snapshot_id": source.get("snapshot_id"),
            "content_digest": source.get("content_digest"),
            "reconciliation_run_id": canary.get("reconciliation_run_id") or (canary.get("reconciliation") or {}).get("run_id"),
            "v3_run_id": canary.get("v3_release_run_id"),
            "semantic_run_id": canary.get("semantic_run_id"),
            "rollback_run_id": rollback.get("rollback_run"),
            "observation_started_at": None,
        }
        blockers = [
            field for field in REQUIRED_FIELDS
            if not str(fields.get(field) or "").strip()
        ]
        semantic_pass = canary.get("semantic", {}).get("pass") is True
        reconciliation_pass = (
            (canary.get("reconciliation") or {}).get("status") == "PASS"
            or bool(canary.get("reconciliation_run_id"))
        )
        rollback_pass = rollback.get("pass") is True
        golden_pass = canary.get("v3_golden", {}).get("golden_all_pass") is True
        if not golden_pass:
            blockers.append("golden_pass")
        if not semantic_pass:
            blockers.append("seven_client_semantic_pass")
        if not reconciliation_pass:
            blockers.append("collection_reconciliation_pass")
        if not rollback_pass:
            blockers.append("rollback_pass")
        status = (
            "PASSED" if not blockers
            else "READY_FOR_ATTESTATION"
            if golden_pass and semantic_pass and reconciliation_pass and rollback_pass
            else "BLOCKED"
        )
        out["services"][service_id] = {
            "status": status,
            "fields": fields,
            "checks": {
                "golden_pass": golden_pass,
                "seven_client_semantic_pass": semantic_pass,
                "collection_reconciliation_pass": reconciliation_pass,
                "rollback_pass": rollback_pass,
                "production_ready_from_canary_runner": report.get("production_ready") is True,
            },
            "blockers": sorted(set(blockers)),
        }
    out["all_passed"] = bool(
        out["services"]
        and all(item["status"] == "PASSED" for item in out["services"].values())
    )
    return out

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=Path("reports/phase2-canary/summary.json"))
    parser.add_argument("--output", type=Path, default=Path("reports/phase2-canary/attestation.json"))
    args = parser.parse_args()
    if not args.summary.is_file():
        payload = {
            "schema": "phase2_canary_attestation_v1",
            "status": "BLOCKED",
            "error": f"missing summary: {args.summary}",
            "all_passed": False,
            "services": {},
        }
    else:
        payload = build_attestation(_load(args.summary))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
