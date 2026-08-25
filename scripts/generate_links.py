#!/usr/bin/env python3
"""generate_links.py — subscription_links.json for all services."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
OUT_DIR = ROOT / "reports" / datetime.now(timezone.utc).strftime("%Y-%m-%d")
CDN = yaml.safe_load((ROOT / "config" / "cdn.yaml").read_text(encoding="utf-8"))

CLIENTS = [
    ("mihomo", "generated/mihomo/{id}.yaml"),
    ("sing-box", "generated/sing-box/{id}.json"),
    ("surge", "generated/surge/{id}.list"),
    ("shadowrocket", "generated/shadowrocket/{id}.list"),
    ("quantumult-x", "generated/quantumult-x/{id}.list"),
    ("egern", "generated/egern/{id}.yaml"),
    ("loon", "generated/loon/{id}.list"),
]


def url(path: str, kind: str) -> str:
    return CDN["mirrors"][kind].format(
        owner=CDN["owner"], repo=CDN["repo"], branch=CDN["branch"], path=path
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = {}
    for p in sorted(SERVICES.glob("*.yaml")):
        if p.name.startswith("example"):
            continue
        sid = p.stem
        clients = {}
        for name, pat in CLIENTS:
            path = pat.format(id=sid)
            clients[name] = {k: url(path, k) for k in CDN["mirrors"]}
            clients[name]["path"] = path
        rows[sid] = clients
    out = OUT_DIR / "subscription_links.json"
    body = json.dumps(rows, indent=2, ensure_ascii=False) + "\n"
    out.write_text(body, encoding="utf-8")
    stable = ROOT / "generated" / "subscription_links.json"
    stable.parent.mkdir(parents=True, exist_ok=True)
    stable.write_text(body, encoding="utf-8")
    print(f"[generate_links] services={len(rows)} → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
