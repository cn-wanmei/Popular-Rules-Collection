from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest

from src.engine.pipeline.run import run_pipeline
from src.engine.promote.artifact import promote_run, rollback_to_run

FIXTURE = Path("tests/fixtures/v3-production/sources")


def _build(tmp_path: Path):
    source = tmp_path / "sources"
    shutil.copytree(FIXTURE, source)
    data = tmp_path / "data"
    generated = tmp_path / "generated"
    result = run_pipeline(source, data)
    run_dir = data / "runs" / result["run_id"]
    assert result["status"] == "ok"
    assert result["stages"]["release"]["state"] == "RC_READY"
    promote_run(run_dir, generated, baseline_path=data / "baseline" / "canonical.json")
    return data, generated, run_dir


def test_p1_rollback_rejects_tampered_client_artifact(tmp_path: Path) -> None:
    data, generated, run_dir = _build(tmp_path)
    target = run_dir / "artifacts" / "mihomo"
    files = list(target.glob("*.yaml"))
    assert files
    files[0].write_text(files[0].read_text(encoding="utf-8") + "# tampered\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="digest"):
        rollback_to_run(run_dir.name, data / "runs", generated)


def test_p1_rollback_rejects_missing_client(tmp_path: Path) -> None:
    data, generated, run_dir = _build(tmp_path)
    shutil.rmtree(run_dir / "artifacts" / "loon")
    with pytest.raises(RuntimeError, match="client artifacts"):
        rollback_to_run(run_dir.name, data / "runs", generated)


def test_p1_promotion_record_contains_release_identity(tmp_path: Path) -> None:
    _, generated, run_dir = _build(tmp_path)
    rec = json.loads((generated / "_promotion" / "latest.json").read_text(encoding="utf-8"))
    manifest = json.loads((run_dir / "release" / "manifest.json").read_text(encoding="utf-8"))
    assert rec["run_id"] == run_dir.name
    assert rec["snapshot_id"] == manifest["snapshot_id"]
    assert rec["client_digests"] == manifest["client_digests"]
