"""Shared helpers for native adapters."""
from __future__ import annotations

from typing import Iterable


def domain_line(typ: str, value: str) -> str:
    t = typ.upper()
    if t in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6"):
        return f"{t},{value}"
    return f"{t},{value}"
