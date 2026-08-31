#!/usr/bin/env python3
"""Unstage release_globs after git add (V2.1 transition)."""
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
        staged = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).splitlines()
    except subprocess.CalledProcessError:
        return 0
    drop = [p for p in staged if any(fnmatch.fnmatch(p, g) for g in globs)]
    if not drop:
        print("[git_skip_release] none")
        return 0
    subprocess.run(["git", "reset", "HEAD", "--"] + drop, cwd=ROOT, check=False)
    print(f"[git_skip_release] unstaged {len(drop)} paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
