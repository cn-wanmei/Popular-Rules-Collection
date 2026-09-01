"""Golden L1–L7."""
from __future__ import annotations
import json
from pathlib import Path

def run_golden(root: Path) -> dict:
    data = root / "data" / "generated"
    reports = data / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    results = []
    results.append({"level": "L1_structural", "pass": (data / "canonical" / "manifest.json").exists() and ((data / "artifacts" / "manifest.json").exists() or (data / "artifacts" / "mihomo").is_dir()), "detail": "canonical + artifacts"})
    hier = reports / "hierarchy_summary.json"
    l2 = False
    if hier.exists():
        doc = json.loads(hier.read_text())
        l2 = all(isinstance(v.get("sha256"), str) and len(v.get("sha256") or "") == 64 for v in doc.values())
    results.append({"level": "L2_semantic", "pass": l2, "detail": "hierarchy sha256"})
    glist = data / "artifacts" / "mihomo" / "google.list"
    results.append({"level": "L3_behavioral", "pass": glist.exists() and glist.stat().st_size > 0, "detail": "mihomo google.list"})
    diff_path = reports / "differential.json"
    l4 = l5 = False
    if diff_path.exists():
        d = json.loads(diff_path.read_text())
        l4 = bool(d.get("all_rules_match"))
        rows = d.get("rows") or []
        l5 = bool(rows) and all(r.get("sha_match") for r in rows)
    results.append({"level": "L4_hierarchical", "pass": l4, "detail": "rules_match"})
    results.append({"level": "L5_legacy", "pass": l5, "detail": "sha_match"})
    clients = ("mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon")
    missing = [c for c in clients if not (data / "artifacts" / c).is_dir() or not any((data / "artifacts" / c).glob("*.list"))]
    results.append({"level": "L6_cross_client", "pass": len(missing) == 0, "detail": "7 clients" if not missing else str(missing)})
    results.append({"level": "L7_reproducibility", "pass": hier.exists() and l2, "detail": "digests"})
    hard = sum(1 for r in results if not r["pass"])
    report = {"results": results, "hard_failures": hard, "pass": hard == 0, "schema": "engine_golden_l1_l7"}
    (reports / "golden_l1_l7.json").write_text(json.dumps(report, indent=2) + "\n")
    return report
