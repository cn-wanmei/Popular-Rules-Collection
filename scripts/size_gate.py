#!/usr/bin/env python3
"""size_gate — enforce active build and archival budgets from artifact_layout.yaml.

The active build budget covers database/generated/reports. Historical backup
snapshots are archival inputs with their own budget; counting every retained
daily snapshot against the active build budget conflates reproducibility evidence
with the current production build footprint.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "config" / "artifact_layout.yaml"
ACTIVE_SCAN = [ROOT / "database", ROOT / "generated", ROOT / "reports"]
ARCHIVE_SCAN = [ROOT / "backup"]


def load_limits(
    cli_file: float | None,
    cli_tree: float | None,
    cli_archive: float | None,
) -> tuple[float, float, float]:
    max_file = 5.0
    max_tree = 90.0
    max_archive = 16384.0
    if LAYOUT.exists():
        doc = yaml.safe_load(LAYOUT.read_text(encoding="utf-8")) or {}
        git = ((doc.get("policy") or {}).get("git") or {})
        if "max_file_mb" in git:
            max_file = float(git["max_file_mb"])
        if "max_tracked_tree_mb" in git:
            max_tree = float(git["max_tracked_tree_mb"])
        if "max_backup_archive_mb" in git:
            max_archive = float(git["max_backup_archive_mb"])
    if cli_file is not None:
        max_file = float(cli_file)
    if cli_tree is not None:
        max_tree = float(cli_tree)
    if cli_archive is not None:
        max_archive = float(cli_archive)
    return max_file, max_tree, max_archive


def measure_roots(
    roots: list[Path], file_limit: int | None = None
) -> tuple[int, list[tuple[Path, int]]]:
    total = 0
    oversized: list[tuple[Path, int]] = []
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            size = path.stat().st_size
            total += size
            if file_limit is not None and size > file_limit:
                oversized.append((path, size))
    return total, oversized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-file-mb", type=float, default=None)
    parser.add_argument("--max-tree-mb", type=float, default=None)
    parser.add_argument("--max-backup-archive-mb", type=float, default=None)
    parser.add_argument("--max-mb", type=float, default=None, help="legacy alias for --max-file-mb")
    args = parser.parse_args()
    if args.max_mb is not None and args.max_file_mb is None:
        args.max_file_mb = args.max_mb

    max_file_mb, max_tree_mb, max_archive_mb = load_limits(
        args.max_file_mb, args.max_tree_mb, args.max_backup_archive_mb
    )
    file_limit = int(max_file_mb * 1024 * 1024)
    tree_limit = int(max_tree_mb * 1024 * 1024)
    archive_limit = int(max_archive_mb * 1024 * 1024)

    active_total, active_bad = measure_roots(ACTIVE_SCAN, file_limit)
    archive_total, archive_bad = measure_roots(ARCHIVE_SCAN, file_limit)
    all_bad_files = active_bad + archive_bad

    rc = 0
    if all_bad_files:
        print(f"[size_gate] FAIL: {len(all_bad_files)} file(s) exceed max_file_mb={max_file_mb}")
        for path, size in sorted(all_bad_files, key=lambda item: -item[1])[:30]:
            print(f"  {size / (1024 * 1024):.2f} MB  {path.relative_to(ROOT)}")
        rc = 1

    active_mb = active_total / (1024 * 1024)
    archive_mb = archive_total / (1024 * 1024)
    if active_total > tree_limit:
        print(
            f"[size_gate] FAIL: active build tree sum {active_mb:.1f} MB "
            f"exceeds max_tracked_tree_mb={max_tree_mb}"
        )
        rc = 1
    else:
        print(f"[size_gate] active_tree_sum={active_mb:.1f} MB <= {max_tree_mb} MB")

    if archive_total > archive_limit:
        print(
            f"[size_gate] FAIL: backup archive sum {archive_mb:.1f} MB "
            f"exceeds max_backup_archive_mb={max_archive_mb}"
        )
        rc = 1
    else:
        print(f"[size_gate] backup_archive_sum={archive_mb:.1f} MB <= {max_archive_mb} MB")

    if rc == 0:
        print(
            f"[size_gate] OK (max_file_mb={max_file_mb}, "
            f"max_tracked_tree_mb={max_tree_mb}, "
            f"max_backup_archive_mb={max_archive_mb}, SSOT=artifact_layout)"
        )
    return rc


if __name__ == "__main__":
    sys.exit(main())
