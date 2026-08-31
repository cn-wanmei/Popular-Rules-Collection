#!/usr/bin/env python3
"""icon_qa.py — Icon Quality Gate. content-ratio + near-black; levels from qa.yaml."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
CFG = ROOT / "config" / "icons.yaml"
QA_CFG = ICON / "metadata" / "qa.yaml"
OUT = ROOT / "reports" / "latest_icon_qa.json"


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8")) if CFG.exists() else {}
    icons = man.get("icons") or {}
    approved = set(cfg.get("approved_mono_brands") or [])
    qa = yaml.safe_load(QA_CFG.read_text(encoding="utf-8")) if QA_CFG.exists() else {}
    cr = qa.get("content_ratio") or {}
    nb = qa.get("near_black") or {}
    cr_level = str(cr.get("level") or "warn")
    nb_level = str(nb.get("level") or "warn")
    cr_thr = float(cr.get("threshold") or 0.08)
    nb_thr = float(nb.get("threshold") or 0.9)
    hard: list[str] = []
    warn: list[str] = []

    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        files = meta.get("files") or {}
        svg_rel = files.get("svg") or f"source/{key}.svg"
        svg = ICON / svg_rel
        if not svg.exists() or svg.stat().st_size < 40:
            hard.append(f"{key}: missing/empty svg")
            continue
        text = svg.read_text(encoding="utf-8", errors="replace")
        if "<svg" not in text.lower():
            hard.append(f"{key}: invalid svg")
        if "viewbox" not in text.lower():
            warn.append(f"{key}: missing viewBox")
        png = ICON / (files.get("png") or {}).get("256", f"png/256/{key}.png")
        if not png.exists() or png.stat().st_size < 200:
            hard.append(f"{key}: missing png/256")
            continue
        try:
            from PIL import Image

            im = Image.open(png).convert("RGBA")
            w, h = im.size
            if (w, h) != (256, 256):
                warn.append(f"{key}: png size {w}x{h} != 256x256")
            dark = opaque = 0
            for r, g, b, a in im.getdata():
                if a < 32:
                    continue
                opaque += 1
                if r + g + b < 60:
                    dark += 1
            if opaque == 0:
                hard.append(f"{key}: blank png")
                continue
            dark_ratio = dark / opaque
            cat = "brand"
            for _sid, ent in (cfg.get("icons") or {}).items():
                if isinstance(ent, dict) and ent.get("icon_id") == key:
                    cat = str(ent.get("category") or "brand")
                    if ent.get("approved_mono"):
                        approved.add(key)
                    break
            xs, ys = [], []
            for y in range(h):
                for x in range(w):
                    a = im.getpixel((x, y))[3]
                    if a >= 32:
                        xs.append(x)
                        ys.append(y)
            if xs and ys:
                bw = max(xs) - min(xs) + 1
                bh = max(ys) - min(ys) + 1
                content_ratio = opaque / max(1, bw * bh)
                if content_ratio < cr_thr and cat == "brand":
                    msg = f"{key}: content_ratio={content_ratio:.3f} (glyph too small)"
                    (hard if cr_level in ("hard", "fail") else warn).append(msg)
            if dark_ratio >= nb_thr and key not in approved and cat == "brand":
                msg = f"{key}: near-black brand dark_ratio={dark_ratio:.2f}"
                (hard if nb_level in ("hard", "fail") else warn).append(msg)
        except Exception as e:
            warn.append(f"{key}: png read {e}")

    for sid, ent in (cfg.get("icons") or {}).items():
        if not isinstance(ent, dict):
            continue
        iid = str(ent.get("icon_id") or "")
        if iid and iid not in icons and iid != "placeholder":
            hard.append(f"{sid}: icon_id {iid} not in manifest")

    status = "fail" if hard else ("warn" if warn else "pass")
    doc = {"status": status, "hard": hard, "warn": warn, "icons": len(icons)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[icon_qa] status={status} hard={len(hard)} warn={len(warn)}")
    for x in hard[:20]:
        print(f"  HARD  {x}")
    for x in warn[:15]:
        print(f"  WARN  {x}")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
