#!/usr/bin/env python3
"""build_icons.py — Icon Dataset builder (SVG source → PNG sizes).

Requires cairosvg for true rasterization. Without it, writes a visible
letter fallback (not a blank dark tile).
  pip install cairosvg && system libcairo2
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "icons" / "manifest.yaml"
ICON_ROOT = ROOT / "assets" / "icons"
SIZES = (64, 128, 256)


def load_manifest() -> dict:
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}")
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}


def prepare_svg_text(svg: Path) -> bytes:
    text = svg.read_text(encoding="utf-8")
    if "fill=" not in text:
        text = text.replace("<svg ", '<svg fill="#0f172a" ', 1)
    return text.encode("utf-8")


def try_cairosvg(svg: Path, dest: Path, size: int) -> bool:
    try:
        import cairosvg
    except ImportError:
        return False
    try:
        data = prepare_svg_text(svg)
        cairosvg.svg2png(
            bytestring=data,
            write_to=str(dest),
            output_width=size,
            output_height=size,
        )
        return dest.exists() and dest.stat().st_size > 200
    except Exception as e:
        print(f"  cairosvg fail {svg.name}@{size}: {e}")
        return False


def ensure_fallback_png(dest: Path, size: int, label: str) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGBA", (size, size), (241, 245, 249, 255))
    d = ImageDraw.Draw(im)
    margin = max(2, size // 16)
    d.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=size // 8,
        outline=(51, 65, 85, 255),
        width=max(2, size // 32),
    )
    letter = (label or "?")[:1].upper()
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    d.text((size // 2, size // 2), letter, fill=(15, 23, 42, 255), anchor="mm", font=font)
    im.save(dest, "PNG")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="rebuild even if PNG exists")
    args = ap.parse_args()
    doc = load_manifest()
    icons = doc.get("icons") or {}
    ok = skip = fail = 0
    has_cairo = False
    try:
        import cairosvg  # noqa: F401

        has_cairo = True
    except ImportError:
        print("WARN: cairosvg not installed — PNG will be letter fallbacks, not real logos")

    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        files = meta.get("files") or {}
        svg_rel = files.get("svg")
        if not svg_rel:
            skip += 1
            continue
        svg = ICON_ROOT / svg_rel
        if not svg.exists():
            print(f"  MISS svg {key}")
            fail += 1
            continue
        png_map = files.get("png") or {}
        for size in SIZES:
            rel = png_map.get(str(size)) or png_map.get(size) or f"png/{size}/{key}.png"
            dest = ICON_ROOT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if (
                dest.exists()
                and not args.force
                and dest.stat().st_size > 3000
                and has_cairo
            ):
                ok += 1
                continue
            if try_cairosvg(svg, dest, size):
                ok += 1
            else:
                ensure_fallback_png(dest, size, key)
                if dest.exists():
                    ok += 1
                else:
                    fail += 1
    print(f"[build_icons] ok={ok} skip={skip} fail={fail} cairosvg={has_cairo}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
