#!/usr/bin/env python3
"""icon_client_adapter.py — per-client icon URL templates (CDN primary + raw fallback)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
CLIENT = ICON / "client_profiles.yaml"
OUT = ROOT / "reports" / "icon_client_urls.json"

sys.path.insert(0, str(ROOT / "scripts"))
from icon_resolver import resolve  # noqa: E402

SAMPLES = ("google", "wechat", "apple", "direct", "lan", "proxy", "china", "12306")
DEFAULT_CDN = "https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Collection@main/assets/icons/png/{size}/{icon_key}.png"
DEFAULT_RAW = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/{size}/{icon_key}.png"


def main() -> int:
    doc = yaml.safe_load(CLIENT.read_text(encoding="utf-8")) or {}
    clients = doc.get("clients") or {}
    cdn = doc.get("cdn") or {}
    out = {
        "version": 2,
        "cdn": {
            "primary": cdn.get("primary") or "jsdelivr",
            "url_template": cdn.get("url_template") or DEFAULT_CDN,
            "fallback_raw": cdn.get("fallback_raw") or DEFAULT_RAW,
        },
        "clients": {},
        "samples": {},
    }
    for cname, cmeta in clients.items():
        cmeta = cmeta or {}
        profile = str(cmeta.get("profile") or "client")
        size = int(cmeta.get("preferred_size") or 256)
        tmpl = cmeta.get("url_template") or cdn.get("url_template") or DEFAULT_CDN
        fb = cmeta.get("url_template_fallback") or cdn.get("fallback_raw") or DEFAULT_RAW
        out["clients"][cname] = {
            "profile": profile,
            "size": size,
            "url_template": tmpl,
            "url_template_fallback": fb,
            "mono_url_template": cmeta.get("mono_url_template") or cdn.get("mono_template"),
            "note": "CDN primary; raw fallback. Do not embed icons in rule lists.",
        }
    for sid in SAMPLES:
        out["samples"][sid] = resolve(sid, profile="client")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[icon_client_adapter] clients={len(out['clients'])} samples={len(SAMPLES)} → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
