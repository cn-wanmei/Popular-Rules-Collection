from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.engine.cas.run_store import verify_run
from src.engine.pipeline.run import run_pipeline, STAGES
from src.engine.reproducibility.hash_compare import compare_runs

FIXTURE = Path("tests/fixtures/v3-production/sources")


def _fixture(tmp_path: Path) -> Path:
    source = tmp_path / "sources"
    shutil.copytree(FIXTURE, source)
    return source


def test_full_production_run_has_quality_cas_and_dag(tmp_path: Path) -> None:
    data = tmp_path / "data"
    result = run_pipeline(_fixture(tmp_path), data)
    assert result["status"] == "ok"
    assert result["execution"]["mode"] == "dag"
    assert ["diff", "golden"] in result["execution"]["layers"]
    assert result["stages"]["observability"]["quality_decision"] == "PASS"
    assert result["stages"]["cas"]["object_count"] > 0
    assert result["stages"]["release"]["state"] == "RC_READY"

    run_dir = data / "runs" / result["run_id"]
    quality = json.loads((run_dir / "quality.json").read_text(encoding="utf-8"))
    assert quality["decision"] == "PASS"
    assert (run_dir / "cas-manifest.json").exists()
    check = verify_run(run_dir, data / "cas" / "objects")
    assert check["verified"] is True

    ir = json.loads((run_dir / "ir" / "ir.json").read_text(encoding="utf-8"))
    assert ir["schema"] == "semantic_ir_v2"
    assert ir["memberships"]
    assert ir["v2_runtime_dependency"] == 0

    artifacts = run_dir / "artifacts"
    assert {p.name for p in artifacts.iterdir() if p.is_dir()} >= {
        "mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon"
    }


def test_pipeline_stages_are_dependency_complete() -> None:
    assert STAGES == [
        "snapshot", "ingest", "quarantine", "canonical", "hierarchy", "ir",
        "adapters", "diff", "golden", "observability", "cas", "release",
    ]


def test_same_snapshot_is_reproducible(tmp_path: Path) -> None:
    source = _fixture(tmp_path)
    data = tmp_path / "data"
    first = run_pipeline(source, data)
    snapshot_id = first["snapshot_id"]
    snap_sources = data / "snapshots" / snapshot_id / "sources"
    second = run_pipeline(snap_sources, data)
    run_a = data / "runs" / first["run_id"]
    run_b = data / "runs" / second["run_id"]
    comparison = compare_runs(run_a, run_b)
    assert comparison["match"] is True
