#!/usr/bin/env python3
"""Re-render protected payment SVGs without brand-color tinting."""
from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

yaml = __import__("yaml")
ROOT = Path(__file__).resolve().parents[1]
ICON_ROOT = ROOT / "assets/icons"
MAN = ICON_ROOT / "manifest.yaml"
PAYMENTS = ("applepay", "googlepay", "unionpay")
TITLES = {"applepay": "Apple Pay", "googlepay": "Google Pay", "unionpay": "UnionPay"}
SIZES = (64, 128, 256)


def load_renderer():
    try:
        import cairosvg
    except ImportError as exc:
        raise SystemExit(
            "CairoSVG is required for protected payment rendering; install requirements.lock"
        ) from exc
    return cairosvg


def validate_source(key: str, svg: Path) -> bytes:
    data = svg.read_bytes()
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise SystemExit(f"{key}: invalid payment SVG: {exc}") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise SystemExit(f"{key}: payment source root is not <svg>")
    view_box = root.attrib.get("viewBox", "").split()
    if len(view_box) != 4:
        raise SystemExit(f"{key}: payment source is missing a valid viewBox")
    titles = [
        (node.text or "").strip()
        for node in root.iter()
        if node.tag.rsplit("}", 1)[-1] == "title"
    ]
    if TITLES[key] not in titles:
        raise SystemExit(f"{key}: payment source title mismatch: {titles!r}")
    return data


def render(cairosvg, key: str, data: bytes, dest: Path, size: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        cairosvg.svg2png(
            bytestring=data,
            write_to=str(dest),
            output_width=size,
            output_height=size,
        )
    except Exception as exc:
        raise SystemExit(f"{key}: render failed at {size}px: {exc}") from exc
    if not dest.is_file() or dest.stat().st_size <= 200:
        raise SystemExit(f"{key}: invalid PNG generated at {dest}")


def main() -> None:
    cairosvg = load_renderer()
    doc = yaml.safe_load(MAN.read_text(encoding="utf-8")) or {}
    icons = doc.get("icons") or {}
    rendered = 0
    for key in PAYMENTS:
        meta = icons.get(key) or {}
        files = meta.get("files") or {}
        svg = ICON_ROOT / (files.get("svg") or f"source/{key}.svg")
        if not svg.is_file():
            raise SystemExit(f"missing payment source: {svg}")
        data = validate_source(key, svg)
        pngs = files.get("png") or {}
        for size in SIZES:
            rel = pngs.get(str(size)) or pngs.get(size) or f"png/{size}/{key}.png"
            render(cairosvg, key, data, ICON_ROOT / rel, size)
            rendered += 1
    print(f"[icon_render_overrides] rendered={rendered}")


if __name__ == "__main__":
    main()
