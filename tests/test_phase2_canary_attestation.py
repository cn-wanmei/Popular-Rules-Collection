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
                    "reconciliation_run_id": "reconcile-dingding-abcdef1234567890",
                    "reconciliation": {"status": "PASS", "run_id": "reconcile-dingding-abcdef1234567890"},
                },
                "rollback": {"rollback_run": "canary-dingding-release-1", "pass": True},
                "production_ready": True,
            }
        },
    }
    report = build_attestation(summary)
    row = report["services"]["dingding"]
    assert row["status"] == "READY_FOR_ATTESTATION"
    assert "reconciliation_run_id" not in row["blockers"]
    assert "observation_started_at" in row["blockers"]
    assert row["checks"]["seven_client_semantic_pass"] is True
    assert row["checks"]["collection_reconciliation_pass"] is True


def test_attestation_does_not_accept_reconciliation_id_without_pass():
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
                    "v3_release_run_id": "run-2",
                    "semantic": {"pass": True},
                    "semantic_run_id": "run-2",
                    "reconciliation_run_id": "reconcile-dingding-present",
                    "reconciliation": {"status": "BLOCKED", "run_id": "reconcile-dingding-present"},
                },
                "rollback": {"rollback_run": "run-1", "pass": True},
            }
        },
    }
    row = build_attestation(summary)["services"]["dingding"]
    assert row["status"] == "BLOCKED"
    assert "collection_reconciliation_pass" in row["blockers"]
