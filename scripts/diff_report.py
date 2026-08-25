#!/usr/bin/env python3
"""diff_report.py — Generate daily added / removed / changed / conflicts reports"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    day = REPORTS / args.date
    for sub in ("added", "removed", "changed", "conflicts", "sources"):
        (day / sub).mkdir(parents=True, exist_ok=True)
    summary = day / "summary.md"
    summary.write_text(
        f"# Diff Report — {args.date}\n\nSee conflicts/summary.md after deduplicate.py\n",
        encoding="utf-8",
    )
    print(f"[diff] wrote {summary}")


if __name__ == "__main__":
    main()
