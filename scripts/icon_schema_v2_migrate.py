#!/usr/bin/env python3
"""Migrate manifest → Schema V2 (backward-compatible)."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
WL = ICON / "metadata" / "official_whitelist.yaml"


def map_source_type(src: dict, itype: str) -> str:
    prov = str(src.get("provenance") or "")
    provider = str(src.get("provider") or "")
    if itype in ("policy", "dataset", "network") or (provider == "project" and prov == "project"):
        return "geometric"
    if provider == "simple-icons" or prov == "third_party":
        return "simple-icons"
    if provider == "official-pack" or prov == "official-source":
        return "official-source"
    if provider in ("project-brand", "project") and prov == "official-colors":
        return "project-redraw"
    if prov == "official-guideline":
        return "official-guideline"
    if provider == "community":
        return "community"
    return "project-generated"


def compute_status(meta: dict) -> str:
    if meta.get("icon_key") == "placeholder" or meta.get("name") == "Placeholder":
        return "placeholder"
    ident = meta.get("identity") or {}
    src = meta.get("source") or {}
    vis = meta.get("visual") or {}
    stype = str(src.get("type") or "")
    if not (src.get("provider") or stype):
        return "missing"
    if not vis.get("qa_passed"):
        return "visual-review"
    if not ident.get("verified"):
        return "identity-review"
    if stype in ("geometric", "official-source"):
        return "verified"
    if stype == "project-redraw" and ident.get("verified"):
        return "verified"
    if stype == "simple-icons":
        return "sourced"
    return "sourced"


def migrate_one(key: str, meta: dict, whitelist: set) -> dict:
    if not isinstance(meta, dict):
        meta = {}
    itype = str(meta.get("type") or "service")
    src = dict(meta.get("source") or {})
    brand = dict(meta.get("brand") or {})
    vis = dict(meta.get("visual") or {})
    lic = dict(meta.get("license") or {})
    files = meta.get("files") or {}

    stype = map_source_type(src, itype)
    src["type"] = stype
    src_verified = stype in ("simple-icons", "official-source", "geometric", "project-redraw")
    if stype == "official-source":
        src["verified"] = bool(src.get("verified", True))
    else:
        src["verified"] = src_verified

    ident = dict(meta.get("identity") or {})
    if key in whitelist or itype in ("policy", "dataset", "network") or stype == "geometric":
        ident["verified"] = True
        ident.pop("review_required", None)
    elif stype == "simple-icons":
        ident["verified"] = True
        ident["confidence"] = "slug-match" if src.get("slug") else "simple-icons"
        ident.pop("review_required", None)
    else:
        ident.setdefault("verified", False)
        if not ident.get("verified"):
            ident["review_required"] = True
    ident["icon_id"] = key
    meta["identity"] = ident

    if stype == "geometric":
        brand["color_verified"] = True
        brand["color_na"] = True
    elif brand.get("color") or src.get("color"):
        brand.setdefault("color", brand.get("color") or src.get("color"))
        brand["color_verified"] = stype in ("official-source", "official-guideline") or (
            stype == "project-redraw" and key in whitelist
        )
        brand.setdefault("color_source", "simple-icons" if stype == "simple-icons" else brand.get("color_source"))
    else:
        brand["color_verified"] = False
    meta["brand"] = brand

    if stype == "geometric":
        lic["reviewed"] = True
        lic.setdefault("type", "CC0-1.0")
    elif lic.get("type") or lic.get("note"):
        lic["reviewed"] = True
    else:
        lic["reviewed"] = False
        lic.setdefault("type", "see-source")
    meta["license"] = lic

    png = files.get("png") if isinstance(files.get("png"), dict) else {}
    svg_path = files.get("svg") or f"source/{key}.svg"
    variants = dict(meta.get("variants") or {})
    color_mode = str(vis.get("color_mode") or "monochrome")
    if color_mode in ("color", "brand") or stype == "geometric":
        variants.setdefault(
            "brand",
            {
                "status": "available",
                "color_mode": "brand" if color_mode != "monochrome" else "monochrome-as-brand",
                "svg": svg_path,
                "png": png or {"64": f"png/64/{key}.png", "128": f"png/128/{key}.png", "256": f"png/256/{key}.png"},
            },
        )
    else:
        variants.setdefault(
            "brand",
            {
                "status": "available",
                "color_mode": "monochrome-tinted",
                "svg": svg_path,
                "png": png,
                "tint_color": brand.get("color"),
                "note": "Master SVG is mono; brand.color used at render",
            },
        )
    mono_png = {"64": f"monochrome/64/{key}.png", "128": f"monochrome/128/{key}.png", "256": f"monochrome/256/{key}.png"}
    mono_ok = (ICON / mono_png["256"]).exists()
    variants.setdefault(
        "mono",
        {"status": "available" if mono_ok else "optional", "color_mode": "monochrome", "png": mono_png if mono_ok else {}},
    )
    if vis.get("theme_mapping"):
        variants.setdefault(
            "dark",
            {"status": "mapped", "maps_to": vis["theme_mapping"].get("dark", "monochrome"), "color_mode": "monochrome"},
        )
        variants.setdefault(
            "light",
            {"status": "mapped", "maps_to": vis["theme_mapping"].get("light", "brand"), "color_mode": "brand"},
        )
    meta["variants"] = variants

    png256 = ICON / (png.get("256") or f"png/256/{key}.png")
    vis["qa_passed"] = png256.exists() and (ICON / svg_path).exists()
    vis["qa"] = "passed" if vis["qa_passed"] else "pending"
    vis["primary_variant"] = "brand"
    meta["visual"] = vis
    meta["source"] = src

    if itype == "policy":
        meta["namespace"] = "policy"
    elif itype == "dataset":
        meta["namespace"] = "dataset"
    elif itype == "network":
        meta["namespace"] = "network"
    else:
        meta["namespace"] = "brand"

    meta["status"] = compute_status(meta)
    meta["schema"] = 2
    return meta


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    wl = set()
    if WL.exists():
        doc = yaml.safe_load(WL.read_text(encoding="utf-8")) or {}
        wl = set((doc.get("verified_official") or {}).keys())
    icons = man.get("icons") or {}
    out = {}
    stats = {}
    for key, meta in icons.items():
        out[key] = migrate_one(key, meta, wl)
        st = out[key].get("status")
        stats[st] = stats.get(st, 0) + 1
    man["icons"] = out
    man["schema_version"] = 2
    man["updated"] = str(date.today())
    man["schema_v2"] = {"migrated": len(out), "status_counts": stats}
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[schema_v2] migrated={len(out)} status={stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
