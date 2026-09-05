#!/usr/bin/env python3
"""Re-render protected payment SVGs without brand-color tinting."""
from __future__ import annotations
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]; ICON_ROOT=ROOT/"assets/icons"; MAN=ICON_ROOT/"manifest.yaml"
def main():
    import cairosvg
    doc=yaml.safe_load(MAN.read_text(encoding="utf-8")) or {}; icons=doc.get("icons") or {}
    for key in ("applepay","googlepay","unionpay"):
        meta=icons.get(key) or {}; svg=ICON_ROOT/(meta.get("files",{}).get("svg") or f"source/{key}.svg")
        if not svg.exists(): raise SystemExit(f"missing {svg}")
        data=svg.read_bytes(); pngs=(meta.get("files",{}).get("png") or {})
        for size in (64,128,256):
            rel=pngs.get(str(size)) or f"png/{size}/{key}.png"; dest=ICON_ROOT/rel; dest.parent.mkdir(parents=True,exist_ok=True)
            cairosvg.svg2png(bytestring=data,write_to=str(dest),output_width=size,output_height=size)
    print("[icon_render_overrides] rendered=3x3")
if __name__=="__main__": main()
