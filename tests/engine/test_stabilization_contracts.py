from src.engine.dag.contract import stage_fingerprint
from src.engine.observability.baseline import build_baseline, evaluate_baseline


def test_stage_fingerprint_is_deterministic():
    a = stage_fingerprint("canonical", "v1", "abc", {"z": 1, "a": 2})
    b = stage_fingerprint("canonical", "v1", "abc", {"a": 2, "z": 1})
    assert a == b
    assert a != stage_fingerprint("canonical", "v2", "abc", {"a": 2, "z": 1})


def test_baseline_ignores_runtime_metadata():
    baseline = build_baseline({"generated_at": "today", "records": {"ingested": 100, "unique_rules": 90}})
    assert "generated_at" not in baseline
    assert baseline["records"]["ingested"] == 100


def test_critical_baseline_deviation_blocks():
    decision = evaluate_baseline(
        {"records": {"ingested": 20, "unique_rules": 90, "memberships": 100}},
        {"records": {"ingested": 100, "unique_rules": 90, "memberships": 100}},
        {"baseline": {"min_ratio": 0.5, "max_ratio": 1.5}},
    )
    assert decision.decision == "BLOCK"
    assert decision.anomalies[0]["metric"] == "ingested"


def test_no_baseline_does_not_false_block():
    assert evaluate_baseline({"records": {"ingested": 1}}, None).decision == "NO_BASELINE"
