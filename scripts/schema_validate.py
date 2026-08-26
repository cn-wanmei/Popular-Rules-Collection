#!/usr/bin/env python3
"""schema_validate.py — categories + service_primary + aggregate children + strict path rules."""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "config" / "categories.yaml"
PRIM = ROOT / "config" / "service_primary.yaml"
SERVICES = ROOT / "database" / "services"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    cats = yaml.safe_load(CAT.read_text(encoding="utf-8")) or {}
    cat_ids = {str(c["id"]) for c in (cats.get("categories") or [])}
    if not cat_ids:
        errors.append("categories.yaml empty")
    prim = yaml.safe_load(PRIM.read_text(encoding="utf-8")) or {}
    services = dict(prim.get("services") or {})
    extra_path = ROOT / "config" / "service_primary_extra.yaml"
    if extra_path.exists():
        extra = yaml.safe_load(extra_path.read_text(encoding="utf-8")) or {}
        services.update(extra.get("services") or {})
        for sid, ov in (extra.get("aggregate_overrides") or {}).items():
            if sid in services:
                services[sid].update(ov)
            else:
                services[sid] = ov
    if not services:
        errors.append("service_primary.yaml empty")

    for sid, meta in services.items():
        if not isinstance(meta, dict):
            errors.append(f"{sid}: mapping must be object")
            continue
        pc = meta.get("primary_category")
        if not pc:
            errors.append(f"{sid}: missing primary_category")
        elif str(pc) not in cat_ids:
            errors.append(f"{sid}: primary_category '{pc}' not in categories.yaml")
        st = meta.get("service_type", "service")
        if st not in ("service", "aggregate"):
            errors.append(f"{sid}: invalid service_type '{st}'")
        children = meta.get("children")
        if st == "aggregate":
            if not children:
                warnings.append(f"{sid}: aggregate without children (display-only aggregate)")
            else:
                for c in children:
                    if c not in services:
                        errors.append(f"{sid}: child '{c}' not defined in service_primary")
                    else:
                        child = services[c]
                        # child should prefer same ecosystem or documented parent
                        if child.get("parent") and child.get("parent") != sid:
                            warnings.append(f"{sid}: child {c} parent={child.get('parent')} mismatch")
        elif children:
            errors.append(f"{sid}: service_type=service must not have children")
        parent = meta.get("parent")
        if parent:
            if parent not in services:
                errors.append(f"{sid}: parent '{parent}' missing")
            elif services[parent].get("service_type") != "aggregate":
                errors.append(f"{sid}: parent '{parent}' is not aggregate")

    # database services should be mapped when present
    if SERVICES.is_dir():
        for p in SERVICES.glob("*.yaml"):
            if p.name.startswith("example"):
                continue
            sid = p.stem
            if sid not in services:
                errors.append(f"database service '{sid}' missing from service_primary.yaml")

    print(f"[schema_validate] errors={len(errors)} warnings={len(warnings)}")
    for e in errors[:40]:
        print(f"  ERROR {e}")
    for w in warnings[:20]:
        print(f"  WARN  {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
