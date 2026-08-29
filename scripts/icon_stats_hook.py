#!/usr/bin/env python3
"""Collect icon_coverage dict for statistics.py."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def collect_icon_coverage() -> dict:
    try:
        icon_man = ROOT / "assets" / "icons" / "manifest.yaml"
        icon_cfg = ROOT / "config" / "icons.yaml"
        im = yaml.safe_load(icon_man.read_text(encoding="utf-8")) if icon_man.exists() else {}
        ic = yaml.safe_load(icon_cfg.read_text(encoding="utf-8")) if icon_cfg.exists() else {}
        smap = im.get("service_icon_map") or {}
        icons = im.get("icons") or {}
        real = sum(1 for v in smap.values() if v and v != "placeholder")
        ph = sum(1 for v in smap.values() if v == "placeholder")
        verified = sum(1 for v in icons.values() if isinstance(v, dict) and v.get("status") == "verified")
        png256 = sum(1 for k in icons if (ROOT / "assets" / "icons" / "png" / "256" / f"{k}.png").exists())
        out = {
            "mapped_services": len(smap),
            "real_icons": real,
            "placeholder": ph,
            "verified": verified,
            "png256": png256,
        }
        if ic.get("icons"):
            out["config_bindings"] = len(ic["icons"])
        return out
    except Exception as e:
        return {"status": "error", "error": str(e)}
