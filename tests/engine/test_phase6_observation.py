import json
from pathlib import Path
from src.engine.observation.contract import observe_run
def _run(root: Path, *, baseline_decision: str = "PASS", quality: str = "PASS", release: str = "RC_READY") -> Path:
    run = root / "runs" / "r1"
    (run / "metrics").mkdir(parents=True)
    (run / "release").mkdir()
    (run / "run_manifest.json").write_text(json.dumps({"run_id": "r1", "snapshot_id": "s1"}), encoding="utf-8")
    (run / "metrics" / "metrics.json").write_text(json.dumps({"records": {"ingested": 10}, "rates": {}, "source_health": {}, "parser_coverage": {}}), encoding="utf-8")
    (run / "metrics" / "baseline-evidence.json").write_text(json.dumps({"decision": baseline_decision}), encoding="utf-8")
    (run / "quality.json").write_text(json.dumps({"decision": quality, "score": 100}), encoding="utf-8")
    (run / "release" / "state.json").write_text(json.dumps({"state": release, "gates": {}}), encoding="utf-8")
    return run
def test_observation_passes_complete_publishable_run(tmp_path: Path) -> None:
    report = observe_run(_run(tmp_path))
    assert report["all_pass"] is True
    assert report["run_id"] == "r1"
def test_observation_blocks_baseline_error(tmp_path: Path) -> None:
    report = observe_run(_run(tmp_path, baseline_decision="ERROR"))
    assert report["all_pass"] is False
    assert "baseline_error" in report["blockers"]
def test_observation_blocks_non_publishable_release(tmp_path: Path) -> None:
    report = observe_run(_run(tmp_path, release="BLOCKED"))
    assert report["all_pass"] is False
    assert "release_not_observed_as_publishable" in report["blockers"]
