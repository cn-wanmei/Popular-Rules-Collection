#!/usr/bin/env python3
"""Phase K: finalize intentional registry classification."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
def y(p:Path)->dict:
    v=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return v if isinstance(v,dict) else {}
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",type=Path,default=None)
    args=ap.parse_args()
    c=y(ROOT/"config/phase_k_intentional_final.yaml")
    reg=y(ROOT/"config/intentional_unmaterialized.yaml").get("services") or {}
    e=c.get("expected") or {}
    mixed=set(map(str,e.get("materialized_and_intentional_ids") or []))
    errors=[]
    if len(reg)!=int(e.get("registry_total",-1)): errors.append(f"registry_total={len(reg)}")
    if not mixed.issubset(reg): errors.append("mixed classification ids missing from registry")
    if len(reg)-len(mixed)!=int(e.get("intentional_only",-1)): errors.append(f"intentional_only={len(reg)-len(mixed)}")
    for sid,item in reg.items():
        if not isinstance(item,dict) or not str(item.get("code") or "").strip() or not str(item.get("reason") or "").strip():
            errors.append(f"{sid}: missing code or reason")
    payload={"schema":"phase_k_intentional_final_report_v1","registry_total":len(reg),"intentional_only":len(reg)-len(mixed),"materialized_and_intentional":sorted(mixed),"pass":not errors,"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"
    print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
