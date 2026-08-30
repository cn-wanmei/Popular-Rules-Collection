#!/usr/bin/env python3
"""Remove redundant icon dirs (strategies/datasets/monochrome/official)."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "assets" / "icons"
DROP = ("strategies", "datasets", "monochrome", "official")


def main() -> int:
    removed = []
    for name in DROP:
        p = ROOT / name
        if p.exists():
            shutil.rmtree(p)
            removed.append(name)
            print(f"  removed {p}")
    print(f"[icon_cleanup] removed={removed or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
