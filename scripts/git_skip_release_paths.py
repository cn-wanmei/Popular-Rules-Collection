#!/usr/bin/env python3
"""Unstage release_globs after git add and restore worktree (V2.1).

Leaving modified-but-unstaged release paths dirty causes:
  error: cannot pull with rebase: You have unstaged changes.
"""
from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "config" / "artifact_layout.yaml"


def main() -> int:
    if not LAYOUT.exists():
        return 0
    globs = (yaml.safe_load(LAYOUT.read_text(encoding="utf-8")) or {}).get("release_globs") or []
    try:
        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True
        ).splitlines()
    except subprocess.CalledProcessError:
        staged = []

    drop = [p for p in staged if any(fnmatch.fnmatch(p, g) for g in globs)]
    if drop:
        subprocess.run(["git", "reset", "HEAD", "--"] + drop, cwd=ROOT, check=False)
        subprocess.run(["git", "restore", "--worktree", "--"] + drop, cwd=ROOT, check=False)
        print(f"[git_skip_release] unstaged+restored {len(drop)} paths")
    else:
        print("[git_skip_release] none staged")

    try:
        dirty = subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines()
    except subprocess.CalledProcessError:
        dirty = []
    dirty_drop = [p for p in dirty if any(fnmatch.fnmatch(p, g) for g in globs)]
    if dirty_drop:
        subprocess.run(["git", "restore", "--worktree", "--"] + dirty_drop, cwd=ROOT, check=False)
        print(f"[git_skip_release] restored dirty {len(dirty_drop)} paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
