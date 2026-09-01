"""Engine Pipeline — full independent V3 order.

HARD ORDER:
  snapshot → ingest → quarantine → canonical
  → hierarchy → decision/ir → adapters
  → diff → golden → release
  (publish only when release state == RC_READY)
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.snapshot.engine import create_source_snapshot
from src.engine.ingest.source_ingest import ingest_snapshot
from src.engine.quarantine.engine import run_quarantine
from src.engine.canonical.store import build_canonical
from src.engine.hierarchy.resolver import build_hierarchy
from src.engine.ir.builder import build_ir
from src.engine.adapters.build_all import build_all_clients
from src.engine.diff.engine import run_diff
from src.engine.golden.runner import run_golden
from src.engine.release.state_machine import evaluate_release

STAGES = [
    "snapshot",
    "ingest",
    "quarantine",
    "canonical",
    "hierarchy",
    "ir",
    "adapters",
    "diff",
    "golden",
    "release",
]


def _new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-run"


def run_pipeline(
    sources_root: Path,
    data_root: Path,
    *,
    run_id: str | None = None,
    stages: list[str] | None = None,
) -> dict[str, Any]:
    data_root = Path(data_root)
    sources_root = Path(sources_root)
    run_id = run_id or _new_run_id()
    run_dir = data_root / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    wanted = stages or STAGES
    results: dict[str, Any] = {
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stages": {},
        "v2_runtime_dependency": 0,
    }
    # Write early so Golden L7 / Release can see the flag
    (run_dir / "run_manifest.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    snapshot_manifest = None
    ingest_result = None
    clean_payload = None

    if "snapshot" in wanted:
        snap_dir = data_root / "snapshots"
        snapshot_manifest = create_source_snapshot(
            sources_root, snap_dir, extra_meta={"run_id": run_id}
        )
        (run_dir / "snapshot_id.txt").write_text(snapshot_manifest["snapshot_id"], encoding="utf-8")
        results["stages"]["snapshot"] = {"status": "ok", "snapshot_id": snapshot_manifest["snapshot_id"]}

    if "ingest" in wanted:
        if not snapshot_manifest:
            raise RuntimeError("ingest requires snapshot")
        snap_path = data_root / "snapshots" / snapshot_manifest["snapshot_id"]
        ingest_result = ingest_snapshot(snap_path)
        (run_dir / "ingest").mkdir(exist_ok=True)
        results["stages"]["ingest"] = {
            "status": "ok",
            "records": ingest_result["stats"]["records"],
            "errors": ingest_result["stats"]["errors"],
        }

    if "quarantine" in wanted:
        if not ingest_result:
            raise RuntimeError("quarantine requires ingest")
        clean_payload = run_quarantine(ingest_result, run_dir / "quarantine")
        results["stages"]["quarantine"] = {
            "status": "ok",
            "clean": clean_payload["stats"]["records"],
            "quarantined": clean_payload["stats"]["quarantined"],
        }

    if "canonical" in wanted:
        if not clean_payload:
            raise RuntimeError("canonical requires quarantine")
        can_manifest = build_canonical(clean_payload, run_dir / "canonical")
        results["stages"]["canonical"] = {
            "status": "ok",
            "unique_rules": can_manifest["unique_rules"],
            "memberships": can_manifest["memberships"],
        }

    if "hierarchy" in wanted:
        h_manifest = build_hierarchy(run_dir / "canonical", run_dir / "hierarchy")
        results["stages"]["hierarchy"] = {"status": "ok", **{k: h_manifest[k] for k in ("service_count", "group_count", "aggregate_count") if k in h_manifest}}

    if "ir" in wanted:
        ir_manifest = build_ir(run_dir / "canonical", run_dir / "hierarchy", run_dir / "ir")
        results["stages"]["ir"] = {"status": "ok", "stats": ir_manifest.get("stats")}

    if "adapters" in wanted:
        art_report = build_all_clients(run_dir / "canonical", run_dir / "artifacts")
        results["stages"]["adapters"] = {"status": "ok", "clients": list(art_report.get("clients", {}).keys())}

    if "diff" in wanted:
        diff_report = run_diff(run_dir / "canonical", None, run_dir / "reports" / "diff")
        results["stages"]["diff"] = {"status": "ok", "added": diff_report["added"]}

    if "golden" in wanted:
        golden = run_golden(run_dir)
        results["stages"]["golden"] = {"status": "ok", "all_pass": golden["all_pass"]}

    if "release" in wanted:
        release = evaluate_release(run_dir)
        results["stages"]["release"] = {
            "status": "ok",
            "state": release["state"],
            "can_publish": release["can_publish"],
        }

    results["finished_at"] = datetime.now(timezone.utc).isoformat()
    results["status"] = "ok"
    (run_dir / "run_manifest.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return results
