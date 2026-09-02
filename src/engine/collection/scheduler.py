from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

DEFAULT_MIN_INTERVAL_HOURS = 24
DEFAULT_RETRY_BASE_MINUTES = 15
DEFAULT_RETRY_MAX_HOURS = 24


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_timestamp(value: Any) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class ScheduleDecision:
    action: str
    reason: str
    retry_at: datetime | None = None


def _hours(value: Any, default: int) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError):
        return default
    return max(1, min(value, 24 * 30))


def decide(previous: dict[str, Any], source: dict[str, Any], *, now: datetime | None = None, force: bool = False) -> ScheduleDecision:
    now = now or utc_now()
    if force:
        return ScheduleDecision("FETCH_FORCED", "manual_force_refresh")

    last_success = parse_timestamp(previous.get("last_success_at"))
    if last_success is None:
        return ScheduleDecision("FETCH_INITIAL", "no_successful_snapshot")

    policy = source.get("collection") or {}
    interval = _hours(policy.get("min_interval_hours"), DEFAULT_MIN_INTERVAL_HOURS)
    fresh_until = last_success + timedelta(hours=interval)
    if now < fresh_until:
        return ScheduleDecision("SKIP_FRESH", "freshness_window_active", fresh_until)

    retry_at = parse_timestamp(previous.get("next_retry_at"))
    if retry_at and now < retry_at:
        return ScheduleDecision("SKIP_RETRY_WINDOW", "failure_backoff_active", retry_at)
    return ScheduleDecision("FETCH_DUE", "freshness_window_expired")


def next_retry_at(*, now: datetime | None = None, failure_count: int = 1, base_minutes: int = DEFAULT_RETRY_BASE_MINUTES, max_hours: int = DEFAULT_RETRY_MAX_HOURS) -> datetime:
    now = now or utc_now()
    exponent = max(0, min(int(failure_count) - 1, 8))
    delay_minutes = min(max(1, base_minutes) * (2**exponent), max(1, max_hours) * 60)
    return now + timedelta(minutes=delay_minutes)
