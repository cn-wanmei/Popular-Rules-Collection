#!/usr/bin/env python3
"""icon_client_adapter.py — per-client icon URL templates + sample resolves."""
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


def main() -> int:
    clients = (yaml.safe_load(CLIENT.read_text(encoding="utf-8")) or {}).get("clients") or {}
    out = {"version": 1, "clients": {}, "samples": {}}
    for cname, cmeta in clients.items():
        profile = str((cmeta or {}).get("profile") or "client")
        size = int((cmeta or {}).get("preferred_size") or 256)
        tmpl = (cmeta or {}).get("url_template") or (
            "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/{size}/{icon_key}.png"
        )
        out["clients"][cname] = {
            "profile": profile,
            "size": size,
            "url_template": tmpl,
            "note": "Resolve icon_key via icon_resolver; do not embed in rule lists",
        }
    for sid in SAMPLES:
        out["samples"][sid] = resolve(sid, profile="client")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[icon_client_adapter] clients={len(out['clients'])} samples={len(SAMPLES)} → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
