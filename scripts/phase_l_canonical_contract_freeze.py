#!/usr/bin/env python3
"""Phase L: assert the frozen Canonical directory contract is internally consistent."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def y(p:Path)->dict:
    v=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return v if isinstance(v,dict) else {}
def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--json-out",type=Path,default=None); args=ap.parse_args()
    c=y(ROOT/"config/phase_l_canonical_contract_freeze.yaml")
    m=y(ROOT/"config/canonical_root_migration.yaml")
    d=y(ROOT/"config/service_model/directories.yaml")
    errors=[]
    if c.get("contract_status")!="FROZEN": errors.append("Phase L contract is not FROZEN")
    if c.get("layout",{}).get("root")!="rules": errors.append("Phase L root must be rules")
    if m.get("contract_status")!="FROZEN": errors.append("migration config contract_status is not FROZEN")
    if m.get("cutover_authorized") is not False: errors.append("Phase L must not authorize cutover")
    for k,a,b in [
        ("aggregate","provider_aggregate","aggregate"),
        ("service","service","service"),
        ("china","china_aggregate","china"),
        ("rule_file","rule_file","rule_file"),
    ]:
        if c.get("layout",{}).get(a)!=m.get("target_layout",{}).get(b): errors.append(f"layout mismatch: {k}")
    if d.get("root")!="rules": errors.append("directory policy root is not rules")
    if (d.get("layout") or {}).get("aggregate")!=c.get("layout",{}).get("provider_aggregate"): errors.append("directory policy aggregate differs from frozen contract")
    payload={"schema":"phase_l_canonical_contract_freeze_report_v1","status":c.get("contract_status"),"cutover_authorized":m.get("cutover_authorized"),"pass":not errors,"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
