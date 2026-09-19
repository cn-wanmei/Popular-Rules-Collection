#!/usr/bin/env python3
"""Phase N: fail-closed runtime cutover authorization gate; never performs cutover."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=("phase_i_pass","phase_j_50_of_50","phase_k_pass","phase_l_frozen","phase_m_equivalence_pass","seven_client_pass","determinism_pass","artifact_equivalence_pass")
def y(p:Path)->dict:
    v=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return v if isinstance(v,dict) else {}
def j(p:Path)->dict:
    v=json.loads(p.read_text(encoding="utf-8"))
    return v if isinstance(v,dict) else {}
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",type=Path,required=True)
    ap.add_argument("--approve",action="store_true")
    ap.add_argument("--json-out",type=Path,default=None)
    args=ap.parse_args()
    c=y(ROOT/"config/phase_n_runtime_cutover.yaml"); errors=[]
    evidence=j(args.evidence) if args.evidence.is_file() else {}
    if c.get("status")!="AUTHORIZED": errors.append("cutover config is not AUTHORIZED")
    if c.get("current_root")!="rule" or c.get("target_root")!="rules": errors.append("runtime roots are invalid")
    if c.get("execution",{}).get("explicit_single_cutover_commit") is not True: errors.append("single cutover commit requirement missing")
    if c.get("execution",{}).get("directory_move_in_script") is not False: errors.append("cutover script must not move directories")
    if not args.approve: errors.append("operator approval was not supplied")
    if not args.evidence.is_file(): errors.append("evidence bundle is missing")
    for key in REQUIRED:
        if evidence.get(key) is not True: errors.append(f"evidence {key}=true is required")
    target=ROOT/"rules"; old=ROOT/"rule"
    if not target.is_dir(): errors.append("target rules/ root is missing")
    elif not any(p.is_file() for p in target.rglob("*")): errors.append("target rules/ root is empty")
    if not old.is_dir(): errors.append("old rule/ root must remain during cutover")
    payload={"schema":"phase_n_runtime_cutover_gate_v2","status":c.get("status"),"authorized":not errors,"cutover_performed":False,"required_evidence":{k:evidence.get(k) for k in REQUIRED},"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
