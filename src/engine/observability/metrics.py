"""Run metrics, source health, parser coverage and release-risk evidence."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _ratio(num: int, den: int) -> float:
    return round(num / den, 6) if den else 0.0


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def build_observability(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    manifest = _load_json(run_dir / "run_manifest.json", {})
    snapshot_id = manifest.get("snapshot_id")
    stages = manifest.get("stages", {})
    ingest = stages.get("ingest", {}) or {}
    quarantine = stages.get("quarantine", {}) or {}
    canonical = stages.get("canonical", {}) or {}
    diff = stages.get("diff", {}) or {}

    ingested = int(ingest.get("records", 0))
    ingest_errors = int(ingest.get("errors", 0))
    clean = int(quarantine.get("clean", 0))
    quarantined = int(quarantine.get("quarantined", 0))
    unique_rules = int(canonical.get("unique_rules", 0))
    memberships = int(canonical.get("memberships", 0))
    canonical_errors = int(canonical.get("errors", 0))

    source_health: dict[str, dict[str, Any]] = defaultdict(lambda: {"files": 0, "bytes": 0, "errors": 0})
    snapshot_path = Path(run_dir).parents[1] / "snapshots" / str(snapshot_id) if snapshot_id else None
    snapshot_manifest = _load_json(snapshot_path / "manifest.json", {}) if snapshot_path else {}
    for rel in snapshot_manifest.get("file_digests", {}):
        p = snapshot_path / "sources" / rel
        source = Path(rel).parts[0] if Path(rel).parts else "root"
        source_health[source]["files"] += 1
        if p.exists() and p.is_file():
            source_health[source]["bytes"] += p.stat().st_size

    qpath = run_dir / "quarantine" / "quarantined.jsonl"
    if qpath.exists():
        for line in qpath.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            rec = item.get("record") if isinstance(item, dict) else None
            path = str(rec.get("path", "unknown")) if isinstance(rec, dict) else "unknown"
            source = Path(path).parts[0] if Path(path).parts else "unknown"
            source_health[source]["errors"] += 1

    recognition_den = ingested + ingest_errors
    parser_coverage = {
        "input_records": recognition_den,
        "recognized_records": ingested,
        "parse_errors": ingest_errors,
        "recognition_rate": _ratio(ingested, recognition_den),
        "quarantine_rate": _ratio(quarantined, ingested + quarantined),
    }

    metrics = {
        "schema": "run_metrics_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_id": run_dir.name,
        "snapshot_id": snapshot_id,
        "records": {
            "ingested": ingested,
            "clean": clean,
            "quarantined": quarantined,
            "unique_rules": unique_rules,
            "memberships": memberships,
            "ingest_errors": ingest_errors,
            "canonical_errors": canonical_errors,
        },
        "rates": {
            "clean_rate": _ratio(clean, ingested),
            "quarantine_rate": _ratio(quarantined, ingested + quarantined),
            "canonical_error_rate": _ratio(canonical_errors, max(clean, 1)),
        },
        "diff": {
            "added": int(diff.get("added", 0)),
            "removed": int(diff.get("removed", 0)),
            "changed": int(diff.get("changed", 0)),
            "baseline_present": bool(diff.get("baseline")),
        },
        "source_health": dict(source_health),
        "parser_coverage": parser_coverage,
        "v2_runtime_dependency": 0,
    }

    # Baseline is a separate immutable control-plane artifact. Never compare
    # against a partially written or timestamp-bearing run file.
    baseline_path = Path(run_dir).parents[2] / "baseline" / "latest.json"
    baseline = _load_json(baseline_path, None)
    baseline_cfg = {"baseline": {"min_ratio": 0.50, "max_ratio": 1.50}}
    try:
        from src.engine.observability.baseline import evaluate_baseline
        baseline_decision = evaluate_baseline(metrics, baseline, baseline_cfg)
        metrics["baseline"] = {
            "schema": "baseline_evidence_v1",
            "decision": baseline_decision.decision,
            "anomalies": list(baseline_decision.anomalies),
            "baseline_path": str(baseline_path.relative_to(Path(run_dir).parents[2])) if baseline_path.exists() else None,
        }
    except Exception as exc:
        # Observability must never silently convert an evaluator failure into
        # a PASS. Record an explicit degraded state for the release policy.
        metrics["baseline"] = {"schema": "baseline_evidence_v1", "decision": "ERROR", "anomalies": [], "error": f"{type(exc).__name__}: {exc}"}

    metrics_dir = run_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    (metrics_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (metrics_dir / "source-health.json").write_text(json.dumps(dict(source_health), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (metrics_dir / "parser-coverage.json").write_text(json.dumps(parser_coverage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (metrics_dir / "baseline-evidence.json").write_text(json.dumps(metrics["baseline"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return metrics


def quality_score(metrics: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Compatibility wrapper around the V3 release policy evaluator."""
    from src.engine.policy.release_policy import evaluate_quality
    decision = evaluate_quality(metrics, policy)
    return {
        "schema": "data_quality_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "score": decision.score,
        "all_hard_pass": decision.passed,
        "checks": decision.checks,
        "decision": decision.decision,
    }
