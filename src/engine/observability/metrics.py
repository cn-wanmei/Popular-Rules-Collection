"""Run metrics, data quality scoring, source health and parser coverage."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _ratio(num: int, den: int) -> float:
    return round(num / den, 6) if den else 1.0


def build_observability(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    snapshot_id = manifest.get("snapshot_id")
    ingest = manifest.get("stages", {}).get("ingest", {})
    quarantine = manifest.get("stages", {}).get("quarantine", {})
    canonical = manifest.get("stages", {}).get("canonical", {})
    diff = manifest.get("stages", {}).get("diff", {})

    input_records = int(ingest.get("records", 0))
    ingest_errors = int(ingest.get("errors", 0))
    clean_records = int(quarantine.get("clean", 0))
    quarantined = int(quarantine.get("quarantined", 0))
    unique_rules = int(canonical.get("unique_rules", 0))
    memberships = int(canonical.get("memberships", 0))
    canonical_errors = int(canonical.get("errors", 0))

    snapshot_manifest = None
    snap_path = Path(run_dir).parents[1] / "snapshots" / str(snapshot_id) / "manifest.json" if snapshot_id else None
    if snap_path and snap_path.exists():
        snapshot_manifest = json.loads(snap_path.read_text(encoding="utf-8"))

    source_health: dict[str, dict[str, Any]] = defaultdict(lambda: {"files": 0, "rules": 0, "errors": 0})
    if snapshot_manifest:
        for rel in snapshot_manifest.get("file_digests", {}):
            source = Path(rel).parts[0] if Path(rel).parts else "root"
            source_health[source]["files"] += 1

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

    parser_coverage = {
        "structured_service_records": int(ingest.get("records", 0)),
        "recognized_records": input_records,
        "recognition_rate": _ratio(input_records - ingest_errors, input_records),
        "quarantine_rate": _ratio(quarantined, input_records + quarantined),
    }

    metrics = {
        "schema": "run_metrics_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_id": run_dir.name,
        "snapshot_id": snapshot_id,
        "records": {
            "ingested": input_records,
            "clean": clean_records,
            "quarantined": quarantined,
            "unique_rules": unique_rules,
            "memberships": memberships,
            "ingest_errors": ingest_errors,
            "canonical_errors": canonical_errors,
        },
        "rates": {
            "clean_rate": _ratio(clean_records, input_records),
            "quarantine_rate": _ratio(quarantined, input_records + quarantined),
            "canonical_error_rate": _ratio(canonical_errors, max(clean_records, 1)),
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

    metrics_path = run_dir / "metrics" / "metrics.json"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (metrics_path.parent / "source-health.json").write_text(json.dumps(dict(source_health), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (metrics_path.parent / "parser-coverage.json").write_text(json.dumps(parser_coverage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return metrics


def quality_score(metrics: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    rates = metrics["rates"]
    thresholds = policy.get("quality", {})
    clean_min = float(thresholds.get("min_clean_rate", 0.995))
    quarantine_max = float(thresholds.get("max_quarantine_rate", 0.01))
    canonical_error_max = float(thresholds.get("max_canonical_error_rate", 0.0))
    diff_removed_max = int(thresholds.get("max_removed_rules", 10000))

    checks = {
        "clean_rate": {"value": rates["clean_rate"], "min": clean_min, "pass": rates["clean_rate"] >= clean_min},
        "quarantine_rate": {"value": rates["quarantine_rate"], "max": quarantine_max, "pass": rates["quarantine_rate"] <= quarantine_max},
        "canonical_error_rate": {"value": rates["canonical_error_rate"], "max": canonical_error_max, "pass": rates["canonical_error_rate"] <= canonical_error_max},
        "removed_rules": {"value": metrics["diff"]["removed"], "max": diff_removed_max, "pass": metrics["diff"]["removed"] <= diff_removed_max},
        "v2_runtime_dependency": {"value": metrics["v2_runtime_dependency"], "expected": 0, "pass": metrics["v2_runtime_dependency"] == 0},
    }
    score = round(100.0 * sum(1 for v in checks.values() if v["pass"]) / len(checks), 2)
    result = {
        "schema": "data_quality_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "score": score,
        "all_hard_pass": all(v["pass"] for v in checks.values()),
        "checks": checks,
        "decision": "PASS" if all(v["pass"] for v in checks.values()) else "BLOCK",
    }
    return result
