#!/usr/bin/env python3
"""Phase A: record an immutable current-state health baseline."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p:Path)->dict: return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--expected-head",default="")
    ap.add_argument("--json-out",type=Path,default=None)
    args=ap.parse_args(); errors=[]
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    if args.expected_head and head!=args.expected_head: errors.append(f"HEAD mismatch: {head} != {args.expected_head}")
    latest=read(ROOT/"reports/latest_release.json"); promotion=read(ROOT/"generated/_promotion/latest.json")
    release_path=ROOT/"reports/latest_release.json"; promotion_path=ROOT/"generated/_promotion/latest.json"
    if not release_path.is_file(): errors.append("missing reports/latest_release.json")
    if not promotion_path.is_file(): errors.append("missing generated/_promotion/latest.json")
    run_id=latest.get("run_id")
    checks=[(latest.get("release_state")=="RC_READY","latest release_state"),(latest.get("quality_score")==100,"latest quality_score"),(latest.get("cas_verified") is True,"latest cas_verified"),(promotion.get("release_state")=="RC_READY","promotion release_state"),(promotion.get("v2_runtime_dependency")==0,"promotion v2_runtime_dependency"),(promotion.get("run_id")==run_id,"release/promotion run_id")]
    for ok,label in checks:
        if not ok: errors.append(f"{label} check failed")
    if latest.get("snapshot_id")!=promotion.get("snapshot_id"): errors.append("release/promotion snapshot_id mismatch")
    if latest.get("canonical_digest")!=promotion.get("baseline_digest"): errors.append("release/promotion canonical digest mismatch")
    legacy=ROOT/"database"/"services"
    if legacy.exists(): errors.append("Legacy database/services still exists after deletion")
    payload={"schema":"phase_a_current_health_v2","head":head,"latest_run_id":run_id,"snapshot_id":latest.get("snapshot_id"),"canonical_digest":latest.get("canonical_digest"),"ir_digest":latest.get("ir_digest"),"golden_digest":latest.get("golden_digest"),"client_digests":latest.get("client_digests") or {}, "determinism_artifact_digest":None,"release_state":latest.get("release_state"),"quality_score":latest.get("quality_score"),"cas_verified":latest.get("cas_verified"),"artifact_count":promotion.get("artifact_count"),"legacy_database_services_exists":legacy.exists(),"pass":not errors,"errors":errors}
    det=read(ROOT/"reports/v1/V3_DETERMINISM_FINAL.json")
    payload["determinism_artifact_digest"]=(det.get("builds") or [{}])[0].get("artifacts") if det.get("builds") else None
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
