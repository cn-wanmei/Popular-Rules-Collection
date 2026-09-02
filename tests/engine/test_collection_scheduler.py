from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.engine.collection.scheduler import decide, next_retry_at

NOW = datetime(2026, 9, 2, 8, 0, tzinfo=timezone.utc)


def test_scheduler_fetches_without_successful_snapshot() -> None:
    result = decide({}, {})
    assert result.action == "FETCH_INITIAL"
    assert result.reason == "no_successful_snapshot"


def test_scheduler_skips_fresh_snapshot() -> None:
    previous = {"last_success_at": (NOW - timedelta(hours=2)).isoformat()}
    result = decide(previous, {}, now=NOW)
    assert result.action == "SKIP_FRESH"
    assert result.reason == "freshness_window_active"


def test_scheduler_uses_source_interval() -> None:
    previous = {"last_success_at": (NOW - timedelta(hours=7)).isoformat()}
    result = decide(previous, {"collection": {"min_interval_hours": 12}}, now=NOW)
    assert result.action == "SKIP_FRESH"
    result = decide(previous, {"collection": {"min_interval_hours": 6}}, now=NOW)
    assert result.action == "FETCH_DUE"


def test_scheduler_honors_failure_backoff() -> None:
    retry_at = NOW + timedelta(minutes=20)
    previous = {
        "last_success_at": (NOW - timedelta(hours=48)).isoformat(),
        "next_retry_at": retry_at.isoformat(),
        "failure_count": 1,
    }
    result = decide(previous, {}, now=NOW)
    assert result.action == "SKIP_RETRY_WINDOW"
    assert result.retry_at == retry_at


def test_force_refresh_bypasses_freshness_and_backoff() -> None:
    previous = {
        "last_success_at": (NOW - timedelta(hours=1)).isoformat(),
        "next_retry_at": (NOW + timedelta(hours=1)).isoformat(),
    }
    result = decide(previous, {}, now=NOW, force=True)
    assert result.action == "FETCH_FORCED"


def test_retry_backoff_is_exponential_and_capped() -> None:
    first = next_retry_at(now=NOW, failure_count=1)
    second = next_retry_at(now=NOW, failure_count=2)
    capped = next_retry_at(now=NOW, failure_count=20)
    assert first == NOW + timedelta(minutes=15)
    assert second == NOW + timedelta(minutes=30)
    assert capped == NOW + timedelta(hours=24)
