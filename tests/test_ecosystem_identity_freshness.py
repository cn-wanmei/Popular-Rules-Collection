import datetime as dt
import json
from io import BytesIO

from scripts import generate_ecosystem_release_status as status


NOW = dt.datetime(2026, 11, 8, 12, 0, tzinfo=dt.timezone.utc)


def test_recent_identity_verification_stays_fresh_even_when_snapshot_is_old() -> None:
    result, reason, age = status.identity_freshness(
        True, "ok", "same-digest", "same-digest",
        "2026-11-08T10:57:00Z", NOW)
    assert result == "fresh"
    assert reason == "recent_identity_freshness_workflow_pass"
    assert age == 3780


def test_identity_content_mismatch_is_stale() -> None:
    result, reason, _ = status.identity_freshness(
        True, "ok", "live-digest", "pinned-digest",
        "2026-11-08T10:57:00Z", NOW)
    assert result == "stale"
    assert reason == "identity_content_hash_mismatch"


def test_expired_identity_verification_is_stale() -> None:
    result, reason, _ = status.identity_freshness(
        True, "ok", "same-digest", "same-digest",
        "2026-10-30T00:00:00Z", NOW)
    assert result == "stale"
    assert reason == "identity_verification_expired"


def test_unreadable_identity_is_unknown() -> None:
    result, reason, _ = status.identity_freshness(
        False, "ok", "same-digest", "same-digest",
        "2026-11-08T10:57:00Z", NOW)
    assert result == "unknown"
    assert reason == "snapshot_unreadable"


def test_semantic_warning_is_not_fresh() -> None:
    result, reason, _ = status.identity_freshness(
        True, "warning", "same-digest", "same-digest",
        "2026-11-08T10:57:00Z", NOW)
    assert result == "unknown"
    assert reason == "identity_semantic_warning"


def test_missing_verification_timestamp_is_unknown() -> None:
    result, reason, _ = status.identity_freshness(
        True, "ok", "same-digest", "same-digest", None, NOW)
    assert result == "unknown"
    assert reason == "identity_verification_timestamp_missing"


def test_latest_identity_run_uses_public_api_without_token(monkeypatch) -> None:
    payload = {
        "workflow_runs": [{
            "id": 12345,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2026-11-08T10:57:00Z",
        }]
    }
    monkeypatch.delenv("ICON_DISPATCH_TOKEN", raising=False)
    monkeypatch.setattr(
        status.urllib.request,
        "urlopen",
        lambda *args, **kwargs: BytesIO(json.dumps(payload).encode("utf-8")),
    )
    created, run_id, error = status.fetch_latest_identity_verification()
    assert created == "2026-11-08T10:57:00Z"
    assert run_id == 12345
    assert error is None


def test_latest_failed_identity_run_is_not_accepted(monkeypatch) -> None:
    payload = {
        "workflow_runs": [{
            "id": 12346,
            "status": "completed",
            "conclusion": "failure",
            "created_at": "2026-11-08T10:57:00Z",
        }]
    }
    monkeypatch.setattr(
        status.urllib.request,
        "urlopen",
        lambda *args, **kwargs: BytesIO(json.dumps(payload).encode("utf-8")),
    )
    created, run_id, error = status.fetch_latest_identity_verification()
    assert created == "2026-11-08T10:57:00Z"
    assert run_id == 12346
    assert error == "latest_identity_freshness_run_not_successful"


def test_latest_identity_run_retries_transient_api_503(monkeypatch) -> None:
    payload = {
        "workflow_runs": [{
            "id": 12347,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2026-11-08T10:57:00Z",
        }]
    }
    attempts = {"count": 0}

    def flaky(*args, **kwargs):
        attempts["count"] += 1
        if attempts["count"] == 1:
            import urllib.error
            raise urllib.error.HTTPError(
                "https://api.github.com/runs", 503, "Service Unavailable", {}, None)
        return BytesIO(json.dumps(payload).encode("utf-8"))

    monkeypatch.setattr(status.urllib.request, "urlopen", flaky)
    monkeypatch.setattr(status.time, "sleep", lambda *_: None)
    created, run_id, error = status.fetch_latest_identity_verification()
    assert created == "2026-11-08T10:57:00Z"
    assert run_id == 12347
    assert error is None
    assert attempts["count"] == 2
