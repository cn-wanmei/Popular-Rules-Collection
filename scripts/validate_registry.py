#!/usr/bin/env python3
"""validate_registry.py — Registry names ⊆ Primary (anti-orphan gate).

Core invariant:
  R = service IDs declared in sources/registry.yaml rules[].name
  P = service IDs in service_primary.yaml ∪ service_primary_extra.yaml
  Must: R ⊆ P

Also checks light structural integrity of primary (parent/children/service_type).
Does NOT replace schema_validate (which checks database/services presence).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "sources" / "registry.yaml"
PRIM = ROOT / "config" / "service_primary.yaml"
EXTRA = ROOT / "config" / "service_primary_extra.yaml"
CAT = ROOT / "config" / "categories.yaml"


def load_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def primary_map() -> dict[str, dict]:
    prim = load_yaml(PRIM)
    services = dict(prim.get("services") or {})
    extra = load_yaml(EXTRA)
    services.update(extra.get("services") or {})
    for sid, ov in (extra.get("aggregate_overrides") or {}).items():
        base = dict(services.get(sid) or {})
        base.update(ov)
        services[sid] = base
    # apply defaults
    defaults = prim.get("defaults") or {}
    out: dict[str, dict] = {}
    for sid, meta in services.items():
        m = dict(defaults)
        if isinstance(meta, dict):
            m.update(meta)
        out[str(sid)] = m
    return out


def registry_service_ids() -> set[str]:
    reg = load_yaml(REG)
    ids: set[str] = set()
    for src in reg.get("sources") or []:
        for r in src.get("rules") or src.get("files") or []:
            if not isinstance(r, dict):
                continue
            name = r.get("name") or r.get("service")
            if not name:
                continue
            sid = str(name).lower().strip()
            # strip common client prefixes if any
            for prefix in ("clash_", "surge_"):
                if sid.startswith(prefix):
                    sid = sid[len(prefix) :]
            if sid.endswith((".yaml", ".list", ".txt", ".conf")):
                sid = Path(sid).stem
            ids.add(sid)
    return ids


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    cats = load_yaml(CAT)
    cat_ids = {str(c["id"]) for c in (cats.get("categories") or [])}
    P = primary_map()
    R = registry_service_ids()

    if not R:
        errors.append("registry has no rule names")
    if not P:
        errors.append("service_primary is empty")

    # Core: R ⊆ P
    orphans = sorted(R - set(P.keys()))
    for oid in orphans:
        errors.append(f"registry service has no primary: {oid}")

    # Light primary structure
    for sid, meta in P.items():
        pc = meta.get("primary_category")
        if not pc:
            errors.append(f"{sid}: missing primary_category")
        elif cat_ids and str(pc) not in cat_ids:
            errors.append(f"{sid}: primary_category '{pc}' not in categories.yaml")
        st = meta.get("service_type", "service")
        if st not in ("service", "aggregate"):
            errors.append(f"{sid}: invalid service_type '{st}'")
        children = meta.get("children") or []
        if st == "aggregate":
            if not children:
                warnings.append(f"{sid}: aggregate without children")
            for c in children:
                if c not in P:
                    errors.append(f"{sid}: child '{c}' not in primary")
        elif children:
            errors.append(f"{sid}: service_type=service must not have children")
        parent = meta.get("parent")
        if parent:
            if parent not in P:
                errors.append(f"{sid}: parent '{parent}' not in primary")
            elif P[parent].get("service_type", "service") != "aggregate":
                errors.append(f"{sid}: parent '{parent}' is not aggregate")

    # IDs only in primary (ok) — optional info
    only_p = sorted(set(P.keys()) - R)
    if only_p:
        warnings.append(
            f"{len(only_p)} primary-only ids (not in registry rules) — ok if intentional"
        )

    print(f"[validate_registry] registry={len(R)} primary={len(P)} "
          f"orphans={len(orphans)} errors={len(errors)} warnings={len(warnings)}")
    for e in errors[:50]:
        print(f"  ERROR {e}")
    for w in warnings[:20]:
        print(f"  WARN  {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
