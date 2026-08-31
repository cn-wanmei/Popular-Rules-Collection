#!/usr/bin/env python3
"""Restore source/*.svg from Simple Icons (identity only, no fill mutation)."""
from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "icons" / "source"
UA = {"User-Agent": "Mozilla/5.0 PRC-Icons"}

SLUGS = {
    "google": "google",
    "microsoft": "microsoft",
    "apple": "apple",
    "github": "github",
    "x": "x",
    "twitter": "x",
    "notion": "notion",
    "vercel": "vercel",
    "steam": "steam",
    "uber": "uber",
    "threads": "threads",
    "tiktok": "tiktok",
    "douyin": "tiktok",
    "wikipedia": "wikipedia",
    "tidal": "tidal",
    "hbo": "hbo",
    "epic": "epicgames",
    "hashicorp": "hashicorp",
    "jetbrains": "jetbrains",
}


def fetch(slug: str):
    for ver in ("11.14.0", "9.21.0"):
        url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{ver}/icons/{slug}.svg"
        req = urllib.request.Request(url, headers=UA)
        try:
            return urllib.request.urlopen(req, timeout=15).read().decode()
        except Exception:
            continue
    return None


def main() -> int:
    n = 0
    for key, slug in sorted(SLUGS.items()):
        svg = fetch(slug)
        if not svg:
            print(f"  SKIP {key}")
            continue
        (SRC / f"{key}.svg").write_text(svg, encoding="utf-8")
        n += 1
    print(f"[restore_si_identity] restored={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
