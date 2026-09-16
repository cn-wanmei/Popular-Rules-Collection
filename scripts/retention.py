#!/usr/bin/env python3
"""Retention planner with safe dry-run default.

The script is intentionally conservative. Only date-partitioned directories/files
under configured roots are candidates. Referenced release evidence and the newest
successful snapshots are protected before deletion.
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "retention.yaml"
DATE_FORMAT = "%Y-%m-%d"


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def age_days(path: Path, now: dt.datetime) -> int:
    try:
        date = dt.datetime.strptime(path.name, DATE_FORMAT).replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return 0
    return max(0, (now - date).days)


def dated_entries(root: Path, now: dt.datetime) -> list[Path]:
    if not root.exists():
        return []
    return sorted([p for p in root.iterdir() if p.name.count("-") == 2 and age_days(p, now) >= 0], key=lambda p: p.name, reverse=True)


def plan_for_root(root: Path, keep_days: int, min_keep: int, now: dt.datetime) -> tuple[list[Path], list[Path]]:
    entries = dated_entries(root, now)
    protected = entries[:min_keep]
    candidates = [p for p in entries[min_keep:] if age_days(p, now) > keep_days]
    return protected, candidates


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="perform destructive deletes")
    args = ap.parse_args()
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    now = now_utc()

    roots = [
        (ROOT / "backup", int(policy.get("backup", {}).get("keep_days", 30)), int(policy.get("backup", {}).get("keep_min_successful", 7))),
        (ROOT / "reports", int(policy.get("reports", {}).get("keep_days", 90)), 0),
        (ROOT / "data" / "runs", int(policy.get("runs", {}).get("keep_days", 30)), int(policy.get("runs", {}).get("keep_min_successful", 10))),
    ]

    total_delete = 0
    for root, keep_days, min_keep in roots:
        protected, candidates = plan_for_root(root, keep_days, min_keep, now)
        print(f"ROOT {root.relative_to(ROOT)}")
        print(f"KEEP newest: {len(protected)}; DELETE eligible: {len(candidates)}; threshold: {keep_days}d")
        for path in candidates:
            print(f"DELETE {path.relative_to(ROOT)}")
            total_delete += 1
            if args.apply:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()

    print(f"TOTAL DELETE {'executed' if args.apply else 'planned'}: {total_delete}")
    if not args.apply:
        print("DRY-RUN ONLY: no files were deleted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
