from __future__ import annotations

import json
from pathlib import Path

from src.engine.pipeline.run import STAGES, run_pipeline


def _fixture(tmp_path: Path) -> Path:
    source = tmp_path / "sources"
    source.mkdir()
    (source / "sample.list").write_text("DOMAIN,example.com\n", encoding="utf-8")
    return source


def test_full_production_run_has_quality_cas_and_dag(tmp_path: Path) -> None:
    source = _fixture(tmp_path)
    data = tmp_path / "data"
    result = run_pipeline(source, data)
    assert result["status"] == "ok"
    run_dir = data / "runs" / result["run_id"]
    quality = json.loads((run_dir / "reports" / "quality.json").read_text(encoding="utf-8"))
    assert quality["decision"] == "PASS"
    cas = json.loads((run_dir / "cas" / "manifest.json").read_text(encoding="utf-8"))
    assert cas["object_count"] > 0
    assert result["execution"]["mode"] == "dag"

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
        "snapshot", "ingest", "source_gate", "quarantine", "canonical",
        "hierarchy", "ir", "directory", "adapters", "diff", "golden", "observability",
        "cas", "release",
    ]


def test_same_snapshot_is_reproducible(tmp_path: Path) -> None:
    source = _fixture(tmp_path)
    data = tmp_path / "data"
    first = run_pipeline(source, data)
    snapshot_id = first["snapshot_id"]
    second = run_pipeline(source, data, snapshot_id=snapshot_id)
    assert second["snapshot_id"] == snapshot_id
    run_a = data / "runs" / first["run_id"]
    run_b = data / "runs" / second["run_id"]
    from src.engine.stabilization.compare import compare_runs
    comparison = compare_runs(run_a, run_b)
    assert comparison["match"] is True
