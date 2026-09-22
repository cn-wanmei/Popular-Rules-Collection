#!/usr/bin/env python3
"""Fail-closed, non-mutating Production Unlock qualification check."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PREREQUISITES = {
    "source_release_verified",
    "immutable_lineage_match",
    "collection_reconciliation_pass",
    "v3_build_pass",
    "seven_client_semantic_pass",
    "rollback_validated",
    "observation_window_started",
}


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


def qualify(
    service_id: str,
    policy: dict[str, Any],
    state: dict[str, Any],
    attestation: dict[str, Any],
    canary_report: dict[str, Any],
) -> dict[str, Any]:
    failures: list[str] = []

    if (policy.get("prs") or {}).get("enabled") is not False:
        failures.append("policy.prs.enabled must remain false")
    if (policy.get("canary") or {}).get("enabled") is not False:
        failures.append("policy.canary.enabled must remain false")

    prerequisites = set((policy.get("production_unlock") or {}).get("requires") or [])
    if prerequisites != REQUIRED_PREREQUISITES:
        failures.append(
            "production unlock prerequisite set mismatch: "
            f"{sorted(prerequisites)}"
        )

    state_row = (state.get("services") or {}).get(service_id) or {}
    if state_row.get("state") != "canary":
        failures.append(f"{service_id}: state must remain canary")
    if state_row.get("enabled") is not True:
        failures.append(f"{service_id}: enabled must remain true for the active canary")
    if (state_row.get("attestation") or {}).get("status") not in ("pending", "ready"):
        failures.append(f"{service_id}: state attestation status must not be production")

    att_row = (attestation.get("services") or {}).get(service_id) or {}
    if att_row.get("status") != "PASSED":
        failures.append(f"{service_id}: attestation status is not PASSED")

    checks = att_row.get("checks") or {}
    for key in (
        "golden_pass",
        "seven_client_semantic_pass",
        "collection_reconciliation_pass",
        "rollback_pass",
        "observation_window_started",
    ):
        if checks.get(key) is not True:
            failures.append(f"{service_id}: attestation check {key} is not true")

    fields = att_row.get("fields") or {}
    for key in (
        "source_release",
        "snapshot_id",
        "content_digest",
        "reconciliation_run_id",
        "v3_run_id",
        "semantic_run_id",
        "rollback_run_id",
        "observation_started_at",
    ):
        if not str(fields.get(key) or "").strip():
            failures.append(f"{service_id}: missing attestation field {key}")

    summary_source_commit = str(attestation.get("source_commit") or "").strip()
    report_source_commit = str((canary_report.get("source") or {}).get("commit") or "").strip()
    if not summary_source_commit or summary_source_commit != report_source_commit:
        failures.append(f"{service_id}: attestation/source report commit mismatch")

    canary = canary_report.get("canary") or {}
    semantic = canary.get("semantic") or {}
    if len(semantic.get("passed_clients") or []) != 7:
        failures.append(f"{service_id}: seven-client semantic did not report exactly 7 passed clients")
    if sorted(semantic.get("passed_clients") or []) != [
        "egern", "loon", "mihomo", "quantumultx", "shadowrocket", "singbox", "surge"
    ]:
        failures.append(f"{service_id}: seven-client semantic client set is incomplete or unexpected")
    if (canary.get("reconciliation") or {}).get("status") != "PASS":
        failures.append(f"{service_id}: canary reconciliation status is not PASS")
    if (canary.get("semantic") or {}).get("pass") is not True:
        failures.append(f"{service_id}: canary semantic result is not PASS")
    if canary_report.get("production_ready") is not True:
        failures.append(f"{service_id}: canary runner production_ready is not true")

    observation = canary.get("observation") or {}
    if observation.get("status") != "ACTIVE":
        failures.append(f"{service_id}: observation window is not ACTIVE")
    if observation.get("promotes") is not False:
        failures.append(f"{service_id}: observation must be non-promoting")

    return {
        "schema": "phase2_production_unlock_gate_v1",
        "status": "PASS" if not failures else "BLOCKED",
        "service_id": service_id,
        "promotes": False,
        "failures": failures,
        "requirements": sorted(REQUIRED_PREREQUISITES),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service", required=True)
    parser.add_argument("--policy", type=Path, default=Path("config/source_promotion_policy.yaml"))
    parser.add_argument("--state", type=Path, default=Path("config/source_canary_state.yaml"))
    parser.add_argument("--attestation", type=Path, default=Path("reports/phase2-canary/attestation.json"))
    parser.add_argument("--canary-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = qualify(
        args.service,
        _load_yaml(args.policy),
        _load_yaml(args.state),
        _load_json(args.attestation),
        _load_json(args.canary_report),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
