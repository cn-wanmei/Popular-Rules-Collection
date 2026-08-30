#!/usr/bin/env python3
"""build_icons.py — Icon System 2.0 renderer (SVG → PNG 64/128/256).

Color rules (brand-first):
  1. Multicolor official SVG → keep paints as-is
  2. Mono black SI + brand.color → tint brand color (no pure-black client icons)
  3. approved_mono (github/apple/…) → allow official black
  4. Policy/dataset geometric → keep project colors
  5. --monochrome → monochrome/{size} single-ink PNGs
  6. NEVER AI-generate brand marks
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


def _norm_hex(v: str) -> str | None:
    v = v.strip().lower()
    if v in ("none", "transparent", "currentcolor"):
        return None
    if v.startswith("url("):
        return None
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) >= 6 and re.match(r"^[0-9a-f]{6}", h):
            return "#" + h[:6]
    if re.match(r"^[0-9a-f]{6}$", v):
        return "#" + v
    return v


def extract_paint_colors(text: str) -> list[str]:
    vals = re.findall(r'(?:fill|stroke)\s*=\s*["\']([^"\']+)["\']', text, flags=re.I)
    out = []
    for v in vals:
        n = _norm_hex(v)
        if n and n.startswith("#"):
            out.append(n)
    return out


def is_near_black(hex_color: str) -> bool:
    h = hex_color.lstrip("#")
    if len(h) < 6:
        return False
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r + g + b) < 80


def is_near_white(hex_color: str) -> bool:
    h = hex_color.lstrip("#")
    if len(h) < 6:
        return False
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r + g + b) > 720


def has_multicolor_brand(text: str) -> bool:
    cols = extract_paint_colors(text)
    distinct = set()
    for c in cols:
        if is_near_black(c) or is_near_white(c):
            continue
        distinct.add(c)
    return len(distinct) >= 2


def is_mono_black_svg(text: str) -> bool:
    cols = extract_paint_colors(text)
    if not cols:
        return True
    return all(is_near_black(c) or is_near_white(c) for c in cols)


def has_concrete_fills(text: str) -> bool:
    return len(extract_paint_colors(text)) > 0


def apply_uniform_fill(text: str, color: str) -> str:
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
    return text


def prepare_svg_text(
    svg: Path,
    brand_color: str | None,
    monochrome: bool = False,
    *,
    keep_official_black: bool = False,
) -> bytes:
    text = svg.read_text(encoding="utf-8")
    color = (brand_color or "").strip() or DEFAULT_INK
    if not re.match(r"^#?[0-9A-Fa-f]{3,8}$", color) and not color.startswith("rgb"):
        color = DEFAULT_INK
    if not color.startswith("#") and re.match(r"^[0-9A-Fa-f]{6}$", color):
        color = "#" + color

    if monochrome:
        return apply_uniform_fill(text, color).encode("utf-8")

    if has_multicolor_brand(text):
        return text.encode("utf-8")

    if is_mono_black_svg(text):
        if keep_official_black and is_near_black(color):
            return apply_uniform_fill(text, color).encode("utf-8")
        if brand_color and not is_near_black(color):
            return apply_uniform_fill(text, color).encode("utf-8")
        if "currentColor" in text or "currentcolor" in text:
            text = text.replace("currentColor", color).replace("currentcolor", color)
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
        vis = meta.get("visual") or {}
        keep_black = bool(vis.get("approved_mono")) or key in (
            "github",
            "apple",
            "x",
            "twitter",
            "notion",
            "vercel",
            "steam",
            "uber",
            "threads",
        )
        data = prepare_svg_text(svg, color, monochrome=False, keep_official_black=keep_black)
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
