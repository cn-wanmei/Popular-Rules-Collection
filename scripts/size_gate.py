#!/usr/bin/env python3
"""size_gate.py — fail CI if any tracked artifact exceeds safety threshold (default 90MB)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = [
    ROOT / "database",
    ROOT / "generated",
    ROOT / "reports",
    ROOT / "backup",
]
SKIP_SUFFIX = {".git"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-mb", type=float, default=90.0)
    args = p.parse_args()
    limit = int(args.max_mb * 1024 * 1024)
    bad: list[tuple[str, int]] = []
    for base in SCAN:
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if not f.is_file():
                continue
            if f.name == "domains.jsonl" and "provenance" in str(f):
                pass
            size = f.stat().st_size
            if size > limit:
                bad.append((str(f.relative_to(ROOT)), size))
    if bad:
        print(f"[size_gate] FAIL: {len(bad)} file(s) exceed {args.max_mb} MB")
        for path, size in sorted(bad, key=lambda x: -x[1]):
            print(f"  {size / (1024*1024):.2f} MB  {path}")
        print("Suggestion: shard or exclude from git; do not use Git LFS for rule indexes.")
        return 1
    print(f"[size_gate] OK (threshold {args.max_mb} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
