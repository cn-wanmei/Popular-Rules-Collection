#!/usr/bin/env python3
"""Forbid legacy Collection icon paths in consumer-facing service docs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPES = [ROOT / "docs" / "services", ROOT / "docs" / "rules"]
FORBIDDEN = [
    "assets/icons/v3",
    "assets/icons/v4",
    "assets/icons/v5",
    "Icon Library V4",
    "Icon Library V3",
]

def main() -> int:
    bad: list[str] = []
    for scope in SCOPES:
        if not scope.exists():
            continue
        for path in scope.rglob("*.md"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in FORBIDDEN:
                if token in text:
                    bad.append(f"{path.relative_to(ROOT)}: {token!r}")
                    break
    if bad:
        print("validate_icon_docs: FAIL")
        for line in bad[:40]:
            print(" ", line)
        return 1
    print("validate_icon_docs: OK (docs/services + docs/rules)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
