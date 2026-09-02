"""V3 production pipeline — deterministic DAG over one immutable Run."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.adapters.build_all import build_all_clients
from src.engine.canonical.store import build_canonical
from src.engine.cas.run_store import register_run
from src.engine.dag.executor import Node, execute
from src.engine.diff.engine import run_diff
from src.engine.golden.runner import run_golden
from src.engine.hierarchy.resolver import build_hierarchy
from src.engine.ingest.source_ingest import ingest_snapshot
from src.engine.ir.builder import build_ir
from src.engine.observability.metrics import build_observability
from src.engine.policy.release_policy import write_quality_report
from src.engine.quarantine.engine import run_quarantine
from src.engine.release.evidence import build_sbom, retention_plan
from src.engine.release.state_machine import evaluate_release
from src.engine.snapshot.engine import create_source_snapshot, load_snapshot_manifest

STAGES = [
    "snapshot", "ingest", "quarantine", "canonical", "hierarchy", "ir",
    "adapters", "diff", "golden", "observability", "cas", "release",
]

DAG_NODES = [
    Node("snapshot"),
    Node("ingest", ("snapshot",)),
    Node("quarantine", ("ingest",)),
    Node("canonical", ("quarantine",)),
    Node("hierarchy", ("canonical",)),
    Node("ir", ("hierarchy",)),
    Node("adapters", ("ir",)),
    Node("diff", ("canonical",)),
    Node("golden", ("adapters",)),
    Node("observability", ("diff", "golden")),
    Node("cas", ("observability",)),
    Node("release", ("cas",)),
]


def _new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-run"


def _resolve_repo_path(path: Path | str) -> Path:
    """Resolve CLI paths against the repository root so relative inputs are stable."""
    value = Path(path).expanduser()
    if not value.is_absolute():
        value = ROOT / value
    return value.resolve()


def _load_collection_manifest(sources_root: Path) -> dict[str, Any] | None:
    """Load the Collection DAG manifest when sources_root is a collection day root."""
    sources_root = _resolve_repo_path(sources_root)
    path = sources_root / "manifests" / "_collection.json"
    if not path.exists():
        return None
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid collection manifest: {path}") from exc
    if manifest.get("schema") != "collection_manifest_v1":
        raise RuntimeError(f"Unsupported collection manifest schema: {manifest.get('schema')!r}")
    if manifest.get("status") == "blocked":
        raise RuntimeError(
            "Collection DAG is blocked: "
            + ", ".join(manifest.get("critical_failures") or ["unknown failure"])
        )
    return manifest


def run_pipeline(
    sources_root: Path,
    data_root: Path,
    *,
    run_id: str | None = None,
    stages: list[str] | None = None,
    skip_large: bool = False,
    snapshot_id: str | None = None,
) -> dict[str, Any]:
    data_root = _resolve_repo_path(data_root)
    sources_root = _resolve_repo_path(sources_root)
    collection_manifest = _load_collection_manifest(sources_root)
    if collection_manifest:
        collection_root = Path(str(collection_manifest.get("root", "")))
        if not collection_root.is_absolute():
            collection_root = ROOT / collection_root
        if collection_root.resolve() != sources_root.resolve():
            raise RuntimeError("Collection manifest root does not match Engine sources root")

    run_id = run_id or _new_run_id()
    run_dir = data_root / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    wanted = stages or STAGES
    if wanted != STAGES and wanted != STAGES[: len(wanted)]:
        raise ValueError("Stages must be a contiguous prefix of the V3 pipeline")
    wanted_set = set(wanted)
    node_by_name = {n.name: n for n in DAG_NODES if n.name in wanted_set}
    nodes = [Node(stage, tuple(d for d in node_by_name[stage].deps if d in wanted_set)) for stage in STAGES if stage in wanted_set]

    results: dict[str, Any] = {
        "schema": "engine_run_v5",
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stages": {},
        "skip_large": skip_large,
        "snapshot_id": snapshot_id,
        "collection_id": collection_manifest.get("collection_id") if collection_manifest else None,
        "collection_manifest": str((sources_root / "manifests" / "_collection.json").relative_to(ROOT)) if collection_manifest else None,
        "v2_runtime_dependency": 0,
        "execution": {"mode": "dag", "layers": []},
    }
    context: dict[str, Any] = {}

    def persist() -> None:
        path = run_dir / "run_manifest.json"
        tmp = path.with_name(".run_manifest.json.tmp")
        tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        tmp.replace(path)

    def handler_snapshot() -> dict[str, Any]:
        if snapshot_id:
            snap_dir = data_root / "snapshots" / snapshot_id
            manifest = load_snapshot_manifest(snap_dir)
            context["snapshot"] = manifest
            results["snapshot_id"] = manifest["snapshot_id"]
            (run_dir / "snapshot_id.txt").write_text(manifest["snapshot_id"], encoding="utf-8")
            return {"status": "ok", "snapshot_id": manifest["snapshot_id"], "file_count": manifest.get("file_count", 0), "reused": True}
        manifest = create_source_snapshot(sources_root, data_root / "snapshots", extra_meta={"run_id": run_id, "skip_large": skip_large, "collection_id": results.get("collection_id")})
        context["snapshot"] = manifest
        results["snapshot_id"] = manifest["snapshot_id"]
        (run_dir / "snapshot_id.txt").write_text(manifest["snapshot_id"], encoding="utf-8")
        return {"status": "ok", "snapshot_id": manifest["snapshot_id"], "file_count": manifest.get("file_count", 0), "reused": False}

    def handler_ingest() -> dict[str, Any]:
        result = ingest_snapshot(data_root / "snapshots" / context["snapshot"]["snapshot_id"], skip_large=skip_large)
        context["ingest"] = result
        return {"status": "ok", "records": result["stats"]["records"], "errors": result["stats"]["errors"]}

    def handler_quarantine() -> dict[str, Any]:
        payload = run_quarantine(context["ingest"], run_dir / "quarantine")
        context["quarantine"] = payload
        return {"status": "ok", "clean": payload["stats"]["records"], "quarantined": payload["stats"]["quarantined"]}

    def handler_canonical() -> dict[str, Any]:
        manifest = build_canonical(context["quarantine"], run_dir / "canonical")
        if manifest["unique_rules"] == 0:
            return {"status": "blocked", "reason": "canonical produced zero rules", **manifest}
        return {"status": "ok", "unique_rules": manifest["unique_rules"], "memberships": manifest["memberships"], "errors": manifest["errors"]}

    def handler_hierarchy() -> dict[str, Any]:
        manifest = build_hierarchy(run_dir / "canonical", run_dir / "hierarchy")
        return {"status": "ok", **{k: manifest[k] for k in ("service_count", "group_count", "aggregate_count") if k in manifest}}

    def handler_ir() -> dict[str, Any]:
        manifest = build_ir(run_dir / "canonical", run_dir / "hierarchy", run_dir / "ir")
        return {"status": "ok", "stats": manifest.get("stats"), "schema": manifest.get("ir_schema", "semantic_ir_v2")}

    def handler_adapters() -> dict[str, Any]:
        report = build_all_clients(run_dir / "ir", run_dir / "artifacts")
        return {"status": "ok", "clients": sorted(report.get("clients", {})), "parallel": report.get("parallel", False), "source_contract": report.get("source_contract")}

    def handler_diff() -> dict[str, Any]:
        baseline = data_root / "baseline" / "canonical.json"
        report = run_diff(run_dir / "canonical", baseline if baseline.exists() else None, run_dir / "reports" / "diff")
        return {"status": "ok", "added": report["added"], "removed": report["removed"], "changed": report["changed"], "baseline": str(baseline) if baseline.exists() else None}

    def handler_golden() -> dict[str, Any]:
        report = run_golden(run_dir)
        return {"status": "ok", "all_pass": report["all_pass"]}

    def handler_observability() -> dict[str, Any]:
        metrics = build_observability(run_dir)
        quality = write_quality_report(run_dir, metrics, Path("config") / "release.yaml")
        evidence = build_sbom(run_dir)
        retention = retention_plan(data_root / "runs", keep=10)
        return {"status": "ok", "quality_score": quality["score"], "quality_decision": quality["decision"], "sbom_files": len(evidence["files"]), "retention_candidates": len(retention["eligible_for_deletion"])}

    def handler_cas() -> dict[str, Any]:
        manifest = register_run(run_dir, data_root / "cas" / "objects")
        return {"status": "ok", "object_count": manifest["object_count"]}

    def handler_release() -> dict[str, Any]:
        release = evaluate_release(run_dir)
        if release["can_publish"]:
            register_run(run_dir, data_root / "cas" / "objects")
        return {"status": "ok" if release["can_publish"] else "blocked", "state": release["state"], "can_publish": release["can_publish"], "quality_score": release.get("quality_score")}

    handlers = {"snapshot": handler_snapshot, "ingest": handler_ingest, "quarantine": handler_quarantine, "canonical": handler_canonical, "hierarchy": handler_hierarchy, "ir": handler_ir, "adapters": handler_adapters, "diff": handler_diff, "golden": handler_golden, "observability": handler_observability, "cas": handler_cas, "release": handler_release}

    def checkpoint(layer: list[str], all_results: dict[str, Any]) -> None:
        results["execution"]["layers"].append(list(layer))
        for name in layer:
            results["stages"][name] = all_results[name]
        persist()

    persist()
    executed = execute(nodes, handlers, max_workers=min(8, len(nodes)), fail_fast=False, on_layer_complete=checkpoint)
    results["stages"].update(executed)
    results["finished_at"] = datetime.now(timezone.utc).isoformat()
    failures = [name for name, value in executed.items() if isinstance(value, dict) and value.get("status") in {"failed", "skipped", "blocked"}]
    results["status"] = "blocked" if failures else "ok"
    if failures:
        results["failure_stages"] = failures
    persist()
    return results


# project root is derived from this module path
ROOT = Path(__file__).resolve().parents[3]
