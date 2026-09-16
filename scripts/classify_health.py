#!/usr/bin/env python3
"""Derive source health from raw telemetry + independent lifecycle registry."""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
HEALTH = ROOT / "sources" / "health.yaml"
LIFECYCLE = ROOT / "sources" / "lifecycle.yaml"
POLICY = ROOT / "config" / "health_policy.yaml"
OUT = ROOT / "reports" / "source_health_status.yaml"


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_ts(value: Any) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def lifecycle_map(data: dict[str, Any]) -> dict[str, str]:
    return {str(k): str(v.get("lifecycle", "active")) for k, v in (data.get("sources") or {}).items()}


def classify(item: dict[str, Any], lifecycle: str, now: dt.datetime, policy: dict[str, Any]) -> tuple[str, str, int | None]:
    if lifecycle in {"retired", "disabled"}:
        return "retired", f"source lifecycle is {lifecycle}", None
    last_success = parse_ts(item.get("last_success"))
    failures = int(item.get("failure_count", 0) or 0)
    if last_success is None:
        return "failed", "no successful fetch recorded", None
    age = max(0, int((now - last_success).total_seconds() // 3600))
    limits = policy.get("classification", {})
    healthy_h = int(limits.get("healthy_max_age_hours", 48))
    degraded_h = int(limits.get("degraded_max_age_hours", 168))
    if failures > 0 and bool(limits.get("failed_if_failure_count_positive", True)):
        return "failed", "failure_count is positive", age
    if age <= healthy_h:
        return "healthy", f"last success {age}h ago", age
    if age <= degraded_h:
        return "degraded", f"last success {age}h ago", age
    return "stale", f"last success {age}h ago", age


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    health = yaml.safe_load(HEALTH.read_text(encoding="utf-8")) or {}
    lifecycle = yaml.safe_load(LIFECYCLE.read_text(encoding="utf-8")) or {}
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    lifecycles = lifecycle_map(lifecycle)
    now = utc_now()
    sources: dict[str, dict[str, Any]] = {}
    for source_id, item in (health.get("sources") or {}).items():
        state = lifecycles.get(source_id, "active")
        status, reason, age = classify(item or {}, state, now, policy)
        sources[source_id] = {
            "lifecycle": state,
            "status": status,
            "reason": reason,
            "last_success": item.get("last_success"),
            "last_attempt": item.get("last_attempt"),
            "failure_count": int(item.get("failure_count", 0) or 0),
            "age_hours": age,
            "rules_declared": item.get("rules_declared", 0),
        }
    for source_id in sorted(set(lifecycles) - set(sources)):
        state = lifecycles[source_id]
        sources[source_id] = {
            "lifecycle": state,
            "status": "retired" if state in {"retired", "disabled"} else "failed",
            "reason": "source is in lifecycle registry but has no telemetry record",
            "last_success": None,
            "last_attempt": None,
            "failure_count": 0,
            "age_hours": None,
            "rules_declared": 0,
        }
    payload = {
        "schema": "source_health_status_v1",
        "generated_at": now.isoformat().replace("+00:00", "Z"),
        "policy": str(POLICY.relative_to(ROOT)),
        "lifecycle_registry": str(LIFECYCLE.relative_to(ROOT)),
        "sources": dict(sorted(sources.items())),
    }
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
