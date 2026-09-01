from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.engine.observability.metrics import build_observability, quality_score
from src.engine.pipeline.run import run_pipeline

FIXTURE = Path("tests/fixtures/v3-production/sources")


def test_p1_5_observability_outputs_and_quality_gate(tmp_path: Path) -> None:
    source = tmp_path / "sources"
    shutil.copytree(FIXTURE, source)
    data = tmp_path / "data"
    result = run_pipeline(source, data)
    assert result["status"] == "ok"
    run_dir = data / "runs" / result["run_id"]
    metrics = json.loads((run_dir / "metrics" / "metrics.json").read_text(encoding="utf-8"))
    quality = json.loads((run_dir / "quality.json").read_text(encoding="utf-8"))
    assert metrics["records"]["ingested"] > 0
    assert metrics["parser_coverage"]["recognition_rate"] == 1.0
    assert quality["decision"] == "PASS"
    assert quality["all_hard_pass"] is True
    assert (run_dir / "metrics" / "source-health.json").exists()
    assert (run_dir / "metrics" / "parser-coverage.json").exists()


def test_quality_score_blocks_low_clean_rate() -> None:
    metrics = {
        "rates": {"clean_rate": 0.8, "quarantine_rate": 0.2, "canonical_error_rate": 0.0},
        "diff": {"removed": 0},
        "v2_runtime_dependency": 0,
    }
    result = quality_score(metrics, {"quality": {"min_clean_rate": 0.95, "max_quarantine_rate": 0.05}})
    assert result["decision"] == "BLOCK"
    assert result["all_hard_pass"] is False
