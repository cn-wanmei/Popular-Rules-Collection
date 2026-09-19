#!/usr/bin/env python3
"""Phase G: require determinism evidence bound to the active release baseline."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def j(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--report",type=Path,default=ROOT/"reports/v1/V3_DETERMINISM_FINAL.json")
    ap.add_argument("--baseline",type=Path,required=True)
    ap.add_argument("--json-out",type=Path,default=None)
    args=ap.parse_args()
    errors=[]; head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    report=j(args.report); baseline=j(args.baseline)
    promotion=j(ROOT/"generated/_promotion/latest.json"); release=j(ROOT/"reports/latest_release.json")
    if report.get("all_pass") is not True or report.get("match") is not True: errors.append("determinism report is not green")
    if not report.get("source_run_id") or not report.get("snapshot_id"): errors.append("determinism report lacks run/snapshot binding")
    if not baseline.get("head"): errors.append("baseline lacks bound HEAD")
    if baseline.get("head")!=head: errors.append(f"baseline HEAD mismatch: {baseline.get('head')} != {head}")
    expected_run=release.get("run_id") or promotion.get("run_id")
    expected_snapshot=release.get("snapshot_id") or promotion.get("snapshot_id")
    if report.get("source_run_id")!=expected_run: errors.append("determinism run_id does not match latest release")
    if report.get("snapshot_id")!=expected_snapshot: errors.append("determinism snapshot_id does not match latest release")
    if baseline.get("latest_run_id")!=expected_run: errors.append("baseline run_id does not match latest release")
    if baseline.get("snapshot_id")!=expected_snapshot: errors.append("baseline snapshot_id does not match latest release")
    if baseline.get("canonical_digest")!=release.get("canonical_digest"): errors.append("baseline canonical digest does not match release projection")
    builds=report.get("builds") or []
    if len(builds)<3: errors.append("determinism report must contain production and two replays")
    else:
        if len({str(x.get("artifacts")) for x in builds})!=1: errors.append("artifact digests differ between deterministic builds")
        if len({str(x.get("overall")) for x in builds})!=1: errors.append("overall digests differ between deterministic builds")
    payload={"schema":"phase_g_determinism_guard_v2","head":head,"source_run_id":report.get("source_run_id"),"snapshot_id":report.get("snapshot_id"),"baseline_head":baseline.get("head"),"pass":not errors,"errors":errors}
    out=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; print(out,end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True); args.json_out.write_text(out,encoding="utf-8")
    return 0 if not errors else 1
if __name__=="__main__":
    raise SystemExit(main())
