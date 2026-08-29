#!/usr/bin/env python3
"""Import official SVG: python scripts/icon_import_official.py --id wechat path/to.svg"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFF = ROOT / "assets" / "icons" / "official"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("svg", type=Path)
    args = ap.parse_args()
    if not args.svg.exists():
        print(f"missing {args.svg}")
        return 1
    OFF.mkdir(parents=True, exist_ok=True)
    dest = OFF / f"{args.id.lower()}.svg"
    shutil.copy2(args.svg, dest)
    print(f"copied → {dest}; run python scripts/icon_p2_apply.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
