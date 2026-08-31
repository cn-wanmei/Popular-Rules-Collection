#!/usr/bin/env python3
"""Validate routing contract + priority + resolution files."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config" / "routing_contract.yaml"
PRIORITY = ROOT / "config" / "routing_priority.yaml"
SRC_PRI = ROOT / "config" / "priority.yaml"
REJECT = ROOT / "database" / "policies" / "reject" / "manifest.yaml"
OVERRIDES = ROOT / "database" / "policies" / "overrides" / "manifest.yaml"
RESOLUTION = ROOT / "config" / "resolution_policy.yaml"


def main() -> int:
    hard: list[str] = []
    warn: list[str] = []
    for p in (CONTRACT, PRIORITY, SRC_PRI, REJECT, OVERRIDES, RESOLUTION):
        if not p.exists():
            hard.append(f"missing {p.relative_to(ROOT)}")
    if hard:
        for h in hard:
            print(f"  HARD  {h}")
        return 1
    c = yaml.safe_load(CONTRACT.read_text(encoding="utf-8")) or {}
    r = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    s = yaml.safe_load(SRC_PRI.read_text(encoding="utf-8")) or {}
    actions = set(c.get("actions") or [])
    if actions != {"DIRECT", "PROXY", "REJECT"}:
        hard.append(f"actions must be DIRECT/PROXY/REJECT, got {actions}")
    term = (c.get("terminal") or {}).get("unmatched") or s.get("default_policy")
    if term != "PROXY":
        warn.append(f"terminal unmatched={term} (expected PROXY for this project)")
    layers = [x.get("id") for x in (c.get("layers") or []) if isinstance(x, dict)]
    order = r.get("precedence_order") or []
    if order and layers and not all(x in layers for x in order):
        hard.append("routing_priority precedence_order not subset of contract layers")
    refs = s.get("routing_refs") or {}
    if not refs.get("contract"):
        warn.append("priority.yaml missing routing_refs.contract")
    print(f"[routing_contract] layers={len(layers)} actions={sorted(actions)} terminal={term}")
    for w in warn:
        print(f"  WARN  {w}")
    for h in hard:
        print(f"  HARD  {h}")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
