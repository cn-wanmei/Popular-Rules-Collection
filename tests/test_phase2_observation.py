from __future__ import annotations

from scripts.phase2_observation import start_observation


def test_observation_starts_only_with_all_prerequisites():
    report = start_observation(
        "dingding",
        "source-sha",
        "snap-dingding",
        "digest",
        "canary-dingding-release-2",
        "canary-dingding-release-2",
        "reconcile-dingding-1234567890abcdef",
        "canary-dingding-release-1",
    )
    assert report["status"] == "ACTIVE"
    assert report["promotes"] is False
    assert report["prerequisites"]["collection_reconciliation_pass"] is True
    assert report["binding"]["source_commit"] == "source-sha"
    assert report["run_id"].startswith("observe-dingding-")


def test_observation_rejects_missing_rollback_binding():
    try:
        start_observation(
            "dingding",
            "source-sha",
            "snap-dingding",
            "digest",
            "run-2",
            "run-2",
            "reconcile-dingding-1234567890abcdef",
            "",
        )
    except RuntimeError as exc:
        assert "rollback_run_id" in str(exc)
    else:
        raise AssertionError("missing rollback binding must block observation")
