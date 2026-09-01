from src.engine.observability.performance import build_performance_baseline, evaluate_performance


def test_build_performance_baseline_is_stable():
    baseline = build_performance_baseline({"build": [10, 20, 30, 40, 50], "collect": [5, 5, 5]})
    assert baseline["schema"] == "performance_baseline_v1"
    assert baseline["records"]["build"]["p50_ms"] == 30
    assert baseline["records"]["build"]["p95_ms"] == 48


def test_performance_regression_blocks():
    baseline = build_performance_baseline({"build": [10, 10, 10, 10]})
    current = build_performance_baseline({"build": [13, 13, 13, 13]})
    decision = evaluate_performance(current, baseline, max_regression_ratio=1.2)
    assert decision.blocked
    assert decision.regressions[0]["stage"] == "build"


def test_missing_baseline_does_not_block():
    current = build_performance_baseline({"build": [10]})
    assert evaluate_performance(current, None).decision == "NO_BASELINE"
