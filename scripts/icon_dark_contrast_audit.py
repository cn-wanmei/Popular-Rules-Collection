#!/usr/bin/env python3
"""Dark Surface contrast audit for brand PNG delivery (Final Freeze P2)."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
OUT = ROOT / "reports" / "icon_dark_contrast.json"

BG = (15, 23, 42)


def luminance(r, g, b):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(rgb, bg=BG):
    L1 = luminance(*rgb)
    L2 = luminance(*bg)
    a, b = max(L1, L2), min(L1, L2)
    return (a + 0.05) / (b + 0.05)


def main() -> int:
    try:
        from PIL import Image
    except ImportError:
        print("[dark_contrast] pillow missing")
        return 0
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    rows = []
    low = []
    for key, meta in sorted(icons.items()):
        if not isinstance(meta, dict):
            continue
        cat = str(meta.get("type") or meta.get("namespace") or "brand")
        if cat in ("policy", "dataset", "network"):
            continue
        png = ICON / "png" / "128" / f"{key}.png"
        if not png.exists():
            continue
        im = Image.open(png).convert("RGBA")
        rs = gs = bs = n = 0
        for r, g, b, a in im.getdata():
            if a < 40:
                continue
            rs += r
            gs += g
            bs += b
            n += 1
        if n < 20:
            continue
        rgb = (rs // n, gs // n, bs // n)
        ratio = contrast(rgb)
        row = {
            "id": key,
            "mean_rgb": list(rgb),
            "contrast_on_dark": round(ratio, 2),
            "display_color": (meta.get("brand") or {}).get("display_color")
            or (meta.get("brand") or {}).get("color"),
        }
        rows.append(row)
        if ratio < 3.0:
            low.append(row)
    rows.sort(key=lambda x: x["contrast_on_dark"])
    doc = {
        "bg": list(BG),
        "threshold": 3.0,
        "checked": len(rows),
        "below_threshold": low,
        "worst": rows[:15],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[dark_contrast] checked={len(rows)} low={len(low)} report={OUT}")
    for r in low[:12]:
        print(f"  LOW  {r['id']} contrast={r['contrast_on_dark']} rgb={r['mean_rgb']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
