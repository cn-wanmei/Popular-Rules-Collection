#!/usr/bin/env python3
"""P0/P1 apply: official whitelist provenance + client CDN templates."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "assets" / "icons" / "manifest.yaml"
WL = ROOT / "assets" / "icons" / "metadata" / "official_whitelist.yaml"
CP = ROOT / "assets" / "icons" / "client_profiles.yaml"

CDN = "https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Collection@main/assets/icons/png/{size}/{icon_key}.png"
RAW = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/{size}/{icon_key}.png"
MONO = "https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Collection@main/assets/icons/monochrome/{size}/{icon_key}.png"


def main() -> int:
    if not WL.exists():
        print("[icon_p0_p1] no whitelist, skip")
        return 0
    wl = yaml.safe_load(WL.read_text(encoding="utf-8")) or {}
    official = wl.get("verified_official") or {}
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.setdefault("icons", {})
    n = 0
    for key, info in official.items():
        meta = icons.get(key)
        if not isinstance(meta, dict):
            continue
        if not isinstance(info, dict):
            info = {}
        src = meta.setdefault("source", {})
        src["provenance"] = src.get("provenance") or "official-colors"
        src["verified"] = True
        src["whitelist"] = True
        if info.get("kit"):
            src["media_kit"] = info["kit"]
        meta["status"] = "verified"
        if info.get("approved_mono"):
            meta.setdefault("visual", {})["approved_mono"] = True
        icons[key] = meta
        n += 1
    man["icons"] = icons
    man["updated"] = str(date.today())
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")

    if CP.exists():
        cp = yaml.safe_load(CP.read_text(encoding="utf-8")) or {}
        cp["cdn"] = {
            "primary": "jsdelivr",
            "url_template": CDN,
            "fallback_raw": RAW,
            "mono_template": MONO,
        }
        for conf in (cp.get("clients") or {}).values():
            if not isinstance(conf, dict):
                continue
            conf["url_template"] = CDN
            conf["url_template_fallback"] = RAW
            conf["mono_url_template"] = MONO
        cp["updated"] = str(date.today())
        CP.write_text(yaml.dump(cp, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    print(f"[icon_p0_p1] whitelist_applied={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
