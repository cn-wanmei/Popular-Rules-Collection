#!/usr/bin/env python3
"""Validate config/profiles.yaml structure (v2)."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "config" / "profiles.yaml"
KNOWN_DS = {"system", "china", "gfw", "proxy", "lan", "private"}


def main() -> int:
    hard, warn = [], []
    if not PATH.exists():
        print("  HARD  missing profiles.yaml")
        return 1
    doc = yaml.safe_load(PATH.read_text(encoding="utf-8")) or {}
    profiles = doc.get("profiles") or {}
    if not profiles:
        hard.append("no profiles")
    for name, p in profiles.items():
        if not isinstance(p, dict):
            hard.append(f"{name}: not a mapping")
            continue
        r = p.get("routing") or {}
        if r and r.get("terminal") not in (None, "PROXY", "DIRECT", "REJECT"):
            hard.append(f"{name}: bad terminal {r.get('terminal')}")
        for d in p.get("datasets") or []:
            if d not in KNOWN_DS:
                warn.append(f"{name}: unknown dataset {d}")
        for x in (p.get("policies") or {}).get("reject") or []:
            if x not in ("security", "ad", "tracker"):
                warn.append(f"{name}: unknown reject {x}")
        svc = p.get("services")
        if svc is None:
            warn.append(f"{name}: no services key")
        elif svc != "*" and not isinstance(svc, list):
            hard.append(f"{name}: services must be list or '*'")
    print(f"[profile_validate] profiles={len(profiles)} hard={len(hard)} warn={len(warn)}")
    for h in hard:
        print(f"  HARD  {h}")
    for w in warn[:10]:
        print(f"  WARN  {w}")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
