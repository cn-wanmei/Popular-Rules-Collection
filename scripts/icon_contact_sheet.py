#!/usr/bin/env python3
"""Modern Brand Icon Grid v2 — contact sheet (audit display only).

Tightened rules:
  - Light canvas #F7F7F8
  - Unified cards, subtle border, 8pt grid
  - Optical center + weight via alpha bbox (no brand redraw)
  - Brand section vs Semantic section (no rainbow frames in brand grid)
  - Client PNG paths unchanged
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
OUT = ROOT / "reports" / "icons" / "contact-sheet.png"
OUT_SEM = ROOT / "reports" / "icons" / "contact-sheet-semantic.png"

GAP = 16
PAD = 24
CARD_W = 88
CARD_H = 100
LOGO_MAX = 44
RADIUS = 10
COLS = 10
BG = (247, 247, 248, 255)
CARD_BG = (255, 255, 255, 255)
BORDER = (226, 232, 240, 255)
LABEL = (71, 85, 105, 255)
TITLE = (15, 23, 42, 255)


def is_semantic(meta: dict) -> bool:
    t = str(meta.get("type") or "")
    ns = str(meta.get("namespace") or "")
    return t in ("policy", "dataset", "network") or ns in ("policy", "dataset", "network")


def load_icons():
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    brand, semantic = [], []
    for k, m in icons.items():
        if not isinstance(m, dict):
            continue
        (semantic if is_semantic(m) else brand).append((k, m))
    brand.sort(key=lambda x: x[0])
    semantic.sort(key=lambda x: x[0])
    return brand, semantic


def load_logo(key: str):
    from PIL import Image

    for size in (128, 256, 64):
        p = ICON / "png" / str(size) / f"{key}.png"
        if not p.exists():
            p = ICON / "rendered" / "transparent" / str(size) / f"{key}.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
    return None


def optical_fit(im, max_side: int):
    from PIL import Image

    if im is None:
        return None
    alpha = im.split()[-1]
    bbox = alpha.getbbox()
    if not bbox:
        return im.resize((max_side, max_side), Image.Resampling.LANCZOS)
    cropped = im.crop(bbox)
    w, h = cropped.size
    scale = max_side / max(w, h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    return cropped.resize((nw, nh), Image.Resampling.LANCZOS)


def rounded_card(draw, x, y, w, h, fill, outline, radius):
    draw.rounded_rectangle(
        [x, y, x + w - 1, y + h - 1], radius=radius, fill=fill, outline=outline, width=1
    )


def draw_grid(items, title: str, out_path: Path) -> int:
    from PIL import Image, ImageDraw, ImageFont

    n = len(items)
    if n == 0:
        return 0
    rows = (n + COLS - 1) // COLS
    title_h = 40
    width = PAD * 2 + COLS * CARD_W + (COLS - 1) * GAP
    height = PAD * 2 + title_h + rows * CARD_H + (rows - 1) * GAP
    sheet = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    try:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
    except Exception:
        font_title = font_label = None

    draw.text((PAD, 12), title, fill=TITLE, font=font_title)

    for i, (key, meta) in enumerate(items):
        r, c = divmod(i, COLS)
        x = PAD + c * (CARD_W + GAP)
        y = PAD + title_h + r * (CARD_H + GAP)
        rounded_card(draw, x, y, CARD_W, CARD_H, CARD_BG, BORDER, RADIUS)

        logo = optical_fit(load_logo(key), LOGO_MAX)
        if logo is not None:
            lx = x + (CARD_W - logo.size[0]) // 2
            ly = y + 12 + (LOGO_MAX - logo.size[1]) // 2
            sheet.paste(logo, (lx, ly), logo)

        name = str(meta.get("name") or key)
        label = name if len(name) <= 12 else (name[:11] + "…")
        try:
            bbox = draw.textbbox((0, 0), label, font=font_label)
            tw = bbox[2] - bbox[0]
        except Exception:
            tw = len(label) * 6
        tx = x + max(4, (CARD_W - tw) // 2)
        ty = y + CARD_H - 18
        draw.text((tx, ty), label, fill=LABEL, font=font_label)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, "PNG")
    return n


def main() -> int:
    brand, semantic = load_icons()
    nb = draw_grid(brand, "Brand icons — optical grid (v2)", OUT)
    ns = draw_grid(semantic, "Semantic / policy / network (separate language)", OUT_SEM)
    print(f"[grid_v2] brand={nb} → {OUT}")
    print(f"[grid_v2] semantic={ns} → {OUT_SEM}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
