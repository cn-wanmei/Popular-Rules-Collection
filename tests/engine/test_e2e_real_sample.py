"""E2E: real database/services sample → migrate → pipeline → promote."""
from __future__ import annotations
import shutil
from pathlib import Path
import pytest
from src.engine.validation.naming_gate import run_naming_gate
from src.engine.ingest.migrate_legacy import migrate_database_services_to_snapshot
from src.engine.pipeline.run import run_pipeline
from src.engine.promote.artifact import promote_run

SAMPLE = Path("database/services_sample")

@pytest.mark.skipif(not SAMPLE.exists() or not any(SAMPLE.glob("*.yaml")), reason="no sample services")
def test_e2e_migrate_pipeline_promote(tmp_path):
    assert run_naming_gate(Path(".")).get("pass") is True
    snaps = tmp_path / "snapshots"
    m = migrate_database_services_to_snapshot(SAMPLE, snaps)
    assert m["v2_runtime_dependency"] == 0
    assert m["extra"]["service_files"] >= 1
    clean = tmp_path / "clean_sources"
    shutil.copytree(snaps / m["snapshot_id"] / "sources", clean)
    data = tmp_path / "data"
    result = run_pipeline(clean, data)
    assert result["status"] == "ok"
    assert result["stages"]["release"]["state"] == "RC_READY"
    rec = promote_run(data / "runs" / result["run_id"], tmp_path / "generated")
    assert (tmp_path / "generated" / "mihomo").exists()
