#!/usr/bin/env python3
"""Rebuild config/icons.yaml from assets/icons/manifest (Phase I binding SSOT)."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "assets" / "icons" / "manifest.yaml"
CFG = ROOT / "config" / "icons.yaml"

STRATEGY = {"direct", "proxy", "reject", "dns", "select", "match", "global"}
DATASET = {
    "china", "lan", "geoip", "geosite", "asn", "network", "private", "stun",
    "adblock", "gfw", "chinamobile", "chinaunicom", "chinatelecom", "provider", "cloud",
}
APPROVED_MONO = {
    "github", "apple", "x", "twitter", "notion", "uber", "threads", "vercel", "steam",
}


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    smap = man.get("service_icon_map") or {}
    entries = {}
    for sid, icon_id in sorted(smap.items()):
        icon_id = str(icon_id)
        meta = icons.get(icon_id) or {}
        if not isinstance(meta, dict):
            meta = {}
        itype = str(meta.get("type") or "")
        if icon_id == "placeholder":
            cat, status = "pending", "placeholder"
        elif icon_id in STRATEGY or itype == "policy":
            cat, status = "strategy", str(meta.get("status") or "verified")
        elif icon_id in DATASET or itype in ("dataset", "network"):
            cat, status = "dataset", str(meta.get("status") or "verified")
        else:
            cat, status = "brand", str(meta.get("status") or "sourced")
        src = meta.get("source") or {}
        brand = meta.get("brand") or {}
        visual = meta.get("visual") or {}
        entries[sid] = {
            "icon_id": icon_id,
            "category": cat,
            "status": status,
            "source": {
                "provider": src.get("provider"),
                "provenance": src.get("provenance"),
                "slug": src.get("slug"),
                "verified": bool(src.get("verified")),
            },
            "brand_color": brand.get("color") or visual.get("primary_color"),
            "variants": {
                "brand": cat == "brand",
                "mono": True,
                "dark": False,
                "light": False,
                "compact": False,
            },
            "approved_mono": icon_id in APPROVED_MONO,
        }
    doc = {
        "version": 1,
        "updated": str(date.today()),
        "description": "service_id → icon_id binding SSOT (binaries in assets/icons/)",
        "architecture": {
            "service_ne_icon_file": True,
            "categories": ["brand", "strategy", "dataset", "pending"],
        },
        "prohibitions": [
            "Service auto-search for logos",
            "Builder guessing logos",
            "favicon as permanent primary asset",
            "Unverified icons marked verified",
            "Black/white conversion overwriting official brand colors",
            "Mixing strategy icons with brand logos",
            "Dataset icons using corporate logos",
            "Fake icons solely for coverage metrics",
            "Embedding icons into sing-box rule JSON",
            "Storing icon binaries inside database/",
        ],
        "approved_mono_brands": sorted(APPROVED_MONO),
        "icons": entries,
    }
    CFG.parent.mkdir(parents=True, exist_ok=True)
    CFG.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[icon_config_sync] services={len(entries)} → {CFG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
