"""Golden L1–L7 — semantic release gates for the complete client matrix."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _client_artifacts_ok(client_dir: Path, ext: str) -> bool:
    if not client_dir.exists():
        return False
    files = list(client_dir.glob(f"*{ext}"))
    if not files:
        return False
    return all(p.stat().st_size > 0 for p in files)


def run_golden(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    results: dict[str, dict[str, Any]] = {}

    snap_id_file = run_dir / "snapshot_id.txt"
    results["L1_snapshot"] = {
        "pass": snap_id_file.exists() and bool(snap_id_file.read_text(encoding="utf-8").strip()),
        "detail": "snapshot_id present",
    }

    can_manifest = run_dir / "canonical" / "manifest.json"
    can_rules = run_dir / "canonical" / "rules.jsonl"
    can_errors = run_dir / "canonical" / "errors.jsonl"
    l2 = (
        can_manifest.exists()
        and can_rules.exists()
        and can_rules.stat().st_size > 0
        and can_errors.exists()
    )
    results["L2_canonical"] = {
        "pass": l2,
        "detail": "canonical artifacts present and non-empty",
    }

    hier = run_dir / "hierarchy" / "graph.json"
    l3 = False
    if hier.exists():
        try:
            g = json.loads(hier.read_text(encoding="utf-8"))
            l3 = len(g.get("services", {})) > 0
        except json.JSONDecodeError:
            l3 = False
    results["L3_hierarchy"] = {"pass": l3, "detail": "hierarchy services > 0"}

    ir_path = run_dir / "ir" / "ir.json"
    l4 = False
    if ir_path.exists():
        try:
            ir = json.loads(ir_path.read_text(encoding="utf-8"))
            l4 = (
                len(ir.get("entity", {}).get("services", [])) > 0
                and len(ir.get("decisions", [])) > 0
                and ir.get("v2_runtime_dependency") == 0
            )
        except json.JSONDecodeError:
            l4 = False
    results["L4_ir"] = {"pass": l4, "detail": "IR has hierarchy + decisions"}

    art = run_dir / "artifacts"
    expected = {
        "mihomo": ".yaml",
        "singbox": ".json",
        "surge": ".list",
        "shadowrocket": ".list",
        "quantumultx": ".list",
        "egern": ".yaml",
        "loon": ".list",
    }
    details: list[str] = []
    l5 = True
    for client, ext in expected.items():
        ok = _client_artifacts_ok(art / client, ext)
        details.append(f"{client}:{ok}")
        l5 = l5 and ok
    results["L5_native_adapters"] = {"pass": l5, "detail": ",".join(details)}

    l6 = False
    mihomo_dir = art / "mihomo"
    if mihomo_dir.exists():
        service_files = [p for p in mihomo_dir.glob("*.yaml") if p.stem != "aggregate" and p.stat().st_size > 0]
        l6 = len(service_files) > 0
    results["L6_service_views"] = {"pass": l6, "detail": "per-service artifacts exist"}

    l7 = all(
        (run_dir / rel).exists()
        for rel in (
            "canonical/manifest.json",
            "hierarchy/manifest.json",
            "ir/manifest.json",
            "snapshot_id.txt",
            "run_manifest.json",
        )
    )
    results["L7_reproducibility_base"] = {
        "pass": l7,
        "detail": "stage manifests present for hash compare",
    }

    all_pass = all(v["pass"] for v in results.values())
    summary = {
        "schema": "golden_v2",
        "all_pass": all_pass,
        "results": results,
        "v2_runtime_dependency": 0,
    }
    out = run_dir / "golden" / "report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary
