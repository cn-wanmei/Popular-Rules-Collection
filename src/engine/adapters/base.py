"""Shared helpers for native adapters."""
from __future__ import annotations


def normalize_type(typ: str) -> str:
    """Normalize canonical IR rule types to native hyphenated names."""
    return str(typ).strip().upper().replace("_", "-")


def domain_line(typ: str, value: str) -> str:
    """Render a classical rule-provider line without a client policy."""
    return f"{normalize_type(typ)},{value}"
