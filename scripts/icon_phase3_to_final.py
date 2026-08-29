#!/usr/bin/env python3
"""Phase III–V: unified strategy/dataset geometry; variant roles; no brand invent."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
SRC = ICON / "source"
MAN = ICON / "manifest.yaml"

STRATEGY = {
    "direct": ("#22C55E", "D", "Direct"),
    "proxy": ("#3B82F6", "P", "Proxy"),
    "reject": ("#EF4444", "R", "Reject"),
    "dns": ("#A855F7", "N", "DNS"),
    "global": ("#0EA5E9", "G", "Global"),
    "select": ("#F59E0B", "S", "Select"),
    "match": ("#14B8A6", "M", "Match"),
    "placeholder": ("#94A3B8", "?", "Placeholder"),
}
DATASET = {
    "china": ("#EAB308", "CN", "China"),
    "lan": ("#64748B", "L", "LAN"),
    "geoip": ("#14B8A6", "IP", "GeoIP"),
    "geosite": ("#6366F1", "GS", "GeoSite"),
    "asn": ("#F472B6", "AS", "ASN"),
    "network": ("#94A3B8", "NW", "Network"),
    "private": ("#64748B", "PR", "Private"),
    "stun": ("#6366F1", "ST", "STUN"),
    "adblock": ("#EF4444", "AD", "AdBlock"),
    "gfw": ("#64748B", "FW", "GFW"),
    "chinamobile": ("#0066CC", "CM", "China Mobile"),
    "chinaunicom": ("#E60027", "CU", "China Unicom"),
    "chinatelecom": ("#003399", "CT", "China Telecom"),
    "provider": ("#0EA5E9", "PV", "Provider"),
    "cloud": ("#38BDF8", "CL", "Cloud"),
}


def geometric(title: str, color: str, glyph: str) -> str:
    g = glyph[:2]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img">
  <title>{title}</title>
  <rect x="2" y="2" width="20" height="20" rx="5" fill="{color}" fill-opacity="0.15"/>
  <rect x="2" y="2" width="20" height="20" rx="5" fill="none" stroke="{color}" stroke-width="1.4"/>
  <circle cx="12" cy="12" r="5.2" fill="none" stroke="{color}" stroke-width="1.3"/>
  <text x="12" y="12.5" text-anchor="middle" dominant-baseline="middle"
        font-family="system-ui,sans-serif" font-size="{10 if len(g)==1 else 7.5}" font-weight="700"
        fill="{color}">{g}</text>
</svg>
'''


def files(key: str) -> dict:
    return {
        "svg": f"source/{key}.svg",
        "png": {"64": f"png/64/{key}.png", "128": f"png/128/{key}.png", "256": f"png/256/{key}.png"},
    }


def write_set(mapping, itype, icons, smap):
    n = 0
    SRC.mkdir(parents=True, exist_ok=True)
    for key, (color, glyph, title) in mapping.items():
        (SRC / f"{key}.svg").write_text(geometric(title, color, glyph), encoding="utf-8")
        icons[key] = {
            "name": title,
            "type": itype,
            "icon_key": key,
            "source": {
                "provider": "project",
                "provenance": "project",
                "method": "geometric-unified",
                "verified": True,
                "phase": "III",
            },
            "files": files(key),
            "license": {"type": "CC0-1.0", "note": "Project geometric mark"},
            "status": "verified",
            "visual": {
                "style": "geometric",
                "color_mode": "color",
                "background": "transparent",
                "variants": ["brand", "mono"],
                "primary_color": color,
                "design_system": "phase3-unified",
            },
            "brand": {"color": color, "color_source": "project"},
        }
        smap[key] = key
        n += 1
    return n


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.setdefault("icons", {})
    smap = man.setdefault("service_icon_map", {})
    n_s = write_set(STRATEGY, "policy", icons, smap)
    n_d = write_set(DATASET, "dataset", icons, smap)
    man["icons"] = icons
    man["service_icon_map"] = smap
    man["updated"] = str(date.today())
    man["phase_iii_v"] = {
        "strategy": n_s,
        "dataset": n_d,
        "variants": {
            "brand": "default",
            "mono": "monochrome/{size}/",
            "compact": "png/64",
            "dark": "deferred",
            "light": "deferred",
        },
    }
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[phase3-final] strategy={n_s} dataset={n_d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
