"""Golden L1–L7 against V2 oracle where applicable."""
from __future__ import annotations

import json
from pathlib import Path


def run_golden(root: Path) -> dict:
    data = root / "data" / "v3"
    reports = data / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    results = []

    l1 = {
        "level": "L1_structural",
        "pass": (data / "canonical" / "manifest.json").exists()
        and ((data / "artifacts" / "manifest.json").exists() or (data / "artifacts" / "mihomo").is_dir()),
        "detail": "canonical + artifacts layout",
    }
    results.append(l1)

    hier = reports / "hierarchy_summary.json"
    l2_pass = False
    if hier.exists():
        doc = json.loads(hier.read_text())
        l2_pass = all(isinstance(v.get("sha256"), str) and len(v.get("sha256") or "") == 64 for v in doc.values())
    results.append({"level": "L2_semantic", "pass": l2_pass, "detail": "hierarchy sha256 present"})

    glist = data / "artifacts" / "mihomo" / "google.list"
    results.append({"level": "L3_behavioral", "pass": glist.exists() and glist.stat().st_size > 0, "detail": "mihomo google.list"})

    diff_path = reports / "differential.json"
    l4 = l5 = False
    if diff_path.exists():
        d = json.loads(diff_path.read_text())
        l4 = bool(d.get("all_rules_match"))
        rows = d.get("rows") or []
        l5 = bool(rows) and all(r.get("sha_match") for r in rows)
    results.append({"level": "L4_hierarchical", "pass": l4, "detail": "aggregate rules_match"})
    results.append({"level": "L5_legacy", "pass": l5, "detail": "aggregate sha_match"})

    clients = ("mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon")
    missing = [c for c in clients if not (data / "artifacts" / c).is_dir() or not any((data / "artifacts" / c).glob("*.list"))]
    results.append({"level": "L6_cross_client", "pass": len(missing) == 0, "detail": f"missing={missing}" if missing else "7 clients"})
    results.append({"level": "L7_reproducibility", "pass": hier.exists() and l2_pass, "detail": "hierarchy digests"})

    hard = sum(1 for r in results if not r["pass"])
    report = {"results": results, "hard_failures": hard, "pass": hard == 0, "schema": "v3_golden_l1_l7"}
    (reports / "golden_l1_l7.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
