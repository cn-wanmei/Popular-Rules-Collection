#!/usr/bin/env python3
"""build_icons.py — Icon System V2 renderer (SVG → PNG 64/128/256).

Color rules (P0):
  1. path/root already has non-currentColor fills → keep as-is (multi-color logos)
  2. only currentColor / no fill → apply manifest brand.color (or DEFAULT_INK)
  3. NEVER force #0f172a on multi-color logos
  4. --monochrome: emit monochrome/{size} single-ink PNGs
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "icons" / "manifest.yaml"
ICON_ROOT = ROOT / "assets" / "icons"
SIZES = (64, 128, 256)
DEFAULT_INK = "#0f172a"


def load_manifest() -> dict:
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}")
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}


def has_concrete_fills(text: str) -> bool:
    fills = re.findall(r'fill\s*=\s*["\']([^"\']+)["\']', text, flags=re.I)
    strokes = re.findall(r'stroke\s*=\s*["\']([^"\']+)["\']', text, flags=re.I)
    concrete = []
    for v in fills + strokes:
        low = v.strip().lower()
        if low in ("none", "transparent", "currentcolor"):
            continue
        concrete.append(low)
    return len(concrete) > 0


def prepare_svg_text(svg: Path, brand_color: str | None, monochrome: bool = False) -> bytes:
    text = svg.read_text(encoding="utf-8")
    color = (brand_color or "").strip() or DEFAULT_INK
    if not re.match(r"^#?[0-9A-Fa-f]{3,8}$", color) and not color.startswith("rgb"):
        color = DEFAULT_INK
    if not color.startswith("#") and re.match(r"^[0-9A-Fa-f]{6}$", color):
        color = "#" + color

    if monochrome:
        text = re.sub(
            r'fill\s*=\s*["\'](?!none|transparent)[^"\']+["\']',
            f'fill="{color}"',
            text,
            flags=re.I,
        )
        text = re.sub(
            r'stroke\s*=\s*["\'](?!none|transparent)[^"\']+["\']',
            f'stroke="{color}"',
            text,
            flags=re.I,
        )
        if "fill=" not in text.lower():
            text = text.replace("<svg ", f'<svg fill="{color}" ', 1)
        return text.encode("utf-8")

    if has_concrete_fills(text):
        return text.encode("utf-8")

    if "currentColor" in text or "currentcolor" in text:
        text = text.replace("currentColor", color).replace("currentcolor", color)

    if "fill=" not in text.lower():
        text = text.replace("<svg ", f'<svg fill="{color}" ', 1)
    return text.encode("utf-8")


def brand_color_for(key: str, meta: dict) -> str | None:
    brand = meta.get("brand") or {}
    if isinstance(brand, dict) and brand.get("color"):
        return str(brand["color"])
    visual = meta.get("visual") or {}
    if isinstance(visual, dict) and visual.get("primary_color"):
        return str(visual["primary_color"])
    src = meta.get("source") or {}
    if isinstance(src, dict) and src.get("color"):
        return str(src["color"])
    return None


def try_cairosvg(data: bytes, dest: Path, size: int) -> bool:
    try:
        import cairosvg
    except ImportError:
        return False
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(
            bytestring=data,
            write_to=str(dest),
            output_width=size,
            output_height=size,
        )
        return dest.exists() and dest.stat().st_size > 200
    except Exception as e:
        print(f"  cairosvg fail {dest.name}@{size}: {e}")
        return False


def ensure_fallback_png(dest: Path, size: int, label: str, color: str = "#64748B") -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    c = color.lstrip("#")
    try:
        if len(c) == 3:
            c = "".join(ch * 2 for ch in c)
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    except Exception:
        r, g, b = 100, 116, 139
    im = Image.new("RGBA", (size, size), (241, 245, 249, 255))
    d = ImageDraw.Draw(im)
    margin = max(2, size // 16)
    d.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=size // 8,
        outline=(r, g, b, 255),
        width=max(2, size // 32),
    )
    letter = (label or "?")[:1].upper()
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    d.text((size // 2, size // 2), letter, fill=(r, g, b, 255), anchor="mm", font=font)
    im.save(dest, "PNG")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--monochrome", action="store_true")
    args = ap.parse_args()
    doc = load_manifest()
    icons = doc.get("icons") or {}
    ok = skip = fail = 0
    has_cairo = False
    try:
        import cairosvg  # noqa: F401

        has_cairo = True
    except ImportError:
        print("WARN: cairosvg not installed — letter fallbacks only")

    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        files = meta.get("files") or {}
        svg_rel = files.get("svg") or f"source/{key}.svg"
        svg = ICON_ROOT / svg_rel
        if not svg.exists():
            print(f"  MISS svg {key}")
            fail += 1
            continue
        color = brand_color_for(key, meta)
        data = prepare_svg_text(svg, color, monochrome=False)
        png_map = files.get("png") or {}
        for size in SIZES:
            rel = png_map.get(str(size)) or png_map.get(size) or f"png/{size}/{key}.png"
            dest = ICON_ROOT / rel
            if dest.exists() and not args.force and dest.stat().st_size > 3000 and has_cairo:
                ok += 1
                continue
            if try_cairosvg(data, dest, size):
                ok += 1
            else:
                ensure_fallback_png(dest, size, key, color or "#64748B")
                if dest.exists():
                    ok += 1
                else:
                    fail += 1

        if args.monochrome:
            mdata = prepare_svg_text(svg, color or DEFAULT_INK, monochrome=True)
            for size in SIZES:
                dest = ICON_ROOT / "monochrome" / str(size) / f"{key}.png"
                if try_cairosvg(mdata, dest, size):
                    ok += 1
                else:
                    ensure_fallback_png(dest, size, key, color or DEFAULT_INK)

    print(f"[build_icons] ok={ok} skip={skip} fail={fail} cairosvg={has_cairo} mono={args.monochrome}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
