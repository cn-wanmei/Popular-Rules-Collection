#!/usr/bin/env python3
"""Validate that every human rule entity has an explicit provider mapping."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[1]
def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict): raise ValueError(f"expected mapping: {path}")
    return data
def hierarchy_services(path: Path) -> dict[str, str]:
    doc = load_yaml(path); out: dict[str,str] = {}
    for provider, meta in (doc.get("providers") or {}).items():
        if not isinstance(meta, dict): continue
        for service in (meta.get("services") or {}):
            sid=str(service).strip()
            if sid in out and out[sid] != str(provider):
                raise ValueError(f"service {sid!r} declared by multiple providers: {out[sid]!r}, {provider!r}")
            out[sid]=str(provider)
    return out
def unmapped_entries(rule_root: Path)->list[str]:
    target=rule_root/"unmapped"
    if not target.is_dir(): return []
    out=[]
    for p in sorted(target.iterdir(), key=lambda x:x.name.casefold()):
        if p.name in {"README.md","_index.yaml","manifest.json"}: continue
        if p.is_dir() and any(x.is_file() for x in p.rglob("*")): out.append(p.name)
        elif p.is_file() and p.suffix in {".yaml",".yml",".json"}: out.append(p.stem)
    return out
def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root",type=Path,default=ROOT)
    ap.add_argument("--require-empty",action="store_true")
    args=ap.parse_args()
    root=args.root.resolve()
    services=hierarchy_services(root/"config/ruleset_hierarchy.yaml")
    names=unmapped_entries(root/"rule")
    unknown=sorted(set(names)-set(services), key=str.casefold)
    errors=[]
    if unknown: errors.append("unmapped services missing from explicit hierarchy: "+", ".join(unknown))
    if args.require_empty and names: errors.append("rule/unmapped is not empty after mapping: "+", ".join(names))
    report={"schema":"rule_mapping_gate_v1","pass":not errors,"declared_service_count":len(services),"unmapped_entries":names,"unknown_unmapped_entries":unknown,"require_empty":args.require_empty}
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
