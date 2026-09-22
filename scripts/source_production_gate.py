#!/usr/bin/env python3
"""Fail-closed Production unlock gate for Phase 2 upstream services."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = (
    "1688", "cainiao", "dingding", "qqmail",
    "qqmusic", "taobao", "tencentcloud", "tmall",
)

PRODUCTION_REQUIRED = (
    "source_release",
    "snapshot_id",
    "content_digest",
    "reconciliation_run_id",
    "v3_run_id",
    "semantic_run_id",
    "rollback_run_id",
    "observation_started_at",
    "production_unlock_run_id",
)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def main() -> int:
    state = load_yaml(ROOT / "config" / "source_canary_state.yaml")
    policy = load_yaml(ROOT / "config" / "source_promotion_policy.yaml")
    services = state.get("services") or {}
    errors: list[str] = []

    prs = policy.get("prs") or {}
    if prs.get("enabled") is not True:
        errors.append("PRS controlled promotion registry must be enabled")

    canary_policy = policy.get("canary") or {}
    active_canaries = {
        sid for sid, item in services.items()
        if isinstance(item, dict) and item.get("state") == "canary" and item.get("enabled") is True
    }
    declared_canaries = {str(x).strip() for x in (canary_policy.get("services") or []) if str(x).strip()}
    if canary_policy.get("enabled") is not True:
        errors.append("canary policy must be enabled for an active canary lifecycle")
    if declared_canaries != active_canaries:
        errors.append(
            "canary policy/state divergence: "
            f"policy={sorted(declared_canaries)} state={sorted(active_canaries)}"
        )

    for sid in SERVICES:
        item = services.get(sid) or {}
        stage = str(item.get("state", "review")).lower()
        enabled = bool(item.get("enabled", False))
        attestation = item.get("attestation") or {}

        if stage != "production":
            continue

        if not enabled:
            errors.append(f"{sid}: production requires enabled=true")
        if attestation.get("status") != "passed":
            errors.append(f"{sid}: production requires attestation.status=passed")

        for field in PRODUCTION_REQUIRED:
            if not str(attestation.get(field, "")).strip():
                errors.append(f"{sid}: production missing {field}")

        if attestation.get("reconciliation_pass") is not True:
            errors.append(f"{sid}: reconciliation_pass must be true")
        if attestation.get("seven_client_semantic_pass") is not True:
            errors.append(f"{sid}: seven_client_semantic_pass must be true")
        if attestation.get("rollback_pass") is not True:
            errors.append(f"{sid}: rollback_pass must be true")
        if attestation.get("observation_pass") is not True:
            errors.append(f"{sid}: observation_pass must be true")
        if attestation.get("source_official_evidence_only") is not True:
            errors.append(f"{sid}: source_official_evidence_only must be true")
        if int(attestation.get("seed_only_count", 0) or 0) != 0:
            errors.append(f"{sid}: seed_only_count must be zero")
        if int(attestation.get("conflict_count", 0) or 0) != 0:
            errors.append(f"{sid}: conflict_count must be zero")

    result = {
        "schema": "source_production_unlock_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
