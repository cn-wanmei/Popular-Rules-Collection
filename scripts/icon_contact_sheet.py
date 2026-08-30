#!/usr/bin/env python3
"""Contact sheet for visual audit."""
from __future__ import annotations
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
OUT = ROOT / "reports" / "icons" / "contact-sheet.png"
CELL, COLS = 96, 12

def main():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("need pillow")
        return 1
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    keys = sorted(k for k, m in (man.get("icons") or {}).items() if isinstance(m, dict))
    rows = (len(keys) + COLS - 1) // COLS
    sheet = Image.new("RGBA", (COLS * CELL, max(1, rows) * CELL), (30, 41, 59, 255))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    for i, key in enumerate(keys):
        r, c = divmod(i, COLS)
        x, y = c * CELL, r * CELL
        png = ICON / "png" / "128" / f"{key}.png"
        if not png.exists():
            png = ICON / "png" / "64" / f"{key}.png"
        if png.exists():
            im = Image.open(png).convert("RGBA").resize((CELL - 16, CELL - 16), Image.Resampling.LANCZOS)
            sheet.paste(im, (x + 8, y + 4), im)
        draw.text((x + 4, y + CELL - 12), key[:12], fill=(226, 232, 240, 255), font=font)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT, "PNG")
    print(f"[contact_sheet] {len(keys)} -> {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
