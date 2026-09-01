"""P0-2: Snapshot & Quarantine must run BEFORE Canonical."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from src.engine.pipeline.run import run_pipeline, STAGES


def _prepare_sources(tmp: Path) -> Path:
    src = tmp / "sources"
    services = src / "services"
    services.mkdir(parents=True)
    (services / "google.yaml").write_text(
        "id: google\ncategory: search\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: google.com\n"
        "  - type: DOMAIN\n    value: www.google.com\n"
        "  - type: DOMAIN\n    # missing value → will be quarantined\n",
        encoding="utf-8",
    )
    return src


def test_stage_order_hard():
    assert STAGES.index("snapshot") < STAGES.index("ingest")
    assert STAGES.index("ingest") < STAGES.index("quarantine")
    assert STAGES.index("quarantine") < STAGES.index("canonical")


def test_pipeline_snapshot_quarantine_before_canonical():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        sources = _prepare_sources(tmp)
        data = tmp / "data"
        # This fixture intentionally contains a quarantined record. Stop at canonical
        # so P1.5 quality policy does not turn an intentionally dirty fixture into a
        # release candidate while we verify stage ordering and quarantine behavior.
        result = run_pipeline(sources, data, stages=STAGES[: STAGES.index("canonical") + 1])

        assert result["v2_runtime_dependency"] == 0
        assert result["status"] == "ok"
        assert "snapshot" in result["stages"]
        assert "quarantine" in result["stages"]
        assert "canonical" in result["stages"]

        assert result["stages"]["quarantine"]["quarantined"] >= 1
        assert result["stages"]["canonical"]["unique_rules"] == 2

        run_id = result["run_id"]
        run_dir = data / "runs" / run_id
        assert (run_dir / "run_manifest.json").exists()
        assert (run_dir / "quarantine" / "quarantine_report.json").exists()
        assert (run_dir / "canonical" / "manifest.json").exists()
        assert (run_dir / "canonical" / "errors.jsonl").exists()

        snap_id = result["stages"]["snapshot"]["snapshot_id"]
        assert (data / "snapshots" / snap_id / "manifest.json").exists()


def test_canonical_cannot_run_without_quarantine():
    """Direct call order protection is inside run_pipeline; this just documents intent."""
    assert STAGES[0] == "snapshot"
    assert "quarantine" in STAGES
    assert STAGES.index("quarantine") < STAGES.index("canonical")
