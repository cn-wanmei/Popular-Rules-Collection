from pathlib import Path

from src.engine.observability.metrics import build_observability
from src.engine.policy.release_policy import evaluate_quality


def test_quarantine_is_not_counted_as_source_error(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "run-1"
    run_dir.mkdir(parents=True)
    (run_dir / "run_manifest.json").write_text(
        '{"snapshot_id":"snap-1","stages":{'
        '"ingest":{"records":100,"errors":0},'
        '"quarantine":{"clean":99,"quarantined":1},'
        '"canonical":{"unique_rules":99,"memberships":99,"errors":0},'
        '"diff":{"added":99,"removed":0,"changed":0,"baseline":null}}}',
        encoding="utf-8",
    )
    qdir = run_dir / "quarantine"
    qdir.mkdir()
    (qdir / "quarantined.jsonl").write_text(
        '{"record":{"path":"blackmatrix7/rules/bad.txt"}}\n',
        encoding="utf-8",
    )

    metrics = build_observability(run_dir)

    assert metrics["source_health"]["blackmatrix7"]["errors"] == 0
    assert metrics["source_health"]["blackmatrix7"]["quarantined"] == 1


def test_quarantine_within_policy_does_not_block_release() -> None:
    metrics = {
        "rates": {
            "clean_rate": 1.0,
            "quarantine_rate": 0.01,
            "canonical_error_rate": 0.0,
        },
        "parser_coverage": {"recognition_rate": 1.0},
        "diff": {"removed": 0},
        "source_health": {"blackmatrix7": {"errors": 0, "quarantined": 1}},
        "v2_runtime_dependency": 0,
        "baseline": {"decision": "NO_BASELINE"},
    }
    decision = evaluate_quality(metrics, {"quality": {}})

    assert decision.decision == "PASS"
    assert decision.checks["source_error_count"]["value"] == 0
