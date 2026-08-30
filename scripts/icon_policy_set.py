#!/usr/bin/env python3
"""PRC policy/strategy geometric icons — filled full-color."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "icons" / "source"
MAN = ROOT / "assets" / "icons" / "manifest.yaml"

ICONS = {
    "direct": ("#22C55E", '<path d="M3 11h11.5l-3.2-3.2 1.4-1.4L19 12l-6.3 5.6-1.4-1.4 3.2-3.2H3v-2z"/><path d="M20 6v12h2V6h-2z"/>'),
    "proxy": ("#3B82F6", '<rect x="2" y="7" width="8" height="10" rx="2"/><rect x="14" y="7" width="8" height="10" rx="2"/><rect x="10" y="11" width="4" height="2" rx="0.5"/>'),
    "reject": ("#EF4444", '<circle cx="12" cy="12" r="9"/><rect x="6" y="11" width="12" height="2" rx="1" fill="#fff"/>'),
    "select": ("#F59E0B", '<path d="M6 9l6 7 6-7H6z"/>'),
    "auto": ("#8B5CF6", '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1" stroke="#8B5CF6" stroke-width="1.75" fill="none"/>'),
    "urltest": ("#A855F7", '<path d="M2 12h3l2.5-7 4 14 3-7H22v-2h-6l-2.2 5.1L9.5 4 6.2 12H2z"/>'),
    "fallback": ("#7C3AED", '<path d="M4 8h9V5l6 5-6 5v-3H4V8z"/><path d="M20 16H11v3l-6-5 6-5v3h9v4z" opacity="0.9"/>'),
    "loadbalance": ("#6366F1", '<rect x="3" y="4" width="4" height="16" rx="1"/><rect x="10" y="8" width="4" height="12" rx="1"/><rect x="17" y="12" width="4" height="8" rx="1"/>'),
    "match": ("#14B8A6", '<path d="M4 12.5l5.5 5.5L20 6.5l-1.5-1.5-9 9.5-4-4L4 12.5z"/>'),
    "final": ("#64748B", '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="8" y="8" width="8" height="8" rx="1" fill="#fff"/>'),
    "dns": ("#06B6D4", '<path d="M12 2l9 4.5v6c0 5-3.6 8.7-9 10-5.4-1.3-9-5-9-10v-6L12 2z"/><circle cx="12" cy="12" r="3.5" fill="#fff"/>'),
    "adblock": ("#F97316", '<path d="M12 2l9 3.5v6.5c0 4.5-3.4 8.2-9 9.5-5.6-1.3-9-5-9-9.5V5.5L12 2z"/><path d="M8 12.5l2.8 2.8 5.5-5.5-1.4-1.4-4.1 4.1-1.4-1.4L8 12.5z" fill="#fff"/>'),
    "global": ("#0EA5E9", '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9" fill="none" stroke="#fff" stroke-width="1.5"/><path d="M3 12h18" stroke="#fff" stroke-width="1.5"/>'),
    "gfw": ("#DC2626", '<path d="M3 6h18v3H3V6zm0 5h18v3H3v-3zm0 5h18v3H3v-3z"/><path d="M8 4v16M16 4v16" stroke="#fff" stroke-width="1.5"/>'),
    "lan": ("#10B981", '<rect x="2" y="15" width="5" height="5" rx="1"/><rect x="9.5" y="10" width="5" height="10" rx="1"/><rect x="17" y="5" width="5" height="15" rx="1"/>'),
    "private": ("#64748B", '<path d="M8 10V8a4 4 0 118 0v2h2a1 1 0 011 1v9a1 1 0 01-1 1H6a1 1 0 01-1-1v-9a1 1 0 011-1h2zm2 0h4V8a2 2 0 10-4 0v2z"/>'),
    "network": ("#3B82F6", '<circle cx="5" cy="8" r="2.5"/><circle cx="19" cy="8" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7 9.5l8-1.5M17 10l-3.5 5.5M7.5 10l3.5 5.5" stroke="#3B82F6" stroke-width="1.5" fill="none"/>'),
    "stun": ("#8B5CF6", '<path d="M12 2l2.8 6.5L22 9.2l-5 4.6 1.5 7.2L12 17.5 5.5 21l1.5-7.2-5-4.6 7.2-.7L12 2z"/>'),
    "cloud": ("#38BDF8", '<path d="M7 18h11a4 4 0 000-8 5.5 5.5 0 00-10.7-1.8A3.5 3.5 0 007 18z"/>'),
    "provider": ("#0EA5E9", '<rect x="3" y="5" width="18" height="5" rx="1"/><rect x="3" y="12" width="18" height="7" rx="1"/><rect x="6" y="14.5" width="3" height="2" rx="0.3" fill="#fff"/><rect x="11" y="14.5" width="3" height="2" rx="0.3" fill="#fff"/>'),
    "asn": ("#6366F1", '<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><rect x="14" y="14" width="6" height="6" rx="1"/>'),
    "geoip": ("#14B8A6", '<path d="M12 2c-4 0-7 3-7 7 0 5.5 7 13 7 13s7-7.5 7-13c0-4-3-7-7-7zm0 4.5a2.5 2.5 0 110 5 2.5 2.5 0 010-5z"/>'),
    "geosite": ("#0D9488", '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9" fill="none" stroke="#fff" stroke-width="1.4"/><path d="M3 12h18" stroke="#fff" stroke-width="1.4"/>'),
    "placeholder": ("#94A3B8", '<circle cx="12" cy="12" r="9"/><rect x="11" y="7" width="2" height="6" rx="1" fill="#fff"/><circle cx="12" cy="17" r="1.2" fill="#fff"/>'),
}

POLICY_NS = {
    "direct", "proxy", "reject", "select", "auto", "urltest", "fallback",
    "loadbalance", "match", "final", "dns", "global", "placeholder",
}


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    smap = man.get("service_icon_map") or {}
    for key, (color, body) in ICONS.items():
        svg = (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">\n'
            f"{body}\n</svg>\n"
        )
        (SRC / f"{key}.svg").write_text(svg, encoding="utf-8")
        ns = "policy" if key in POLICY_NS else "dataset"
        meta = icons.get(key) or {}
        meta.update(
            {
                "name": key.title().replace("Urltest", "URLTest").replace("Adblock", "AdBlock"),
                "type": "policy" if ns == "policy" else meta.get("type") or "dataset",
                "namespace": ns if key in POLICY_NS else meta.get("namespace") or "dataset",
                "icon_key": key,
                "source": {"provider": "project", "type": "geometric", "provenance": "project", "verified": True},
                "files": {
                    "svg": f"source/{key}.svg",
                    "png": {"64": f"png/64/{key}.png", "128": f"png/128/{key}.png", "256": f"png/256/{key}.png"},
                },
                "license": {"type": "CC0-1.0", "note": "PRC policy geometric", "reviewed": True},
                "status": "verified",
                "brand": {"color": color, "color_source": "policy-palette"},
                "visual": {"style": "geometric", "color_mode": "color", "background": "transparent"},
                "identity": {"verified": True, "icon_id": key},
            }
        )
        icons[key] = meta
        smap[key] = key
    man["icons"] = icons
    man["service_icon_map"] = smap
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[policy_set] icons={len(ICONS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
