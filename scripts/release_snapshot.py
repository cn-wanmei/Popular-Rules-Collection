#!/usr/bin/env python3
"""release_snapshot.py — Phase 3A: auditable release record per pipeline run.

Writes:
  reports/<date>/release.json
  reports/latest_release.json

commit = pipeline_input SHA (before collect git commit). HEAD after push
contains this file and may differ by one commit — by design.
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
    sh_split = stats.get("source_health") or {}

    def _status_from_report(path: Path, fail_key: str = "failures") -> str:
        if not path.exists():
            return "unknown"
        try:
            rep = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return "unknown"
        if "status" in rep:
            return str(rep["status"])
        if fail_key in rep:
            return "fail" if rep.get(fail_key) else "pass"
        return "unknown"

    schema_st = _status_from_report(day / "schema_validate.json")
    validate_st = _status_from_report(day / "validation_report.json")
    builder_st = _status_from_report(day / "builder-validation.json", fail_key="failures")
    stats_val = stats.get("validation") or {}
    if schema_st == "unknown":
        schema_st = stats_val.get("schema_validate") or "unknown"
    if validate_st == "unknown":
        validate_st = stats_val.get("validate") or "unknown"
    if builder_st == "unknown":
        builder_st = stats_val.get("builder_validate") or "unknown"

    input_commit = git_head()

    release = {
        "schema_version": 2,
        "phase": "3A",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": args.date,
        "commit": input_commit,
        "commit_role": "pipeline_input",
        "commit_note": (
            "SHA observed when release_snapshot ran (before collect's git commit). "
            "HEAD after push is the commit that contains this file + generated artifacts."
        ),
        "source_status": {
            "health": health.get("sources") or sh_split.get("statuses") or {},
            "healthy_ratio": sh_split.get("healthy_ratio"),
            "configured_sources": sh_split.get("configured_sources"),
            "enabled_sources": sh_split.get("enabled_sources"),
            "collected_this_run": sh_split.get("collected_this_run"),
            "historical_in_health": sh_split.get("historical_in_health"),
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
        "validation": {
            "schema_validate": schema_st,
            "builder_validate": builder_st,
            "validate": validate_st,
            "builder_failures": stats_val.get("builder_failures"),
        },
        "quality": {
            "flags": (quality or {}).get("flags"),
            "shown": (quality or {}).get("shown"),
            "empty_generated": (quality or {}).get("empty_generated"),
            "large_sets": (quality or {}).get("large_sets"),
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
            "schema_validate": str((day / "schema_validate.json").relative_to(ROOT))
            if (day / "schema_validate.json").exists()
            else None,
            "validation_report": str((day / "validation_report.json").relative_to(ROOT))
            if (day / "validation_report.json").exists()
            else None,
        },
    }

    out = day / "release.json"
    out.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (REPORTS / "latest_release.json").write_text(
        json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"[release_snapshot] date={args.date} commit={release['commit'][:8]} "
        f"materialized={release['materialized_count']} domains={release['domain_count']} "
        f"schema={schema_st} validate={validate_st} builder={builder_st}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
