from __future__ import annotations

from scripts.phase2_production_unlock_gate import qualify


def _base():
    return (
        {
            "prs": {"enabled": False},
            "canary": {"enabled": True, "services": ["dingding"]},
            "production_unlock": {
                "requires": [
                    "source_release_verified",
                    "collection_reconciliation_pass",
                    "v3_build_pass",
                    "seven_client_semantic_pass",
                    "rollback_validated",
                    "observation_window_started",
                ]
            },
        },
        {
            "services": {
                "dingding": {
                    "state": "canary",
                    "enabled": True,
                    "attestation": {"status": "pending"},
                }
            }
        },
        {
            "schema": "phase2_canary_attestation_v1",
            "source_commit": "source-sha",
            "services": {
                "dingding": {
                    "status": "PASSED",
                    "fields": {
                        "source_release": "release.json",
                        "snapshot_id": "snap-dingding",
                        "content_digest": "digest",
                        "reconciliation_run_id": "reconcile-1",
                        "v3_run_id": "run-2",
                        "semantic_run_id": "run-2",
                        "rollback_run_id": "run-1",
                        "observation_started_at": "2026-09-21T00:00:00+00:00",
                    },
                    "checks": {
                        "golden_pass": True,
                        "seven_client_semantic_pass": True,
                        "collection_reconciliation_pass": True,
                        "rollback_pass": True,
                        "observation_window_started": True,
                    },
                }
            },
        },
        {
            "source": {"commit": "source-sha"},
            "canary": {
                "semantic": {
                    "pass": True,
                    "passed_clients": [
                        "egern", "loon", "mihomo", "quantumultx",
                        "shadowrocket", "singbox", "surge",
                    ],
                },
                "reconciliation": {"status": "PASS"},
                "observation": {"status": "ACTIVE", "promotes": False},
            },
            "production_ready": True,
        },
    )


def test_unlock_gate_is_non_mutating_and_passes_complete_evidence():
    result = qualify("dingding", *_base())
    assert result["status"] == "PASS"
    assert result["promotes"] is False


def test_unlock_gate_rejects_id_only_reconciliation():
    policy, state, attestation, canary = _base()
    attestation["services"]["dingding"]["checks"]["collection_reconciliation_pass"] = False
    canary["canary"]["reconciliation"] = {"status": "BLOCKED", "run_id": "reconcile-1"}
    result = qualify("dingding", policy, state, attestation, canary)
    assert result["status"] == "BLOCKED"
    assert any("collection_reconciliation_pass" in item for item in result["failures"])


def test_unlock_gate_rejects_production_state_mutation():
    policy, state, attestation, canary = _base()
    state["services"]["dingding"]["state"] = "production"
    result = qualify("dingding", policy, state, attestation, canary)
    assert result["status"] == "BLOCKED"
    assert any("state must remain canary" in item for item in result["failures"])
