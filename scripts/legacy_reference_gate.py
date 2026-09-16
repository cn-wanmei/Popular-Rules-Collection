#!/usr/bin/env python3
"""Fail when production-facing files reintroduce retired V2 migration paths."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SCAN_ROOTS = ["scripts", "src", "tests", ".github", "docs", "PUBLISH_STATUS.md", "README.md"]
BANNED = (
    "legacy/migration/",
    "legacy\\migration\\",
    "scripts/normalize.py",
    "scripts/deduplicate.py",
    "scripts/v2fly_parser.py",
)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    violations: list[str] = []
    for entry in SCAN_ROOTS:
        path = ROOT / entry
        paths = [path] if path.is_file() else ([p for p in path.rglob("*") if p.is_file()] if path.exists() else [])
        for file in paths:
            if file.resolve() == SELF:
                continue
            rel = file.relative_to(ROOT).as_posix()
            try:
                text = file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
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
