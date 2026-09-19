#!/usr/bin/env python3
"""Phase C/K: validate intentional-unmaterialized registry semantics."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
ALLOWED={"NO_UPSTREAM","COVERED_BY_AGGREGATE","MAPS_TO","DEFERRED_PROFILE","KEYWORD_ONLY","SOURCE_DRIFT"}

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--registry",type=Path,default=ROOT/"config/intentional_unmaterialized.yaml")
    ap.add_argument("--expected-count",type=int,default=37)
    ap.add_argument("--expected-intentional-only",type=int,default=34)
    ap.add_argument("--materialized-and-intentional",nargs="*",default=["adblock-light","adblock-pro","stripe"])
    args=ap.parse_args()
    doc=yaml.safe_load(args.registry.read_text(encoding="utf-8")) or {}
    services=doc.get("services") or {}
    errors=[]; rows=[]
    mixed=set(args.materialized_and_intentional)
    for sid,item in sorted(services.items()):
        item=item or {}
        code=str(item.get("code","")).strip()
        reason=str(item.get("reason","")).strip()
        if code not in ALLOWED: errors.append(f"{sid}: invalid code {code!r}")
        if not reason: errors.append(f"{sid}: missing reason")
        disposition="materialized_and_intentional" if sid in mixed else "intentional_only"
        rows.append({"id":sid,"code":code,"reason":reason,"disposition":disposition})
    if len(rows)!=args.expected_count: errors.append(f"registry count={len(rows)}, expected {args.expected_count}")
    mixed_present={r["id"] for r in rows if r["disposition"]=="materialized_and_intentional"}
    if mixed_present!=mixed: errors.append("materialized_and_intentional ids do not match contract")
    intentional_only=sum(r["disposition"]=="intentional_only" for r in rows)
    if intentional_only!=args.expected_intentional_only: errors.append(f"intentional_only={intentional_only}, expected {args.expected_intentional_only}")
    counts={}
    for row in rows: counts[row["code"]]=counts.get(row["code"],0)+1
    payload={"schema":"phase_c_intentional_audit_v2","registry_total":len(rows),"expected_count":args.expected_count,"intentional_only":intentional_only,"materialized_and_intentional":sorted(mixed_present),"code_counts":counts,"pass":not errors,"errors":errors,"entries":rows}
    print(json.dumps(payload,ensure_ascii=False,indent=2))
    return 0 if not errors else 1

if __name__=="__main__":
    raise SystemExit(main())
