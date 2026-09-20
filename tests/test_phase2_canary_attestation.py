from scripts.canary_attestation import build_attestation

def test_attestation_stops_before_reconciliation_and_observation():
    summary = {
        "source_commit": "abc",
        "services": {
            "dingding": {
                "source": {
                    "release_artifact": "releases/dingding/snap/release.json",
                    "snapshot_id": "snap-dingding",
                    "content_digest": "digest",
                },
                "canary": {
                    "v3_golden": {"golden_all_pass": True},
                    "v3_release_run_id": "canary-dingding-release-2",
                    "semantic": {"pass": True},
                    "semantic_run_id": "canary-dingding-release-2",
                },
                "rollback": {"rollback_run": "canary-dingding-release-1", "pass": True},
                "production_ready": True,
            }
        },
    }
    report = build_attestation(summary)
    row = report["services"]["dingding"]
    assert row["status"] == "READY_FOR_ATTESTATION"
    assert "reconciliation_run_id" in row["blockers"]
    assert "observation_started_at" in row["blockers"]
    assert row["checks"]["seven_client_semantic_pass"] is True
