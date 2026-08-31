#!/usr/bin/env python3
"""PRC Icon Engine: Source -> Normalize -> Render (Final Freeze + P2 optical)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
LEGACY_PNG = ICON / "png"
RENDERED = ICON / "rendered"
NORMALIZED = ICON / "normalized"
OPTICAL = ICON / "metadata" / "optical_overrides.yaml"
SIZES = (64, 128, 256)
CANVAS = 512
SAFE = 0.82


def load_man():
    return yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}


def load_optical() -> dict:
    if not OPTICAL.exists():
        return {}
    doc = yaml.safe_load(OPTICAL.read_text(encoding="utf-8")) or {}
    return doc.get("overrides") or {}


def scale_for(key: str, overrides: dict) -> float:
    ent = overrides.get(key) or {}
    try:
        s = float(ent.get("scale") or 1.0)
    except (TypeError, ValueError):
        s = 1.0
    return max(0.7, min(1.2, s))


def brand_color(meta):
    brand = meta.get("brand") or {}
    if isinstance(brand, dict):
        for k in ("display_color", "color"):
            if brand.get(k):
                return str(brand[k])
    for bag in (meta.get("visual"), meta.get("source")):
        if isinstance(bag, dict) and bag.get("color"):
            return str(bag["color"])
        if isinstance(bag, dict) and bag.get("primary_color"):
            return str(bag["primary_color"])
    return None


def extract_viewbox(svg_text):
    m = re.search(r'viewBox\s*=\s*["\']([^"\']+)["\']', svg_text, re.I)
    return m.group(1).strip() if m else "0 0 24 24"


def inner_content(svg_text):
    t = re.sub(r"<\?xml[^>]*\?>", "", svg_text, flags=re.I)
    t = re.sub(r"<!DOCTYPE[^>]*>", "", t, flags=re.I)
    m = re.search(r"<svg\b[^>]*>(.*)</svg\s*>", t, re.I | re.S)
    return m.group(1).strip() if m else t.strip()


def normalize_svg(svg_text, scale: float = 1.0):
    vb = extract_viewbox(svg_text)
    inner = inner_content(svg_text)
    safe = max(0.55, min(0.95, SAFE * scale))
    pad = (1.0 - safe) / 2.0 * CANVAS
    size = safe * CANVAS
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}" '
        f'width="{CANVAS}" height="{CANVAS}">\n'
        f'  <svg x="{pad:.2f}" y="{pad:.2f}" width="{size:.2f}" height="{size:.2f}" '
        f'viewBox="{vb}" preserveAspectRatio="xMidYMid meet">\n'
        f"    {inner}\n"
        "  </svg>\n</svg>\n"
    )


def near_black(v):
    v = v.strip().lower()
    if v in ("none", "transparent", "currentcolor"):
        return True
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) >= 6:
            try:
                r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                return r + g + b < 80
            except Exception:
                return False
    return False


def apply_tint_if_mono_black(svg_text, color, keep_black):
    if not color or keep_black:
        return svg_text
    fills = re.findall(r'fill\s*=\s*["\']([^"\']+)["\']', svg_text, flags=re.I)
    concrete = [f for f in fills if f.strip().lower() not in ("none", "transparent")]
    if concrete and not all(near_black(f) for f in concrete):
        return svg_text
    c = color if color.startswith("#") else ("#" + color)
    out = re.sub(
        r'fill\s*=\s*["\'](?!none|transparent)[^"\']+["\']',
        f'fill="{c}"',
        svg_text,
        flags=re.I,
    )
    if "fill=" not in out.lower():
        out = out.replace("<svg ", f'<svg fill="{c}" ', 1)
    out = re.sub(r"<path\b(?![^>]*fill=)", f'<path fill="{c}"', out)
    return out


def cairo_png(svg_bytes, dest, size):
    try:
        import cairosvg
    except ImportError:
        return False
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(
            bytestring=svg_bytes, write_to=str(dest), output_width=size, output_height=size
        )
        return dest.exists() and dest.stat().st_size > 100
    except Exception:
        return False


def composite_tile(src_png, dest, bg):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False
    if not src_png.exists():
        return False
    im = Image.open(src_png).convert("RGBA")
    size = im.size[0]
    canvas = Image.new("RGBA", (size, size), bg)
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    rad = max(4, int(size * 0.18))
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=rad, fill=255)
    pad = max(2, size // 12)
    logo = im.resize((size - 2 * pad, size - 2 * pad), Image.Resampling.LANCZOS)
    canvas.paste(logo, (pad, pad), logo)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(canvas, mask=mask)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG")
    return True


def render_mode(meta):
    itype = str(meta.get("type") or "")
    ns = str(meta.get("namespace") or "")
    if itype in ("policy", "dataset", "network") or ns in ("policy", "dataset", "network"):
        return "semantic"
    return str((meta.get("render") or {}).get("mode") or "brand_preserve")


def process_one(key, meta, force):
    svg_path = ICON / ((meta.get("files") or {}).get("svg") or f"source/{key}.svg")
    if not svg_path.exists():
        return "miss"
    raw = svg_path.read_text(encoding="utf-8", errors="replace")
    color = brand_color(meta)
    if color:
        raw = apply_tint_if_mono_black(raw, color, False)
    scale = scale_for(key, load_optical())
    norm = normalize_svg(raw, scale=scale)
    if color:
        norm = apply_tint_if_mono_black(norm, color, False)
    NORMALIZED.mkdir(parents=True, exist_ok=True)
    (NORMALIZED / f"{key}.svg").write_text(norm, encoding="utf-8")
    nb = norm.encode("utf-8")
    ok = True
    for size in SIZES:
        tdest = RENDERED / "transparent" / str(size) / f"{key}.png"
        leg = LEGACY_PNG / str(size) / f"{key}.png"
        if force or not tdest.exists() or tdest.stat().st_size < 200:
            if not cairo_png(nb, tdest, size):
                ok = False
                continue
        if tdest.exists():
            leg.parent.mkdir(parents=True, exist_ok=True)
            leg.write_bytes(tdest.read_bytes())
        for variant, bg in (("light", (248, 250, 252, 255)), ("dark", (15, 23, 42, 255))):
            vdest = RENDERED / variant / str(size) / f"{key}.png"
            if force or not vdest.exists():
                composite_tile(tdest, vdest, bg)
    return "ok" if ok else "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    man = load_man()
    icons = man.get("icons") or {}
    only = {x.strip() for x in args.only.split(",") if x.strip()} if args.only else None
    stats = {"ok": 0, "fail": 0, "miss": 0, "skip": 0}
    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        if only and key not in only:
            stats["skip"] += 1
            continue
        r = process_one(key, meta, args.force)
        stats[r] = stats.get(r, 0) + 1
        if r == "ok":
            meta.setdefault("render", {})
            meta["render"]["mode"] = render_mode(meta)
            meta["render"]["canvas"] = CANVAS
            meta["render"]["safe_area"] = SAFE
            meta["render"]["optical_scale"] = scale_for(key, load_optical())
            meta["render"]["variants"] = ["transparent", "light", "dark"]
            meta["render"]["engine"] = "prc-icon-engine-1"
            icons[key] = meta
    man["icons"] = icons
    man["icon_engine"] = {"version": 1, "canvas": CANVAS, "safe_area": SAFE}
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[icon_engine] {stats}")
    return 0 if stats.get("fail", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
