#!/usr/bin/env python3
"""Validate service docs consume Icon V6 only (no Collection V4 paths)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FORBIDDEN = [
    "assets/icons/v4",
    "Icon Library V4",
    "/assets/icons/v4/",
]

def main() -> int:
    bad: list[str] = []
    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN:
            if token in text:
                bad.append(f"{path.relative_to(ROOT)}: contains {token!r}")
                break
    if bad:
        print("validate_icon_docs: FAIL")
        for line in bad[:50]:
            print(" ", line)
        if len(bad) > 50:
            print(f"  ... and {len(bad) - 50} more")
        return 1
    print("validate_icon_docs: OK (no V4 icon paths in docs/)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
