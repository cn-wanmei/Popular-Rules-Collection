from scripts.generate_ecosystem_release_status import identity_freshness


def test_unchanged_identity_content_stays_fresh_even_when_snapshot_is_old() -> None:
    status, reason = identity_freshness(
        True, "ok", "same-digest", "same-digest")
    assert status == "fresh"
    assert reason == "identity_content_hash_match"


def test_identity_content_mismatch_is_stale() -> None:
    status, reason = identity_freshness(
        True, "ok", "live-digest", "pinned-digest")
    assert status == "stale"
    assert reason == "identity_content_hash_mismatch"


def test_unreadable_identity_is_unknown() -> None:
    status, reason = identity_freshness(
        False, "ok", "live-digest", "pinned-digest")
    assert status == "unknown"
    assert reason == "snapshot_unreadable"


def test_missing_identity_hash_is_unknown() -> None:
    status, reason = identity_freshness(
        True, "warning", "live-digest", None)
    assert status == "unknown"
    assert reason == "identity_content_hash_missing"
