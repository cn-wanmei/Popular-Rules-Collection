#!/usr/bin/env python3
"""size_gate — threshold from config/artifact_layout.yaml SSOT."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "config" / "artifact_layout.yaml"
SCAN = [ROOT / "database", ROOT / "generated", ROOT / "reports", ROOT / "backup"]


def threshold_mb(cli):
    if cli is not None:
        return cli
    if LAYOUT.exists():
        doc = yaml.safe_load(LAYOUT.read_text(encoding="utf-8")) or {}
        git = ((doc.get("policy") or {}).get("git") or {})
        if "max_tracked_tree_mb" in git:
            return float(git["max_tracked_tree_mb"])
        if "max_file_mb" in git:
            return max(90.0, float(git["max_file_mb"]) * 18)
    return 90.0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-mb", type=float, default=None)
    args = p.parse_args()
    max_mb = threshold_mb(args.max_mb)
    limit = int(max_mb * 1024 * 1024)
    bad = []
    for base in SCAN:
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if f.is_file() and f.stat().st_size > limit:
                bad.append((str(f.relative_to(ROOT)), f.stat().st_size))
    if bad:
        print(f"[size_gate] FAIL: {len(bad)} file(s) exceed {max_mb} MB (artifact_layout)")
        for path, size in sorted(bad, key=lambda x: -x[1]):
            print(f"  {size / (1024*1024):.2f} MB  {path}")
        return 1
    print(f"[size_gate] OK (threshold {max_mb} MB, SSOT=artifact_layout)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
