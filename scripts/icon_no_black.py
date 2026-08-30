#!/usr/bin/env python3
"""Repo policy: no pure-black brand icons."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "icons" / "source"
MAN = ROOT / "assets" / "icons" / "manifest.yaml"

PALETTE = {
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
}


def lift(hexc: str) -> str:
    h = hexc.lstrip("#").upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) < 6:
        return "6366F1"
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if r + g + b < 80:
        return "6366F1"
    return h


def force_fill(svg: str, hex_color: str) -> str:
    c = "#" + hex_color.lstrip("#")
    fills = re.findall(r'fill="(#[0-9A-Fa-f]{3,8})"', svg)
    distinct = set()
    for f in fills:
        fh = f[1:].upper()
        if len(fh) == 3:
            fh = "".join(x * 2 for x in fh)
        if len(fh) >= 6:
            rr, gg, bb = int(fh[0:2], 16), int(fh[2:4], 16), int(fh[4:6], 16)
            if rr + gg + bb >= 80 and fh != "FFFFFF":
                distinct.add(fh)
    if len(distinct) >= 2:
        return svg
    out = re.sub(r'\sfill="[^"]*"', "", svg)
    out = re.sub(r"\sfill='[^']*'", "", out)
    out = re.sub(r"<svg\b", f'<svg fill="{c}"', out, count=1)
    for tag in ("path", "circle", "polygon", "rect"):
        out = re.sub(rf"<{tag}\b", f'<{tag} fill="{c}"', out)
    out = re.sub(r'stroke="#[0-9a-fA-F]{3,8}"', f'stroke="{c}"', out)
    return out


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    n = 0
    for key, meta in list(icons.items()):
        if not isinstance(meta, dict):
            continue
        svg_path = SRC / f"{key}.svg"
        if not svg_path.exists():
            continue
        ns = str(meta.get("namespace") or meta.get("type") or "")
        if ns in ("policy", "dataset", "network") and key not in PALETTE:
            continue
        bc = (meta.get("brand") or {}).get("color") or (meta.get("source") or {}).get("color")
        if key in PALETTE:
            hexc = PALETTE[key]
        elif isinstance(bc, str):
            hexc = lift(bc)
            h = bc.lstrip("#")
            if len(h) >= 6:
                r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                if r + g + b >= 80:
                    continue
        else:
            continue
        hexc = lift(hexc)
        text = force_fill(svg_path.read_text(encoding="utf-8", errors="replace"), hexc)
        svg_path.write_text(text, encoding="utf-8")
        meta.setdefault("brand", {})["color"] = f"#{hexc}"
        meta["brand"]["color_source"] = "no-black-palette"
        meta.setdefault("visual", {})["approved_mono"] = False
        meta["visual"]["color_mode"] = "color"
        icons[key] = meta
        n += 1
    man["icons"] = icons
    man["icon_policy"] = {"no_pure_black": True}
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[no_black] recolored={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
