#!/usr/bin/env python3
"""Phase O: observation/freeze/retirement guard. Never deletes the old root."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def y(p:Path)->dict: return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--state",required=True,choices=["CUTOVER_EXECUTED","OBSERVING","FROZEN_OLD_ROOT","RETIRED"])
    ap.add_argument("--runs",type=int,default=0)
    ap.add_argument("--approve-retirement",action="store_true")
    ap.add_argument("--json-out",type=Path,default=None)
    args=ap.parse_args(); c=y(ROOT/"config/phase_o_observation_retirement.yaml"); errors=[]
    minimum=int((c.get("observation") or {}).get("minimum_runs",3))
    if args.state in {"OBSERVING","FROZEN_OLD_ROOT","RETIRED"} and args.runs<minimum: errors.append(f"observation runs={args.runs}, minimum={minimum}")
    if args.state=="RETIRED" and not args.approve_retirement: errors.append("retirement requires explicit operator approval")
    payload={"schema":"phase_o_observation_retirement_gate_v1","state":args.state,"runs":args.runs,"automatic_delete":False,"pass":not errors,"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
