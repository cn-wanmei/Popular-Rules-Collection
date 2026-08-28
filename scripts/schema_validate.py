#!/usr/bin/env python3
"""schema_validate.py — Primary mapping + database service rule schema (P1-0).

categories + service_primary + aggregate children
+ database/services/{id}.yaml: id==stem, canonical types, non-empty values
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "config" / "categories.yaml"
PRIM = ROOT / "config" / "service_primary.yaml"
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"

# Keep in sync with scripts/rule_loader.py TYPED_KEYS (+ process_name for future)
CANONICAL_TYPES = frozenset(
    {
        "domain",
        "domain_suffix",
        "domain_keyword",
        "domain_regex",
        "ip_cidr",
        "ip_cidr6",
        "process_name",
    }
)


def validate_service_file(path: Path, errors: list[str], warnings: list[str]) -> None:
    """P1-0: structural integrity of one database service YAML."""
    sid = path.stem
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        errors.append(f"{sid}: invalid YAML ({e})")
        return
    if not isinstance(doc, dict):
        errors.append(f"{sid}: document must be a mapping")
        return

    rid = doc.get("id")
    if not rid:
        errors.append(f"{sid}: missing id")
    elif str(rid) != sid:
        errors.append(f"{sid}: id '{rid}' != filename stem")

    rules = doc.get("rules")
    if rules is None:
        warnings.append(f"{sid}: missing rules key (expected list, possibly empty)")
        rules = []
    elif not isinstance(rules, list):
        errors.append(f"{sid}: rules must be a list")
        return

    for i, r in enumerate(rules):
        if not isinstance(r, dict):
            errors.append(f"{sid}: rules[{i}] must be object")
            continue
        t = (r.get("type") or "").lower().strip()
        v = r.get("value")
        if not t:
            errors.append(f"{sid}: rules[{i}] missing type")
        elif t not in CANONICAL_TYPES:
            errors.append(f"{sid}: rules[{i}] type '{t}' not in canonical set")
        if v is None or (isinstance(v, str) and not v.strip()):
            errors.append(f"{sid}: rules[{i}] empty value")

    has_sidecar = False
    if (DOMAINS / f"{sid}.txt").exists() and (DOMAINS / f"{sid}.txt").stat().st_size > 0:
        has_sidecar = True
    if (IPS / f"{sid}.txt").exists() and (IPS / f"{sid}.txt").stat().st_size > 0:
        has_sidecar = True
    if not rules and not has_sidecar:
        warnings.append(f"{sid}: empty rules and no domains/ips sidecar")


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
                        if child.get("parent") and child.get("parent") != sid:
                            warnings.append(
                                f"{sid}: child {c} parent={child.get('parent')} mismatch"
                            )
        elif children:
            errors.append(f"{sid}: service_type=service must not have children")
        parent = meta.get("parent")
        if parent:
            if parent not in services:
                errors.append(f"{sid}: parent '{parent}' missing")
            elif services[parent].get("service_type") != "aggregate":
                errors.append(f"{sid}: parent '{parent}' is not aggregate")

    if SERVICES.is_dir():
        for p in sorted(SERVICES.glob("*.yaml")):
            if p.name.startswith("example"):
                continue
            sid = p.stem
            if sid not in services:
                errors.append(f"database service '{sid}' missing from service_primary.yaml")
            validate_service_file(p, errors, warnings)

    print(f"[schema_validate] errors={len(errors)} warnings={len(warnings)}")
    for e in errors[:40]:
        print(f"  ERROR {e}")
    for w in warnings[:20]:
        print(f"  WARN  {w}")

    try:
        from datetime import datetime, timezone
        import json
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        out_dir = ROOT / "reports" / day
        out_dir.mkdir(parents=True, exist_ok=True)
        rep = {
            "status": "fail" if errors else "pass",
            "errors": len(errors),
            "warnings": len(warnings),
            "error_samples": errors[:20],
            "warning_samples": warnings[:10],
        }
        (out_dir / "schema_validate.json").write_text(
            json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except Exception:
        pass

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
