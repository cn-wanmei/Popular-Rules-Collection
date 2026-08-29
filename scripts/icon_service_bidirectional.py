#!/usr/bin/env python3
"""Service ↔ Icon bidirectional QA (Schema V2)."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "assets" / "icons" / "manifest.yaml"
CFG = ROOT / "config" / "icons.yaml"
PRIM = ROOT / "config" / "service_primary.yaml"
EXTRA = ROOT / "config" / "service_primary_extra.yaml"
INTENT = ROOT / "config" / "intentional_unmaterialized.yaml"
OUT = ROOT / "reports" / "latest_icon_service_bidirectional.json"


def load(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def main() -> int:
    man = load(MAN)
    icons = man.get("icons") or {}
    smap = man.get("service_icon_map") or {}
    prim = load(PRIM).get("services") or {}
    extra = load(EXTRA).get("services") or {}
    services = {**prim, **extra}
    intent = set((load(INTENT).get("services") or {}).keys())
    hard: list[str] = []
    warn: list[str] = []

    for sid in sorted(services.keys()):
        if sid in intent:
            continue
        iid = smap.get(sid)
        if not iid:
            cfg = load(CFG).get("icons") or {}
            if sid in cfg:
                continue
            hard.append(f"service {sid}: no icon mapping")
            continue
        if iid != "placeholder" and iid not in icons:
            hard.append(f"service {sid}: icon_id {iid} missing in manifest")

    for iid, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        if meta.get("namespace") in ("policy", "dataset", "network"):
            continue
        sids = meta.get("service_ids") or ([iid] if iid in services else [])
        for sid in sids:
            if sid not in services and sid not in smap:
                warn.append(f"icon {iid}: service_id {sid} not in service registry")

    reverse = set(smap.values())
    for iid in icons:
        if iid not in reverse and iid != "placeholder" and (icons.get(iid) or {}).get("namespace") == "brand":
            warn.append(f"icon {iid}: no service_icon_map reverse ref")

    status = "fail" if hard else ("warn" if warn else "pass")
    doc = {"status": status, "hard": hard, "warn": warn[:50], "services": len(services), "icons": len(icons), "mapped": len(smap)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[icon_service_bidirectional] status={status} hard={len(hard)} warn={len(warn)}")
    for x in hard[:15]:
        print(f"  HARD  {x}")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
