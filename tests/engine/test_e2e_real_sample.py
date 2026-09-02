"""Deterministic production-fixture E2E for the V3 supply chain."""
from __future__ import annotations

import json
from pathlib import Path
import shutil

from src.engine.pipeline.run import run_pipeline
from src.engine.promote.artifact import promote_run, rollback_to_run

FIXTURE = Path("tests/fixtures/v3-production/sources")


def test_e2e_production_fixture_is_not_skipped(tmp_path: Path) -> None:
    source = tmp_path / "sources"
    shutil.copytree(FIXTURE, source)
    data = tmp_path / "data"
    generated = tmp_path / "generated"
    baseline = data / "baseline" / "canonical.json"

    result = run_pipeline(source, data)
    assert result["status"] == "ok", json.dumps({"release": result["stages"].get("release"), "stages": result["stages"]}, indent=2, sort_keys=True)
    assert result["stages"]["golden"]["all_pass"] is True
    assert result["stages"]["release"]["state"] == "RC_READY"

    run_dir = data / "runs" / result["run_id"]
    record = promote_run(run_dir, generated, baseline_path=baseline)
    assert record["release_state"] == "RC_READY"
    assert len(record["client_digests"]) == 7
    assert baseline.exists()
    assert (generated / "_promotion" / "latest.json").exists()
    assert (generated / "mihomo").is_dir()
    assert (generated / "singbox").is_dir()
    assert (generated / "surge").is_dir()
    assert (generated / "shadowrocket").is_dir()
    assert (generated / "quantumultx").is_dir()
    assert (generated / "egern").is_dir()
    assert (generated / "loon").is_dir()

    release_manifest = json.loads((run_dir / "release" / "manifest.json").read_text(encoding="utf-8"))
    golden = json.loads((run_dir / "golden" / "report.json").read_text(encoding="utf-8"))
    assert release_manifest["release_state"] == "RC_READY"
    assert release_manifest["client_digests"] == record["client_digests"]
    assert golden["all_pass"] is True

    rolled = rollback_to_run(result["run_id"], data / "runs", generated)
    assert rolled["run_id"] == result["run_id"]
