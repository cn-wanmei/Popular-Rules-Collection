#!/usr/bin/env python3
"""Phase M: semantic dual-track verifier. Path identity is not equivalence."""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
REQUIRED=("service_identities","asset_identities","memberships","dependency_closures","aggregate_closures","network_references","final_ir_digest","artifact_digest")
def load(p:Path)->dict:
    v=json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(v,dict): raise ValueError("semantic inventory must be an object")
    return v
def digest(v:dict)->str:
    blob=json.dumps({k:v.get(k) for k in REQUIRED},ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(blob).hexdigest()
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("left",type=Path); ap.add_argument("right",type=Path); ap.add_argument("--json-out",type=Path,default=None)
    args=ap.parse_args(); left=load(args.left); right=load(args.right); errors=[]
    for label,v in (("left",left),("right",right)):
        miss=[k for k in REQUIRED if k not in v]
        if miss: errors.append(f"{label}: missing sections {miss}")
    for key in REQUIRED:
        if left.get(key)!=right.get(key): errors.append(f"semantic mismatch: {key}")
    ld,rd=digest(left),digest(right)
    if ld!=rd: errors.append("semantic manifest digest mismatch")
    payload={"schema":"phase_m_dual_track_report_v1","left_digest":ld,"right_digest":rd,"pass":not errors,"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
