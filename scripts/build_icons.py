#!/usr/bin/env python3
"""build_icons.py — Icon Dataset builder (SVG source → PNG sizes).

Does not touch Service Rules / Collect pipeline.
Optional: cairosvg for true SVG rasterization; else keeps existing PNG or draws placeholder.
"""
from __future__ import annotations

import argparse
import sys
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


def try_cairosvg(svg: Path, dest: Path, size: int) -> bool:
    try:
        import cairosvg  # type: ignore
    except ImportError:
        return False
    try:
        cairosvg.svg2png(
            url=str(svg), write_to=str(dest), output_width=size, output_height=size
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception as e:
        print(f"  cairosvg fail {svg.name}@{size}: {e}")
        return False


def ensure_placeholder_png(dest: Path, size: int, label: str) -> None:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(
        [size // 10, size // 10, size - size // 10, size - size // 10],
        radius=size // 8,
        fill=(30, 41, 59, 255),
    )
    d.ellipse(
        [size // 4, size // 4, size - size // 4, size - size // 4],
        outline=(148, 163, 184, 255),
        width=max(2, size // 20),
    )
    im.save(dest, "PNG")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force-placeholder", action="store_true")
    args = ap.parse_args()
    doc = load_manifest()
    icons = doc.get("icons") or {}
    ok = skip = fail = 0
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
            if dest.exists() and not args.force_placeholder:
                ok += 1
                continue
            if try_cairosvg(svg, dest, size):
                ok += 1
            else:
                ensure_placeholder_png(dest, size, key)
                if dest.exists():
                    ok += 1
                else:
                    fail += 1
    print(f"[build_icons] ok={ok} skip={skip} fail={fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
