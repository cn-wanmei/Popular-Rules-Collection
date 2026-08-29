#!/usr/bin/env python3
"""Icon P2: pin SI → official intake → theme roles → QA config → dual-write."""
from __future__ import annotations

import os
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
SRC = ICON / "source"
OFFICIAL_DIR = ICON / "official"
MAN = ICON / "manifest.yaml"
WL = ICON / "metadata" / "official_whitelist.yaml"
QA_CFG = ICON / "metadata" / "qa.yaml"
SI_VER = "13.21.0"

STRATEGY_KEYS = {"direct", "proxy", "reject", "dns", "global", "select", "match", "placeholder"}
DATASET_KEYS = {
    "china", "lan", "geoip", "geosite", "asn", "network", "private", "stun",
    "adblock", "gfw", "chinamobile", "chinaunicom", "chinatelecom", "provider", "cloud",
}


def p23_pin(man: dict) -> int:
    icons = man.setdefault("icons", {})
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n = 0
    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        src = meta.setdefault("source", {})
        if not (src.get("slug") or src.get("provider") == "simple-icons"):
            continue
        src["upstream"] = "simple-icons"
        src["upstream_version"] = SI_VER
        src.setdefault("retrieved_at", now)
        src["upstream_package"] = f"https://cdn.jsdelivr.net/npm/simple-icons@{SI_VER}/"
        icons[key] = meta
        n += 1
    man["icons"] = icons
    man["si_pin"] = {"version": SI_VER, "pinned_at": now, "count": n}
    print(f"[P2.3] pinned={n} si={SI_VER}")
    return n


def p25_official(man: dict) -> int:
    OFFICIAL_DIR.mkdir(parents=True, exist_ok=True)
    readme = OFFICIAL_DIR / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Official icon packs\n\nPlace `{icon_id}.svg` then run `python scripts/icon_p2_apply.py`.\n",
            encoding="utf-8",
        )
    wl = {}
    if WL.exists():
        wl = (yaml.safe_load(WL.read_text(encoding="utf-8")) or {}).get("verified_official") or {}
    icons = man.setdefault("icons", {})
    smap = man.setdefault("service_icon_map", {})
    n = 0
    for svg in sorted(OFFICIAL_DIR.glob("*.svg")):
        key = svg.stem.lower().replace(" ", "")
        data = svg.read_bytes()
        if len(data) < 40:
            continue
        (SRC / f"{key}.svg").write_bytes(data)
        meta = icons.get(key) or {"name": key.title(), "type": "service", "icon_key": key}
        info = wl.get(key) or {}
        meta["source"] = {
            "provider": "official-pack",
            "provenance": "official-colors",
            "verified": True,
            "whitelist": key in wl,
            "media_kit": (info.get("kit") if isinstance(info, dict) else None) or "official-drop",
            "path": f"official/{svg.name}",
            "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        meta["status"] = "verified"
        meta["files"] = {
            "svg": f"source/{key}.svg",
            "png": {"64": f"png/64/{key}.png", "128": f"png/128/{key}.png", "256": f"png/256/{key}.png"},
        }
        meta["license"] = meta.get("license") or {
            "type": "brand",
            "note": "Official brand asset; trademarks apply.",
        }
        icons[key] = meta
        smap[key] = key
        n += 1
        print(f"  [P2.5] imported official/{svg.name}")
    man["icons"] = icons
    man["service_icon_map"] = smap
    print(f"[P2.5] official_imported={n}")
    return n


def p21_theme(man: dict) -> int:
    icons = man.setdefault("icons", {})
    n = 0
    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        vis = meta.setdefault("visual", {})
        approved = bool(vis.get("approved_mono") or vis.get("approved_theme_variant"))
        if not approved and key in ("github", "apple", "notion", "vercel", "steam", "x", "twitter"):
            vis["approved_mono"] = True
            approved = True
        variants = list(vis.get("variants") or ["brand", "mono"])
        if "mono" not in variants:
            variants.append("mono")
        if approved:
            if "dark" not in variants:
                variants.append("dark")
            vis["theme_mapping"] = {
                "dark": "monochrome",
                "light": "brand",
                "note": "dark uses mono path; no bulk theme PNGs unless approved_theme_variant",
            }
            n += 1
        vis["variants"] = variants
        meta["visual"] = vis
        icons[key] = meta
    man["icons"] = icons
    print(f"[P2.1] theme_roles={n}")
    return n


def p24_qa_config() -> None:
    doc = {
        "version": 1,
        "updated": str(date.today()),
        "content_ratio": {"enabled": True, "threshold": 0.08, "level": "warn"},
        "near_black": {
            "enabled": True,
            "threshold": 0.9,
            "level": "warn",
            "skip_approved_mono": True,
        },
    }
    QA_CFG.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print("[P2.4] wrote metadata/qa.yaml")


def p22_dual_write(man: dict) -> int:
    icons = man.get("icons") or {}
    n = 0
    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        itype = str(meta.get("type") or "")
        if key in STRATEGY_KEYS or itype == "policy":
            bucket = "strategies"
        elif key in DATASET_KEYS or itype in ("dataset", "network"):
            bucket = "datasets"
        else:
            if os.environ.get("P2_DUAL_BRANDS") != "1":
                continue
            bucket = "brands"
        svg = SRC / f"{key}.svg"
        if not svg.exists():
            continue
        dest_dir = ICON / bucket / key
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(svg, dest_dir / "icon.svg")
        for size in (64, 128, 256):
            png = ICON / "png" / str(size) / f"{key}.png"
            if png.exists():
                shutil.copy2(png, dest_dir / f"{size}.png")
        alt = meta.setdefault("files_alt", {})
        alt["root"] = f"{bucket}/{key}"
        alt["svg"] = f"{bucket}/{key}/icon.svg"
        alt["png"] = {str(s): f"{bucket}/{key}/{s}.png" for s in (64, 128, 256)}
        icons[key] = meta
        n += 1
    man["icons"] = icons
    man["dual_write"] = {
        "enabled": True,
        "legacy_primary": True,
        "brands_opt_in": "P2_DUAL_BRANDS=1",
        "count": n,
    }
    print(f"[P2.2] dual_write={n} (legacy primary)")
    return n


def main() -> int:
    SRC.mkdir(parents=True, exist_ok=True)
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    p23_pin(man)
    p25_official(man)
    p21_theme(man)
    p24_qa_config()
    p22_dual_write(man)
    man["updated"] = str(date.today())
    man["phase_p2"] = {"si_version": SI_VER, "date": str(date.today()), "steps": ["2.3", "2.5", "2.1", "2.4", "2.2"]}
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print("[icon_p2_apply] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
