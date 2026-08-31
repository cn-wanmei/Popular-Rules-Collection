#!/usr/bin/env python3
"""V2.2 Content validation for fetched blobs."""
from __future__ import annotations

from pathlib import Path


def validate_bytes(data: bytes, name: str = "") -> list[str]:
    reasons: list[str] = []
    if not data:
        return ["empty"]
    if len(data) < 16:
        reasons.append("too_small")
    low = data[:64].lstrip().lower()
    if low.startswith(b"<!doctype html") or low.startswith(b"<html") or b"<html" in data[:500].lower():
        reasons.append("html_document")
    if b"Access Denied" in data[:1000] or b"access denied" in data[:1000]:
        reasons.append("access_denied")
    if data.count(b"\x00") > max(10, len(data) // 100):
        reasons.append("binary_nulls")
    return reasons


def validate_file(path: Path) -> list[str]:
    try:
        data = path.read_bytes()[:2_000_000]
    except OSError as e:
        return [f"read_error:{e}"]
    return validate_bytes(data, path.name)
