#!/usr/bin/env python3
"""release_snapshot.py — Phase 3A: auditable release record per pipeline run.

Writes:
  reports/<date>/release.json
  reports/latest_release.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def git_head() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


def load_json(p: Path) -> dict:
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)

    stats = load_json(day / "statistics.json") or load_json(day / "summary.json")
    drift = load_json(day / "rule_count_drift.json")
    counts = load_json(day / "rule_counts.json")
    identity = load_json(day / "identity_report.json")
    quality = load_json(day / "quality_report.json")
    source_snap = load_json(day / "source_snapshot.json")

    health = {}
    health_path = ROOT / "sources" / "health.yaml"
    if health_path.exists():
        try:
            import yaml

            health = yaml.safe_load(health_path.read_text(encoding="utf-8")) or {}
        except Exception:
            pass

    sc = stats.get("service_coverage") or {}
    rc = stats.get("rule_coverage") or {}
    bc = stats.get("builder_coverage") or {}
    sh = stats.get("source_health") or {}

    release = {
        "schema_version": 1,
        "phase": "3A",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": args.date,
        "commit": git_head(),
        "source_status": {
            "health": health.get("sources") or sh.get("statuses") or {},
            "healthy_ratio": sh.get("healthy_ratio"),
            "enabled_sources": sh.get("enabled_sources"),
            "snapshot": source_snap or None,
        },
        "service_count": sc.get("registered"),
        "materialized_count": sc.get("materialized"),
        "intentional_unmaterialized": sc.get("intentional_unmaterialized"),
        "domain_count": rc.get("domains") or stats.get("domains"),
        "ip_count": rc.get("ips") or stats.get("cidr"),
        "builder_count": len(
            [k for k, v in bc.items() if (v or {}).get("status") == "ok"]
        ),
        "builder_coverage": bc,
        "validation": stats.get("validation") or {},
        "quality": {
            "flags": (quality or {}).get("flags"),
            "shown": (quality or {}).get("shown"),
        },
        "drift": {
            "warn": len((drift or {}).get("warn") or []),
            "high": len((drift or {}).get("high") or []),
            "review": len((drift or {}).get("review") or []),
            "baseline_compared": (drift or {}).get("baseline_compared"),
        },
        "identity": {
            "checked": (identity or {}).get("checked"),
            "warnings": len((identity or {}).get("warnings") or []),
        },
        "rule_counts_total": (counts or {}).get("total_rules"),
        "artifacts": {
            "statistics": str((day / "statistics.json").relative_to(ROOT))
            if (day / "statistics.json").exists()
            else None,
            "rule_counts": str((day / "rule_counts.json").relative_to(ROOT))
            if (day / "rule_counts.json").exists()
            else None,
            "manifest": "generated/manifest.json",
        },
    }

    out = day / "release.json"
    out.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (REPORTS / "latest_release.json").write_text(
        json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"[release_snapshot] date={args.date} commit={release['commit'][:8]} "
        f"materialized={release['materialized_count']} domains={release['domain_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
