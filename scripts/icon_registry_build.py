#!/usr/bin/env python3
"""icon_registry_build.py — rebuild registry.yaml from manifest + service_icon_map."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
REG = ICON / "registry.yaml"

NETWORK_KEYS = {
    "direct", "proxy", "reject", "dns", "lan", "china", "geoip", "geosite", "asn",
    "network", "placeholder", "chinamobile", "chinaunicom", "chinatelecom",
    "stun", "adblock", "gfw", "private", "global",
}


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


def main() -> int:
    man = load(MAN) or {}
    icons = man.get("icons") or {}
    smap = man.get("service_icon_map") or {}
    registry_services = {}
    variant_catalog = {}

    def add_variant(vid: str, **kw):
        variant_catalog[vid] = kw

    for sid, icon_key in sorted(smap.items()):
        icon_key = str(icon_key)
        meta = icons.get(icon_key) or {}
        if not isinstance(meta, dict):
            meta = {}
        prov = str(((meta.get("source") or {}).get("provenance") or ""))
        provider = str(((meta.get("source") or {}).get("provider") or ""))
        mode = str(((meta.get("visual") or {}).get("color_mode") or ""))
        status = str(meta.get("status") or "sourced")
        svg_rel = ((meta.get("files") or {}).get("svg") or f"source/{icon_key}.svg")
        png256 = ((meta.get("files") or {}).get("png") or {}).get("256") or f"png/256/{icon_key}.png"
        variants = {}

        if icon_key in NETWORK_KEYS or prov == "project" or provider == "project":
            nid = f"{icon_key}-network"
            add_variant(
                nid, type="network", source="project", path=svg_rel,
                png={"256": png256, "128": f"png/128/{icon_key}.png", "64": f"png/64/{icon_key}.png"},
                color_mode="color", status="verified", service_icon_key=icon_key,
            )
            variants["network"] = nid
            variants["default"] = nid
        elif prov == "official-colors" or provider == "project-brand":
            bid = f"{icon_key}-brand"
            add_variant(
                bid, type="brand", source=provider or "project-brand", path=svg_rel,
                png={"256": png256, "128": f"png/128/{icon_key}.png", "64": f"png/64/{icon_key}.png"},
                color_mode=mode or "color", status=status, service_icon_key=icon_key,
            )
            variants["brand"] = bid
            variants["default"] = bid
        elif provider == "simple-icons" or prov == "third_party":
            sid_v = f"{icon_key}-simple"
            add_variant(
                sid_v, type="simple", source="simple-icons",
                slug=((meta.get("source") or {}).get("slug")), path=svg_rel,
                png={"256": png256}, color_mode="monochrome", status="sourced",
                brand_color=((meta.get("brand") or {}).get("color")), service_icon_key=icon_key,
            )
            variants["simple"] = sid_v
            variants["default"] = sid_v
        else:
            pid = "placeholder-default"
            add_variant(
                pid, type="placeholder", source="project", path="source/placeholder.svg",
                png={"256": "png/256/placeholder.png"}, color_mode="color", status="verified",
            )
            variants["default"] = pid
            variants["placeholder"] = pid

        mono_png = f"monochrome/256/{icon_key}.png"
        if icon_key != "placeholder" and (
            (ICON / mono_png).exists() or (ICON / "source" / f"{icon_key}.svg").exists()
        ):
            mid = f"{icon_key}-mono"
            add_variant(
                mid, type="monochrome", source="project-render", path=svg_rel,
                png={"256": mono_png if (ICON / mono_png).exists() else png256},
                color_mode="monochrome", status=status, service_icon_key=icon_key,
            )
            variants["mono"] = mid

        default_by_profile = {
            "brand": variants.get("brand") or variants.get("simple") or variants.get("default"),
            "colorful": variants.get("brand") or variants.get("simple") or variants.get("default"),
            "minimal": variants.get("flat") or variants.get("simple") or variants.get("default"),
            "monochrome": variants.get("mono") or variants.get("default"),
            "network": variants.get("network") or variants.get("default"),
            "client": variants.get("brand") or variants.get("simple") or variants.get("default"),
        }
        registry_services[sid] = {
            "icon_key": icon_key,
            "variants": variants,
            "default": variants.get("default"),
            "default_by_profile": default_by_profile,
        }

    for icon_key, meta in icons.items():
        if icon_key in registry_services:
            continue
        if not isinstance(meta, dict):
            continue
        if icon_key not in NETWORK_KEYS and str(meta.get("type") or "") not in ("policy", "dataset", "network"):
            continue
        svg_rel = ((meta.get("files") or {}).get("svg") or f"source/{icon_key}.svg")
        png256 = ((meta.get("files") or {}).get("png") or {}).get("256") or f"png/256/{icon_key}.png"
        nid = f"{icon_key}-network"
        if nid not in variant_catalog:
            variant_catalog[nid] = {
                "type": "network", "source": "project", "path": svg_rel,
                "png": {"256": png256}, "color_mode": "color", "status": "verified",
                "service_icon_key": icon_key,
            }
        registry_services[icon_key] = {
            "icon_key": icon_key,
            "variants": {"network": nid, "default": nid},
            "default": nid,
            "default_by_profile": {
                "brand": nid, "colorful": nid, "minimal": nid, "monochrome": nid,
                "network": nid, "client": nid,
            },
        }

    doc = {
        "version": 1,
        "updated": str(date.today()),
        "description": "Service → Icon Variant roles (shared paths until dedicated sources exist)",
        "limits": {
            "max_variants_per_service": 5,
            "roles": ["brand", "simple", "flat", "mono", "network", "placeholder", "default"],
        },
        "services": registry_services,
        "variants": variant_catalog,
    }
    REG.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[icon_registry_build] services={len(registry_services)} variants={len(variant_catalog)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
