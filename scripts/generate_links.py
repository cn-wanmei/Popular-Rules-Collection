#!/usr/bin/env python3
"""generate_links.py — Produce subscription link tables for README"""

from __future__ import annotations

REPO = "cn-wanmei/Popular-Rules-Collection"
BRANCH = "main"


def raw(path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}"


def jsdelivr(path: str) -> str:
    return f"https://cdn.jsdelivr.net/gh/{REPO}@{BRANCH}/{path}"


def main() -> None:
    print("Primary (GitHub Raw):")
    print("  ", raw("generated/mihomo/google.yaml"))
    print("Mirrors:")
    print("  jsDelivr:", jsdelivr("generated/mihomo/google.yaml"))


if __name__ == "__main__":
    main()
