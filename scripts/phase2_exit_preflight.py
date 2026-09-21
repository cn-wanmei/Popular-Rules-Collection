#!/usr/bin/env python3
"""Evidence-bound Phase 2 exit preflight.

This gate is intentionally non-mutating. It answers whether the Collection
tree has enough service-level evidence to begin the Phase 2 exit procedure.
Production promotion itself remains service-scoped and PR-gated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "config" / "source_canary_state.yaml"
IMMUTABLE_PATH = ROOT / "sources" / "immutable_registry.yaml"

SERVICES = (
    "1688",
    "cainiao",
    "dingding",
    "qqmail",
    "qqmusic",
    "taobao",
    "tencentcloud",
    "tmall",
)

REQUIRED_ATTESTATION = (
    "status",
    "source_release",
    "snapshot_id",
    "content_digest",
    "reconciliation_run_id",
    "v3_run_id",
    "semantic_run_id",
    "rollback_run_id",
    "observation_run_id",
    "observation_started_at",
    "production_unlock_run_id",
    "reconciliation_pass",
    "seven_client_semantic_pass",
    "rollback_pass",
    "observation_pass",
    "source_official_evidence_only",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def evaluate(
    state: dict[str, Any],
    immutable: dict[str, Any],
) -> dict[str, Any]:
    services = state.get("services") or {}
    bindings = immutable.get("bindings") or {}
    service_reports: dict[str, Any] = {}
    blockers: dict[str, list[str]] = {}

    for service_id in SERVICES:
        item = services.get(service_id)
        binding = bindings.get(service_id)
        failures: list[str] = []

        if not isinstance(item, dict):
            failures.append("service_state_missing")
            item = {}
        if item.get("state") != "production":
            failures.append(f"state={item.get('state')!r}")
        if item.get("enabled") is not True:
            failures.append("enabled!=true")

        attestation = item.get("attestation")
        if not isinstance(attestation, dict):
            failures.append("attestation_missing")
            attestation = {}
        for key in REQUIRED_ATTESTATION:
            value = attestation.get(key)
            if key.endswith("_pass") or key == "source_official_evidence_only":
                if value is not True:
                    failures.append(f"{key}!=true")
            elif not str(value or "").strip():
                failures.append(f"{key}=missing")
        if int(attestation.get("seed_only_count", 0) or 0) != 0:
            failures.append("seed_only_count!=0")
        if int(attestation.get("conflict_count", 0) or 0) != 0:
            failures.append("conflict_count!=0")

        if not isinstance(binding, dict) or binding.get("status") != "active":
            failures.append("immutable_binding_missing_or_inactive")
            binding = {}
        for key in ("source_ref", "snapshot_id", "content_digest", "artifact_path", "release_path"):
            if not str(binding.get(key) or "").strip():
                failures.append(f"immutable_{key}=missing")

        service_reports[service_id] = {
            "production": not failures,
            "state": item.get("state"),
            "enabled": item.get("enabled"),
            "attestation_status": attestation.get("status"),
            "snapshot_id": attestation.get("snapshot_id"),
            "content_digest": attestation.get("content_digest"),
            "immutable_source_ref": binding.get("source_ref"),
            "blockers": failures,
        }
        if failures:
            blockers[service_id] = failures

    ready = not blockers
    return {
        "schema": "phase2_exit_preflight_v1",
        "phase": 2,
        "status": "PASS" if ready else "BLOCKED",
        "exit_ready": ready,
        "population": {
            "required_services": len(SERVICES),
            "production_services": sum(
                1 for x in service_reports.values() if x["production"]
            ),
            "blocked_services": len(blockers),
        },
        "services": service_reports,
        "blockers": blockers,
        "next_phase": "phase2_exit" if ready else "service_production_completion",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=STATE_PATH)
    parser.add_argument("--immutable", type=Path, default=IMMUTABLE_PATH)
    args = parser.parse_args()

    result = evaluate(_load_yaml(args.state), _load_yaml(args.immutable))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["exit_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
