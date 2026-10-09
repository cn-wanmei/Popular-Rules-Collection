#!/usr/bin/env python3
"""Phase E: compare dual-track canonical models semantically, never by path identity."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
SECTIONS=("service_identities","asset_identities","memberships","dependency_closures","aggregate_closures","network_references","final_ir_digest","artifact_digest")
def load(p:Path)->dict:
    v=json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(v,dict): raise ValueError(f"semantic inventory must be an object: {p}")
    return v
def digest(v:dict)->str:
    raw=json.dumps({k:v.get(k) for k in SECTIONS},ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("left_manifest",type=Path)
    ap.add_argument("right_manifest",type=Path)
    ap.add_argument("--json-out",type=Path,default=None)
    ap.add_argument("--diagnostic-path-inventory",action="store_true")
    args=ap.parse_args()
    left,right=load(args.left_manifest),load(args.right_manifest); errors=[]
    for label,v in (("left",left),("right",right)):
        miss=[k for k in SECTIONS if k not in v]
        if miss: errors.append(f"{label}: missing semantic sections {miss}")
    for key in SECTIONS:
        if left.get(key)!=right.get(key): errors.append(f"semantic mismatch: {key}")
    ld,rd=digest(left),digest(right)
    if ld!=rd: errors.append("semantic manifest digest mismatch")
    payload={"schema":"phase_e_dual_track_equivalence_v2","left_digest":ld,"right_digest":rd,"path_inventory_is_non_authoritative":True,"pass":not errors,"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
