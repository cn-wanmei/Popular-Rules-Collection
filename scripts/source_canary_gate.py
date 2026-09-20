#!/usr/bin/env python3
"""Fail-closed validation for per-service Source Canary state."""
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

REQUIRED_CANARY_FIELDS = (
    "source_release",
    "snapshot_id",
    "content_digest",
    "reconciliation_run_id",
    "v3_run_id",
    "semantic_run_id",
    "rollback_run_id",
    "observation_started_at",
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
    if prs.get("enabled") is not False:
        errors.append("PRS global registry must remain disabled during Phase 2")

    canary = policy.get("canary") or {}
    if canary.get("enabled") is not False:
        errors.append("global canary switch must remain disabled until a service is explicitly promoted")

    canary_services: list[str] = []

    for sid in SERVICES:
        item = services.get(sid) or {}
        stage = str(item.get("state", "review")).lower()
        enabled = bool(item.get("enabled", False))
        if stage not in {"review", "verified", "canary", "production"}:
            errors.append(f"{sid}: invalid state {stage}")
        if stage == "canary":
            canary_services.append(sid)
        if stage in {"canary", "production"} and not enabled:
            errors.append(f"{sid}: {stage} requires enabled=true")
        if stage in {"review", "verified"} and enabled:
            errors.append(f"{sid}: {stage} must keep enabled=false")
        attestation = item.get("attestation") or {}
        attestation_status = str(attestation.get("status", "pending")).lower()

        if stage == "canary":
            if attestation_status not in {"pending", "passed"}:
                errors.append(f"{sid}: canary invalid attestation status {attestation_status}")
            if attestation_status == "passed":
                for field in REQUIRED_CANARY_FIELDS:
                    if not str(attestation.get(field, "")).strip():
                        errors.append(f"{sid}: canary passed missing attestation field {field}")

        if stage == "production":
            if attestation_status != "passed":
                errors.append(f"{sid}: production requires attestation.status=passed")
            for field in REQUIRED_CANARY_FIELDS:
                if not str(attestation.get(field, "")).strip():
                    errors.append(f"{sid}: production missing attestation field {field}")

    if len(canary_services) > 1:
        errors.append(
            "at most one service may be state=canary at a time: "
            + ", ".join(sorted(canary_services))
        )

    result = {
        "schema": "source_canary_state_gate_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
