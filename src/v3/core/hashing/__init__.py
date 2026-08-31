"""Stable hashing helpers."""
from __future__ import annotations
import hashlib

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_lines(lines: list[str]) -> str:
    return sha256_text("\n".join(sorted(lines)))
