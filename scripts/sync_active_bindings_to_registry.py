#!/usr/bin/env python3
"""Align registry/primary/hierarchy with active immutable bindings (post-handoff)."""
from __future__ import annotations
import sys
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
IM = ROOT / "sources" / "immutable_registry.yaml"
REG = ROOT / "sources" / "registry.yaml"
PRI = ROOT / "config" / "service_primary.yaml"
HIER = ROOT / "config" / "ruleset_hierarchy.yaml"


def main() -> int:
    im = yaml.safe_load(IM.read_text(encoding="utf-8")) or {}
    active = sorted(
        str(k)
        for k, v in (im.get("bindings") or {}).items()
        if isinstance(v, dict) and v.get("status") == "active"
    )
    reg = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    src = next(s for s in reg.get("sources") or [] if s.get("id") == "popular-rules-source")
    rules = src.setdefault("rules", [])
    by = {str(r.get("service")): r for r in rules}
    enabled = added = 0
    for sid in active:
        if sid in by:
            if by[sid].get("enabled") is not True:
                by[sid]["enabled"] = True
                enabled += 1
        else:
            rules.append(
                {
                    "path": f"generated/source/{sid}/domains.txt",
                    "name": sid,
                    "service": sid,
                    "local": f"PRS_{sid}.domains.txt",
                    "enabled": True,
                }
            )
            added += 1
    reg["last_updated"] = __import__("datetime").date.today().isoformat()
    REG.write_text(yaml.safe_dump(reg, allow_unicode=True, sort_keys=False), encoding="utf-8")

    pri = yaml.safe_load(PRI.read_text(encoding="utf-8")) or {}
    services = pri.setdefault("services", {})
    pri_added = 0
    for sid in active:
        if sid not in services:
            services[sid] = {
                "primary_category": "other",
                "display_name": sid,
                "categories": ["other"],
                "service_type": "service",
            }
            pri_added += 1
    pri["updated"] = __import__("datetime").date.today().isoformat()
    PRI.write_text(yaml.safe_dump(pri, allow_unicode=True, sort_keys=False), encoding="utf-8")

    hier = yaml.safe_load(HIER.read_text(encoding="utf-8")) or {}
    prov = hier.setdefault("providers", {})
    hier_ids = set()
    for pv in prov.values():
        if not isinstance(pv, dict):
            continue
        if pv.get("aggregate"):
            hier_ids.add(str(pv["aggregate"]))
        for sid in (pv.get("services") or {}):
            hier_ids.add(str(sid))
    hier_added = 0
    for sid in active:
        if sid in hier_ids:
            continue
        prov[sid] = {"display_name": sid, "aggregate": sid, "services": {}}
        hier_added += 1
    HIER.write_text(yaml.safe_dump(hier, allow_unicode=True, sort_keys=False), encoding="utf-8")

    print(
        f"sync_active_bindings: active={len(active)} reg_enabled={enabled} "
        f"reg_added={added} primary_added={pri_added} hierarchy_added={hier_added}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
