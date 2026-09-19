"""Phase 5 — unified release engine.

This module composes the existing V3 pipeline and promotion gate. It does not
duplicate or weaken release validation.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from src.engine.pipeline.run import run_pipeline
from src.engine.promote.artifact import promote_run
UNIFIED_RELEASE_SCHEMA = "unified_release_v1"
@dataclass(frozen=True)
class UnifiedReleaseResult:
    status: str
    run_id: str | None
    release_state: str | None
    promotion: dict[str, Any] | None = None
    failures: tuple[str, ...] = ()
    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": UNIFIED_RELEASE_SCHEMA,
            "status": self.status,
            "run_id": self.run_id,
            "release_state": self.release_state,
            "promotion": self.promotion,
            "failures": list(self.failures),
        }
class UnifiedReleaseEngine:
    def run(
        self,
        sources_root: Path,
        data_root: Path,
        generated_root: Path,
        baseline_path: Path | None = None,
        *,
        run_id: str | None = None,
        skip_large: bool = False,
    ) -> UnifiedReleaseResult:
        pipeline = run_pipeline(
            Path(sources_root),
            Path(data_root),
            run_id=run_id,
            skip_large=skip_large,
        )
        actual_run_id = pipeline.get("run_id")
        if pipeline.get("status") != "ok":
            failures = tuple(str(item) for item in pipeline.get("failure_stages", []))
            return UnifiedReleaseResult("blocked", actual_run_id, None, failures=failures)
        release_state = pipeline.get("stages", {}).get("release", {}).get("state")
        if release_state != "RC_READY":
            return UnifiedReleaseResult("blocked", actual_run_id, str(release_state), failures=("release_not_rc_ready",))
        promotion = promote_run(
            Path(data_root) / "runs" / str(actual_run_id),
            Path(generated_root),
            baseline_path=baseline_path,
        )
        return UnifiedReleaseResult("published", str(actual_run_id), "RC_READY", promotion=promotion)

def run_unified_release(
    sources_root: Path,
    data_root: Path,
    generated_root: Path,
    baseline_path: Path | None = None,
    *,
    run_id: str | None = None,
    skip_large: bool = False,
) -> dict[str, Any]:
    return UnifiedReleaseEngine().run(
        sources_root,
        data_root,
        generated_root,
        baseline_path,
        run_id=run_id,
        skip_large=skip_large,
    ).to_dict()
