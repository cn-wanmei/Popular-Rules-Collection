#!/usr/bin/env python3
"""size_gate — thresholds from config/artifact_layout.yaml SSOT.

Semantics (clarified 2026-10-08 audit):
  policy.git.max_file_mb          → max single file under SCAN roots
  policy.git.max_tracked_tree_mb  → soft budget for sum of SCAN roots (warn/fail)
  policy.release.max_bundle_mb    → release channel (not enforced here)

Production DAG should invoke this script (build.yml Size Gate step).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "config" / "artifact_layout.yaml"
SCAN = [ROOT / "database", ROOT / "generated", ROOT / "reports", ROOT / "backup"]


def load_limits(cli_file: float | None, cli_tree: float | None) -> tuple[float, float]:
    max_file = 5.0
    max_tree = 90.0
    if LAYOUT.exists():
        doc = yaml.safe_load(LAYOUT.read_text(encoding="utf-8")) or {}
        git = ((doc.get("policy") or {}).get("git") or {})
        if "max_file_mb" in git:
            max_file = float(git["max_file_mb"])
        if "max_tracked_tree_mb" in git:
            max_tree = float(git["max_tracked_tree_mb"])
    if cli_file is not None:
        max_file = float(cli_file)
    if cli_tree is not None:
        max_tree = float(cli_tree)
    return max_file, max_tree


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-file-mb", type=float, default=None)
    p.add_argument("--max-tree-mb", type=float, default=None)
    p.add_argument("--max-mb", type=float, default=None, help="legacy alias for --max-file-mb")
    args = p.parse_args()
    if args.max_mb is not None and args.max_file_mb is None:
        args.max_file_mb = args.max_mb
    max_file_mb, max_tree_mb = load_limits(args.max_file_mb, args.max_tree_mb)
    file_limit = int(max_file_mb * 1024 * 1024)
    tree_limit = int(max_tree_mb * 1024 * 1024)

    bad_files = []
    total = 0
    for base in SCAN:
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if not f.is_file():
                continue
            size = f.stat().st_size
            total += size
            if size > file_limit:
                bad_files.append((str(f.relative_to(ROOT)), size))

    rc = 0
    if bad_files:
        print(f"[size_gate] FAIL: {len(bad_files)} file(s) exceed max_file_mb={max_file_mb}")
        for path, size in sorted(bad_files, key=lambda x: -x[1])[:30]:
            print(f"  {size / (1024*1024):.2f} MB  {path}")
        rc = 1
    tree_mb = total / (1024 * 1024)
    if total > tree_limit:
        print(
            f"[size_gate] FAIL: SCAN tree sum {tree_mb:.1f} MB exceeds max_tracked_tree_mb={max_tree_mb}"
        )
        rc = 1
    else:
        print(f"[size_gate] tree_sum={tree_mb:.1f} MB <= {max_tree_mb} MB")
    if rc == 0:
        print(
            f"[size_gate] OK (max_file_mb={max_file_mb}, max_tracked_tree_mb={max_tree_mb}, SSOT=artifact_layout)"
        )
    return rc


if __name__ == "__main__":
    sys.exit(main())
