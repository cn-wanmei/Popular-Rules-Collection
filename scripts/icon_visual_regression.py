#!/usr/bin/env python3
"""icon_visual_regression.py — color_ratio / mono detection for Icon Dataset.

Soft gate: WARN on near-black official-colors, blank PNGs, or color_ratio regression.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "icons" / "manifest.yaml"
ICON_ROOT = ROOT / "assets" / "icons"
REPORTS = ROOT / "reports"
BASELINE = ROOT / "assets" / "icons" / "visual_baseline.json"


def color_metrics(png: Path) -> dict:
    try:
        from PIL import Image
    except ImportError:
        return {"error": "no-pillow"}
    im = Image.open(png).convert("RGBA")
    w, h = im.size
    total = w * h
    opaque = 0
    buckets: dict[tuple[int, int, int], int] = {}
    dark = 0
    for r, g, b, a in im.getdata():
        if a < 32:
            continue
        opaque += 1
        q = (r // 32 * 32, g // 32 * 32, b // 32 * 32)
        buckets[q] = buckets.get(q, 0) + 1
        if r + g + b < 60:
            dark += 1
    if opaque == 0:
        return {
            "opaque_ratio": 0.0,
            "color_ratio": 0.0,
            "dark_ratio": 0.0,
            "unique_buckets": 0,
            "likely_mono": True,
            "likely_blank": True,
        }
    top = max(buckets.values()) if buckets else 0
    color_ratio = 1.0 - (top / opaque) if opaque else 0.0
    multi = len([c for c, n in buckets.items() if n > opaque * 0.02])
    likely_mono = multi <= 1 or color_ratio < 0.08
    return {
        "opaque_ratio": round(opaque / total, 4),
        "color_ratio": round(color_ratio, 4),
        "dark_ratio": round(dark / opaque, 4),
        "unique_buckets": len(buckets),
        "multi_significant": multi,
        "likely_mono": likely_mono,
        "likely_blank": opaque / total < 0.02,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--size", type=int, default=256)
    args = ap.parse_args()

    if not MANIFEST.exists():
        print("[icon_visual] HARD missing manifest")
        return 1
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    icons = doc.get("icons") or {}
    results = {}
    hard: list[str] = []
    warn: list[str] = []

    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        rel = ((meta.get("files") or {}).get("png") or {}).get(str(args.size)) or f"png/{args.size}/{key}.png"
        png = ICON_ROOT / rel
        if not png.exists():
            warn.append(f"{key}: missing png {rel}")
            continue
        m = color_metrics(png)
        results[key] = m
        if m.get("likely_blank"):
            hard.append(f"{key}: likely blank png")
            continue
        prov = str(((meta.get("source") or {}).get("provenance") or ""))
        mode = str(((meta.get("visual") or {}).get("color_mode") or ""))
        if (
            prov == "official-colors"
            and mode == "color"
            and m.get("likely_mono")
            and float(m.get("dark_ratio") or 0) >= 0.85
        ):
            warn.append(
                f"{key}: official-colors but near-black mono "
                f"dark_ratio={m.get('dark_ratio')} color_ratio={m.get('color_ratio')}"
            )
        if m.get("opaque_ratio", 1) < 0.05:
            warn.append(f"{key}: very low opaque_ratio={m.get('opaque_ratio')}")

    baseline = {}
    if BASELINE.exists():
        try:
            baseline = json.loads(BASELINE.read_text(encoding="utf-8")) or {}
        except Exception:
            baseline = {}
    regressions = []
    for key, m in results.items():
        old = (baseline.get("icons") or {}).get(key) or {}
        if not old:
            continue
        old_cr = float(old.get("color_ratio") or 0)
        new_cr = float(m.get("color_ratio") or 0)
        if old_cr >= 0.25 and new_cr < 0.08:
            regressions.append(f"{key}: color_ratio {old_cr} → {new_cr}")
            warn.append(f"{key}: visual regression color_ratio {old_cr}→{new_cr}")

    if args.write_baseline:
        BASELINE.write_text(
            json.dumps(
                {
                    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "size": args.size,
                    "icons": results,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"[icon_visual] baseline written → {BASELINE} n={len(results)}")

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rep = REPORTS / day
    rep.mkdir(parents=True, exist_ok=True)
    status = "fail" if hard else ("warn" if warn or regressions else "pass")
    out = {
        "date": day,
        "status": status,
        "hard": hard,
        "warnings": warn[:80],
        "regressions": regressions,
        "counts": {
            "icons_measured": len(results),
            "hard": len(hard),
            "warn": len(warn),
            "regressions": len(regressions),
        },
    }
    (rep / "icon_visual.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"[icon_visual] status={status} measured={len(results)} "
        f"hard={len(hard)} warn={len(warn)} regressions={len(regressions)}"
    )
    for e in hard[:15]:
        print(f"  HARD  {e}")
    for w in warn[:20]:
        print(f"  WARN  {w}")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
