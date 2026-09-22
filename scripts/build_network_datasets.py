#!/usr/bin/env python3
"""Compatibility entry point for the unified Network Dataset builder.

The production implementation lives in :mod:`scripts.build_network_bundle`.
These helpers remain as a narrow compatibility surface for legacy callers and
tests; they do not create a second production output path.
"""
from __future__ import annotations

from pathlib import Path

from scripts.build_network_bundle import main


def _read_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _write(path: Path, lines: list[str]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(lines)


def domain_to_clash(src: Path, dest: Path) -> int:
    """Legacy-compatible DOMAIN-SUFFIX formatter.

    Production generation is still performed by build_network_bundle.py.
    """
    return _write(dest, [f"DOMAIN-SUFFIX,{line.lstrip('.')}" for line in _read_lines(src)])


def cidr_to_clash(src: Path, dest: Path) -> int:
    """Legacy-compatible IPv4/IPv6 CIDR formatter."""
    def format_cidr(value: str) -> str:
        host = value.split("/", 1)[0]
        return f"IP-CIDR6,{value}" if ":" in host else f"IP-CIDR,{value}"

    return _write(dest, [format_cidr(line) for line in _read_lines(src)])


if __name__ == "__main__":
    raise SystemExit(main())
