"""Engine Pipeline — one immutable V3 run from snapshot to release."""
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
from src.engine.observability.metrics import build_observability, quality_score
from src.engine.release.evidence import build_sbom, retention_plan
from src.engine.release.state_machine import evaluate_release

STAGES = [
    "snapshot", "ingest", "quarantine", "canonical", "hierarchy",
    "ir", "adapters", "diff", "golden", "observability", "release",
]


def _new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-run"


def _load_quality_policy(repo_root: Path | None = None) -> dict[str, Any]:
    path = (repo_root or Path(".")) / "config" / "release.yaml"
    if not path.exists():
        return {}
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def run_pipeline(
    sources_root: Path,
    data_root: Path,
    *,
    run_id: str | None = None,
    stages: list[str] | None = None,
    skip_large: bool = False,
) -> dict[str, Any]:
    data_root = Path(data_root)
    sources_root = Path(sources_root)
    run_id = run_id or _new_run_id()
    run_dir = data_root / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    wanted = stages or STAGES
    if wanted != STAGES and wanted != STAGES[: len(wanted)]:
        raise ValueError("Stages must be a contiguous prefix of the V3 pipeline")

    results: dict[str, Any] = {
        "schema": "engine_run_v2",
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stages": {},
        "skip_large": skip_large,
        "v2_runtime_dependency": 0,
    }

    def persist() -> None:
        (run_dir / "run_manifest.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    persist()
    snapshot_manifest = ingest_result = clean_payload = None

    if "snapshot" in wanted:
        snapshot_manifest = create_source_snapshot(sources_root, data_root / "snapshots", extra_meta={"run_id": run_id, "skip_large": skip_large})
        (run_dir / "snapshot_id.txt").write_text(snapshot_manifest["snapshot_id"], encoding="utf-8")
        results["snapshot_id"] = snapshot_manifest["snapshot_id"]
        results["stages"]["snapshot"] = {"status": "ok", "snapshot_id": snapshot_manifest["snapshot_id"]}
        persist()

    if "ingest" in wanted:
        if snapshot_manifest is None:
            raise RuntimeError("ingest requires snapshot")
        ingest_result = ingest_snapshot(data_root / "snapshots" / snapshot_manifest["snapshot_id"], skip_large=skip_large)
        results["stages"]["ingest"] = {"status": "ok", "records": ingest_result["stats"]["records"], "errors": ingest_result["stats"]["errors"]}
        persist()

    if "quarantine" in wanted:
        if ingest_result is None:
            raise RuntimeError("quarantine requires ingest")
        clean_payload = run_quarantine(ingest_result, run_dir / "quarantine")
        results["stages"]["quarantine"] = {"status": "ok", "clean": clean_payload["stats"]["records"], "quarantined": clean_payload["stats"]["quarantined"]}
        persist()

    if "canonical" in wanted:
        if clean_payload is None:
            raise RuntimeError("canonical requires quarantine")
        can_manifest = build_canonical(clean_payload, run_dir / "canonical")
        results["stages"]["canonical"] = {"status": "ok", "unique_rules": can_manifest["unique_rules"], "memberships": can_manifest["memberships"], "errors": can_manifest["errors"]}
        persist()
        if can_manifest["unique_rules"] == 0:
            raise RuntimeError("canonical produced zero rules")

    if "hierarchy" in wanted:
        h_manifest = build_hierarchy(run_dir / "canonical", run_dir / "hierarchy")
        results["stages"]["hierarchy"] = {"status": "ok", **{k: h_manifest[k] for k in ("service_count", "group_count", "aggregate_count") if k in h_manifest}}
        persist()

    if "ir" in wanted:
        ir_manifest = build_ir(run_dir / "canonical", run_dir / "hierarchy", run_dir / "ir")
        results["stages"]["ir"] = {"status": "ok", "stats": ir_manifest.get("stats")}
        persist()

    if "adapters" in wanted:
        art_report = build_all_clients(run_dir / "canonical", run_dir / "artifacts")
        results["stages"]["adapters"] = {"status": "ok", "clients": list(art_report.get("clients", {}).keys()), "parallel": art_report.get("parallel", False)}
        persist()

    if "diff" in wanted:
        baseline = data_root / "baseline" / "canonical.json"
        diff_report = run_diff(run_dir / "canonical", baseline if baseline.exists() else None, run_dir / "reports" / "diff")
        results["stages"]["diff"] = {"status": "ok", "added": diff_report["added"], "removed": diff_report["removed"], "changed": diff_report["changed"], "baseline": str(baseline) if baseline.exists() else None}
        persist()

    if "golden" in wanted:
        golden = run_golden(run_dir)
        results["stages"]["golden"] = {"status": "ok", "all_pass": golden["all_pass"]}
        persist()
        if not golden["all_pass"]:
            results["status"] = "blocked"
            results["finished_at"] = datetime.now(timezone.utc).isoformat()
            persist()
            return results

    if "observability" in wanted:
        metrics = build_observability(run_dir)
        quality = quality_score(metrics, _load_quality_policy(Path(".")))
        evidence = build_sbom(run_dir)
        retention = retention_plan(data_root / "runs", keep=10)
        results["stages"]["observability"] = {"status": "ok", "quality_score": quality["score"], "quality_decision": quality["decision"], "sbom_files": len(evidence["files"]), "retention_candidates": len(retention["eligible_for_deletion"])}
        (run_dir / "quality.json").write_text(json.dumps(quality, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (run_dir / "retention-plan.json").write_text(json.dumps(retention, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        persist()
        if not quality["all_hard_pass"]:
            results["status"] = "blocked"
            results["finished_at"] = datetime.now(timezone.utc).isoformat()
            persist()
            return results

    if "release" in wanted:
        persist()
        release = evaluate_release(run_dir)
        results["stages"]["release"] = {"status": "ok" if release["can_publish"] else "blocked", "state": release["state"], "can_publish": release["can_publish"]}
        if release["state"] != "RC_READY":
            results["status"] = "blocked"
            results["finished_at"] = datetime.now(timezone.utc).isoformat()
            persist()
            return results

    results["finished_at"] = datetime.now(timezone.utc).isoformat()
    results["status"] = "ok"
    persist()
    return results
