#!/usr/bin/env python3
"""Fail when production-facing files reintroduce retired V2 migration paths."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SCAN_ROOTS = ["scripts", "src", "tests", ".github"]
BANNED = (
    "legacy/migration/",
    "legacy\\migration\\",
    "scripts/normalize.py",
    "scripts/deduplicate.py",
    "scripts/v2fly_parser.py",
)


def main() -> int:
    violations: list[str] = []
    for entry in SCAN_ROOTS:
        path = ROOT / entry
        if not path.exists():
            continue
        for file in path.rglob("*"):
            if not file.is_file() or file.resolve() == SELF:
                continue
            try:
                text = file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            rel = file.relative_to(ROOT).as_posix()
            for token in BANNED:
                if token in text:
                    violations.append(f"{rel}: {token}")
    if violations:
        print("Legacy Reference Gate: FAILED")
        print("\n".join(sorted(set(violations))))
        return 1
    print("Legacy Reference Gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
