#!/usr/bin/env python3
"""V2.5 hierarchy_validate."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SM = ROOT / "config" / "service_model"


def load(name: str) -> dict:
    p = SM / name
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def main() -> int:
    errs, warns = [], []
    providers = load("providers.yaml").get("providers") or {}
    services = load("services.yaml").get("services") or {}
    groups = load("groups.yaml").get("groups") or {}
    aggregates = load("memberships.yaml").get("aggregates") or {}
    aliases = load("aliases.yaml").get("aliases") or {}

    for aid, a in aliases.items():
        can = (a or {}).get("canonical")
        if not can:
            errs.append(f"alias {aid}: missing canonical")
        elif can in aliases:
            errs.append(f"alias chain forbidden: {aid} → {can}")

    for gid, g in groups.items():
        for m in (g or {}).get("members") or []:
            if m not in services and m not in groups:
                errs.append(f"ghost group member: {gid} → {m}")
        for m in (g or {}).get("members") or []:
            if m in groups:
                for s in (groups[m] or {}).get("members") or []:
                    if s in groups:
                        errs.append(f"group depth>2: {gid} → {m} → {s}")

    for vid, v in aggregates.items():
        members = (v or {}).get("members") or []
        if not members:
            errs.append(f"aggregate {vid}: empty members")
        for m in members:
            if m not in services and m not in groups:
                errs.append(f"ghost aggregate member: {vid} → {m}")
        if (v or {}).get("source"):
            errs.append(f"aggregate {vid} must not own source")

    for sid, s in services.items():
        if (s or {}).get("provider") and (s or {}).get("provider") not in providers:
            errs.append(f"service {sid}: unknown provider")
        if (s or {}).get("source"):
            errs.append(f"service {sid} must not own source")

    print(f"[hierarchy_validate] errors={len(errs)} warnings={len(warns)}")
    for e in errs:
        print(f"  ERROR {e}")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
