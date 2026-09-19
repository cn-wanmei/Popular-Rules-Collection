"""Phase 6 — canonical observation evidence contract.

The contract composes existing run metrics, baseline evidence, quality and
release state into one read-only observation report. It does not mutate
release artifacts or decide promotion by itself.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
OBSERVATION_SCHEMA = "v1_observation_v1"
@dataclass
class ObservationReport:
    schema: str = OBSERVATION_SCHEMA
    run_id: str = ""
    snapshot_id: str | None = None
    baseline_decision: str = "MISSING"
    quality_decision: str = "MISSING"
    release_state: str = "MISSING"
    blockers: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    @property
    def all_pass(self) -> bool:
        return not self.blockers
    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "run_id": self.run_id,
            "snapshot_id": self.snapshot_id,
            "baseline_decision": self.baseline_decision,
            "quality_decision": self.quality_decision,
            "release_state": self.release_state,
            "blockers": sorted(self.blockers),
            "evidence": self.evidence,
            "all_pass": self.all_pass,
        }
def _read(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError): return {}
    return value if isinstance(value, dict) else {}
def observe_run(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    manifest = _read(run_dir / "run_manifest.json")
    metrics = _read(run_dir / "metrics" / "metrics.json")
    baseline = _read(run_dir / "metrics" / "baseline-evidence.json")
    quality = _read(run_dir / "quality.json")
    release = _read(run_dir / "release" / "state.json")
    report = ObservationReport(
        run_id=str(manifest.get("run_id", run_dir.name)),
        snapshot_id=manifest.get("snapshot_id"),
        baseline_decision=str(baseline.get("decision", "MISSING")),
        quality_decision=str(quality.get("decision", "MISSING")),
        release_state=str(release.get("state", "MISSING")),
    )
    if not metrics:
        report.blockers.append("metrics_missing")
    if not baseline:
        report.blockers.append("baseline_evidence_missing")
    elif report.baseline_decision == "ERROR":
        report.blockers.append("baseline_error")
    if not quality or report.quality_decision != "PASS":
        report.blockers.append("quality_not_pass")
    if not release or report.release_state not in {"RC_READY", "PRODUCTION"}:
        report.blockers.append("release_not_observed_as_publishable")
    report.evidence = {
        "records": metrics.get("records", {}),
        "rates": metrics.get("rates", {}),
        "source_health": metrics.get("source_health", {}),
        "parser_coverage": metrics.get("parser_coverage", {}),
        "baseline": baseline,
        "quality_score": quality.get("score"),
        "release_gates": release.get("gates", {}),
    }
    out = run_dir / "observation" / "report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report.to_dict()
