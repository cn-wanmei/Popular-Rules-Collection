#!/usr/bin/env python3
"""Phase J: strict P0 50-service production readiness gate."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
GATES = ("identity","source","canonical","semantic_audit","overlap_audit","seven_client","golden","release")

def y(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--enforce", action="store_true")
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()
    errors=[]
    ids=[str(x["id"]) for x in y(ROOT/"config/p0_materialization.yaml").get("services",[]) if isinstance(x,dict) and x.get("id")]
    identity=[str(x["id"]) for x in y(ROOT/"config/p0_service_identity.yaml").get("services",[]) if isinstance(x,dict) and x.get("id")]
    matrix=y(ROOT/"config/p0_service_production.yaml").get("services") or {}
    batches=y(ROOT/"config/phase_j_p0_batch_plan.yaml").get("batches") or {}
    plan_ids=[sid for group in batches.values() for sid in group]
    if len(ids)!=50 or len(set(ids))!=50: errors.append("P0 queue must contain exactly 50 unique services")
    if len(batches)!=5 or any(len(group)!=10 for group in batches.values()): errors.append("batch plan must be exactly 5×10")
    if set(plan_ids)!=set(ids): errors.append("batch plan does not cover exactly the P0 queue")
    if set(identity)!=set(ids): errors.append("identity mapping does not exactly match P0 queue")
    if set(matrix)!=set(ids): errors.append("production matrix does not exactly match P0 queue")
    status={}
    for sid in ids:
        row=matrix.get(sid) or {}
        failed=[g for g in GATES if row.get(g)!="pass"]
        status[sid]={"status":row.get("status"),"failed_gates":failed}
    production=[sid for sid in ids if status[sid]["status"]=="production" and not status[sid]["failed_gates"]]
    blocked=[sid for sid in ids if sid not in production]
    payload={
        "schema":"phase_j_p0_50_gate_v1",
        "queue_size":len(ids),
        "production_count":len(production),
        "blocked_count":len(blocked),
        "production_complete":len(production)==50,
        "batches":{k:len(v) for k,v in batches.items()},
        "blocked":{sid:status[sid]["failed_gates"] or ["status!=production"] for sid in blocked},
        "pass":not errors and (len(production)==50 if args.enforce else True),
        "errors":errors
    }
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"
    print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(out,encoding="utf-8")
    return 0 if payload["pass"] else 1

if __name__=="__main__":
    raise SystemExit(main())
