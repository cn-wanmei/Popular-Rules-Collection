#!/usr/bin/env python3
"""Optical weight overrides loader for icon_engine normalize scale."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OPTICAL = ROOT / "assets" / "icons" / "metadata" / "optical_overrides.yaml"


def load_optical() -> dict:
    if not OPTICAL.exists():
        return {}
    doc = yaml.safe_load(OPTICAL.read_text(encoding="utf-8")) or {}
    return doc.get("overrides") or {}


def scale_for(key: str, overrides: dict | None = None) -> float:
    overrides = overrides if overrides is not None else load_optical()
    ent = overrides.get(key) or {}
    try:
        s = float(ent.get("scale") or 1.0)
    except (TypeError, ValueError):
        s = 1.0
    return max(0.7, min(1.2, s))
