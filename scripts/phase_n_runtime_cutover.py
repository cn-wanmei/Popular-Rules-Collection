#!/usr/bin/env python3
"""Phase N: runtime cutover authorization gate; never performs cutover."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def y(p:Path)->dict: return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",type=Path,required=True)
    ap.add_argument("--approve",action="store_true")
    ap.add_argument("--json-out",type=Path,default=None)
    args=ap.parse_args(); c=y(ROOT/"config/phase_n_runtime_cutover.yaml"); errors=[]
    if c.get("status")!="AUTHORIZED": errors.append("cutover config is not AUTHORIZED")
    if c.get("execution",{}).get("explicit_single_cutover_commit") is not True: errors.append("single cutover commit requirement missing")
    if not args.approve: errors.append("operator approval was not supplied")
    if not args.evidence.is_file(): errors.append("evidence bundle is missing")
    payload={"schema":"phase_n_runtime_cutover_gate_v1","status":c.get("status"),"authorized":not errors,"cutover_performed":False,"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
