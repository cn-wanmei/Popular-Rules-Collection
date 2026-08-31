#!/usr/bin/env python3
"""Validate routing contract + priority consistency (V2 hard gate)."""
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

ALLOWED = {"DIRECT", "PROXY", "REJECT"}


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
    if actions != ALLOWED:
        hard.append(f"contract.actions must be {ALLOWED}, got {actions}")

    layers = {x.get("id"): x for x in (c.get("layers") or []) if isinstance(x, dict) and x.get("id")}
    order = r.get("precedence_order") or []
    if not all(x in layers for x in order):
        hard.append("routing_priority precedence_order not subset of contract layers")

    for name, conf in (r.get("intent") or {}).items():
        if not isinstance(conf, dict):
            continue
        act = str(conf.get("action") or "").upper()
        if act and act not in ALLOWED:
            hard.append(f"intent.{name}.action illegal: {act} (not in contract.actions)")
        lay = conf.get("layer")
        if lay and lay not in layers:
            hard.append(f"intent.{name}.layer unknown: {lay}")

    cm = r.get("conflict_matrix") or {}
    for a, row in cm.items():
        if str(a).upper() not in ALLOWED:
            hard.append(f"conflict_matrix key illegal: {a}")
        if isinstance(row, dict):
            for b in row:
                if str(b).upper() not in ALLOWED:
                    hard.append(f"conflict_matrix[{a}] key illegal: {b}")

    term = (c.get("terminal") or {}).get("unmatched") or s.get("default_policy")
    if str(term).upper() not in ALLOWED:
        hard.append(f"terminal unmatched illegal: {term}")

    if not (s.get("routing_refs") or {}).get("contract"):
        warn.append("priority.yaml missing routing_refs.contract")

    print(f"[routing_contract] layers={len(layers)} actions={sorted(actions)} terminal={term}")
    for w in warn:
        print(f"  WARN  {w}")
    for h in hard:
        print(f"  HARD  {h}")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
