#!/usr/bin/env python3
"""Upgrade HOT placeholders via Simple Icons only (no guess, no CN invent)."""
from __future__ import annotations

import json
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
SRC = ICON / "source"
MAN = ICON / "manifest.yaml"

UPGRADE = {
    "amazon": "amazon",
    "aws": "amazonwebservices",
    "linkedin": "linkedin",
    "slack": "slack",
    "adobe": "adobe",
    "heroku": "heroku",
    "oracle": "oracle",
    "walmart": "walmart",
    "canva": "canva",
    "gitlab": "gitlab",
    "steam": "steam",
    "epic": "epicgames",
    "paypal": "paypal",
    "notion": "notion",
    "zoom": "zoom",
    "figma": "figma",
    "dropbox": "dropbox",
    "uber": "uber",
    "airbnb": "airbnb",
    "shopify": "shopify",
    "stripe": "stripe",
    "firebase": "firebase",
    "vercel": "vercel",
    "icloud": "icloud",
    "applemusic": "applemusic",
    "messenger": "messenger",
    "threads": "threads",
    "signal": "signal",
    "line": "line",
    "pinterest": "pinterest",
    "snapchat": "snapchat",
    "appletv": "appletv",
    "speedtest": "speedtest",
    "emby": "emby",
    "kakaotalk": "kakaotalk",
    "naver": "naver",
    "oppo": "oppo",
    "vivo": "vivo",
    "rockstar": "rockstargames",
    "nintendo": "nintendoswitch",
    "youtubemusic": "youtubemusic",
}


def fetch(url: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRC-hot-si"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = r.read()
        return d if len(d) > 40 else None
    except Exception:
        return None


def load_colors() -> dict:
    raw = fetch("https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/_data/simple-icons.json")
    out = {}
    if not raw:
        return out
    data = json.loads(raw.decode())
    for it in data.get("icons") or []:
        hx = (it.get("hex") or "").strip()
        if not hx:
            continue
        hx = "#" + hx.lstrip("#")
        title = "".join(c for c in (it.get("title") or "").lower() if c.isalnum())
        out[title] = hx
        if it.get("slug"):
            out[str(it["slug"]).lower()] = hx
    return out


def protected(meta: dict) -> bool:
    src = meta.get("source") or {}
    return str(src.get("provenance") or "") in ("official-colors", "project") or str(
        src.get("provider") or ""
    ) in ("project-brand", "project")


def main() -> int:
    SRC.mkdir(parents=True, exist_ok=True)
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.setdefault("icons", {})
    smap = man.setdefault("service_icon_map", {})
    colors = load_colors()
    ok = fail = skip = 0
    for sid, slug in sorted(UPGRADE.items()):
        meta = icons.get(sid) or {}
        if isinstance(meta, dict) and protected(meta):
            skip += 1
            smap[sid] = sid
            continue
        data = fetch(f"https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/{slug}.svg")
        if not data:
            fail += 1
            print(f"  FAIL {sid} {slug}")
            continue
        (SRC / f"{sid}.svg").write_bytes(data)
        hx = colors.get(slug)
        entry = {
            "name": sid.replace("_", " ").title(),
            "type": "service",
            "icon_key": sid,
            "source": {
                "provider": "simple-icons",
                "slug": slug,
                "provenance": "third_party",
                "verified": False,
                "url": f"https://simpleicons.org/?q={slug}",
            },
            "files": {
                "svg": f"source/{sid}.svg",
                "png": {
                    "64": f"png/64/{sid}.png",
                    "128": f"png/128/{sid}.png",
                    "256": f"png/256/{sid}.png",
                },
            },
            "status": "sourced",
            "license": {"type": "see-source", "note": "Simple Icons; brand trademarks apply."},
            "visual": {
                "style": "brand",
                "color_mode": "monochrome",
                "background": "transparent",
                "variants": ["monochrome"],
                "primary_color": hx,
            },
        }
        if hx:
            entry["brand"] = {"color": hx, "color_source": "simple-icons"}
            entry["source"]["color"] = hx
        icons[sid] = entry
        smap[sid] = sid
        if sid == "aws":
            smap["amazonaws"] = "aws"
        ok += 1
        print(f"  OK {sid} {hx}")
    man["icons"] = icons
    man["service_icon_map"] = smap
    man["updated"] = str(date.today())
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    ph = sum(1 for v in smap.values() if v == "placeholder")
    print(f"[icon_upgrade_hot_si] ok={ok} fail={fail} skip={skip} placeholder={ph}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
