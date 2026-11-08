import datetime as dt

from scripts.generate_ecosystem_release_status import identity_freshness


NOW = dt.datetime(2026, 11, 8, 12, 0, tzinfo=dt.timezone.utc)


def _report() -> dict:
    return {
        "schema": "icon_identity_freshness_v4",
        "drift": False,
        "content_match": True,
        "live_file_sha256": "same-digest",
        "pinned_file_sha256": "same-digest",
        "only_in_collection": [],
        "only_in_snapshot": [],
        "field_mismatches": [],
    }


def test_recent_identity_verification_stays_fresh_even_when_snapshot_is_old() -> None:
    status, reason, age = identity_freshness(
        True, "ok", "same-digest", "same-digest",
        _report(), "2026-11-08T10:57:00Z", NOW)
    assert status == "fresh"
    assert reason == "recent_identity_freshness_workflow_pass"
    assert age == 3780


def test_identity_content_mismatch_is_stale() -> None:
    status, reason, _ = identity_freshness(
        True, "ok", "live-digest", "pinned-digest",
        _report(), "2026-11-08T10:57:00Z", NOW)
    assert status == "stale"
    assert reason == "identity_content_hash_mismatch"


def test_identity_verification_drift_is_stale() -> None:
    report = _report()
    report["drift"] = True
    status, reason, _ = identity_freshness(
        True, "ok", "same-digest", "same-digest",
        report, "2026-11-08T10:57:00Z", NOW)
    assert status == "stale"
    assert reason == "identity_freshness_drift_detected"


def test_expired_identity_verification_is_stale() -> None:
    status, reason, _ = identity_freshness(
        True, "ok", "same-digest", "same-digest",
        _report(), "2026-10-30T00:00:00Z", NOW)
    assert status == "stale"
    assert reason == "identity_verification_expired"


def test_unreadable_identity_is_unknown() -> None:
    status, reason, _ = identity_freshness(
        False, "ok", "same-digest", "same-digest",
        _report(), "2026-11-08T10:57:00Z", NOW)
    assert status == "unknown"
    assert reason == "snapshot_unreadable"


def test_missing_verification_report_is_unknown() -> None:
    status, reason, _ = identity_freshness(
        True, "ok", "same-digest", "same-digest",
        None, None, NOW)
    assert status == "unknown"
    assert reason == "identity_verification_report_unavailable"


def test_semantic_warning_is_not_fresh() -> None:
    status, reason, _ = identity_freshness(
        True, "warning", "same-digest", "same-digest",
        _report(), "2026-11-08T10:57:00Z", NOW)
    assert status == "unknown"
    assert reason == "identity_semantic_warning"


def test_unexpected_identity_report_schema_is_unknown() -> None:
    report = _report()
    report["schema"] = "unexpected"
    status, reason, _ = identity_freshness(
        True, "ok", "same-digest", "same-digest",
        report, "2026-11-08T10:57:00Z", NOW)
    assert status == "unknown"
    assert reason == "identity_verification_schema_invalid"
