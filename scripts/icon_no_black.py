#!/usr/bin/env python3
"""No pure-black *delivery*: split source_color vs display_color. Never mutate source SVG."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "assets" / "icons" / "manifest.yaml"
COLORS = ROOT / "assets" / "icons" / "metadata" / "colors.yaml"

DISPLAY_PALETTE = {
    "apple": "86868B",
    "applemusic": "FA243C",
    "appletv": "A2AAAD",
    "github": "6E5494",
    "x": "1D9BF0",
    "twitter": "1D9BF0",
    "notion": "E1622F",
    "vercel": "0070F3",
    "steam": "66C0F4",
    "uber": "276EF1",
    "threads": "1D9BF0",
    "tidal": "00CED1",
    "hbo": "B100FF",
    "epic": "0078F2",
    "wikipedia": "636466",
    "tiktok": "FE2C55",
    "douyin": "FE2C55",
    "cursor": "7C3AED",
    "hashicorp": "7B42BC",
    "jetbrains": "FE2857",
    "ea": "FF4747",
    "ubisoft": "0070FF",
    "copilot": "6E5494",
    "google": "4285F4",
    "microsoft": "00A4EF",
}


def is_near_black(hexc: str | None) -> bool:
    if not hexc:
        return False
    h = str(hexc).lstrip("#").upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) < 6:
        return False
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return False
    return r + g + b < 80


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    si_colors = {}
    if COLORS.exists():
        doc = yaml.safe_load(COLORS.read_text(encoding="utf-8")) or {}
        for k, v in (doc.get("colors") or {}).items():
            if isinstance(v, dict) and v.get("hex"):
                si_colors[k] = str(v["hex"])

    n = 0
    for key, meta in list(icons.items()):
        if not isinstance(meta, dict):
            continue
        ns = str(meta.get("namespace") or meta.get("type") or "")
        if ns in ("policy", "dataset", "network"):
            continue

        brand = meta.setdefault("brand", {})
        src_c = brand.get("source_color") or si_colors.get(key) or (meta.get("source") or {}).get("color")
        if not src_c and brand.get("color") and brand.get("color_source") not in (
            "no-black-palette",
            "display-policy",
        ):
            src_c = brand.get("color")
        if key in DISPLAY_PALETTE and not src_c:
            src_c = "#000000"

        if isinstance(src_c, str) and not str(src_c).startswith("#") and len(str(src_c)) in (3, 6):
            src_c = "#" + src_c

        display = None
        policy = "identity"
        if key in DISPLAY_PALETTE:
            display = "#" + DISPLAY_PALETTE[key]
            policy = "lift-black" if key not in ("google", "microsoft") else "brand-accent"
        elif is_near_black(src_c):
            display = "#" + DISPLAY_PALETTE.get(key, "6366F1")
            policy = "lift-black"
        elif src_c:
            display = src_c if str(src_c).startswith("#") else f"#{src_c}"
            policy = "identity"

        if not display:
            continue

        brand["source_color"] = src_c if src_c else brand.get("source_color")
        brand["display_color"] = display
        brand["color_policy"] = policy
        brand["color"] = display
        brand["color_source"] = (
            "display-policy" if policy == "lift-black" else brand.get("color_source") or "simple-icons"
        )
        meta.setdefault("visual", {})["approved_mono"] = False
        meta["visual"]["color_mode"] = "color"
        icons[key] = meta
        n += 1

    man["icons"] = icons
    man["icon_policy"] = {
        "no_pure_black_delivery": True,
        "source_immutable": True,
        "note": "source SVG identity; display_color applied at render only",
    }
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[no_black] metadata_updated={n} (source SVG untouched)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
