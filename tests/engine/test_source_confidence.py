import math

import pytest

from src.engine.decision.source_confidence import SourceEvidence, score_source


def test_integrity_is_highest_weight_and_failure_forces_low_level():
    result = score_source(SourceEvidence(1.0, 1.0, 0.9))
    assert result.score == 0.95
    assert result.level == "low"
    assert "integrity_failures_present" in result.reasons


def test_invalid_ratios_fail_closed():
    for kwargs in (
        {"success_rate": math.nan, "freshness_ratio": 1.0, "integrity_rate": 1.0},
        {"success_rate": 1.0, "freshness_ratio": math.inf, "integrity_rate": 1.0},
        {"success_rate": 1.0, "freshness_ratio": 1.0, "integrity_rate": -math.inf},
        {"success_rate": 1.1, "freshness_ratio": 1.0, "integrity_rate": 1.0},
    ):
        with pytest.raises(ValueError):
            score_source(SourceEvidence(**kwargs))


def test_negative_or_boolean_failure_count_fails_closed():
    with pytest.raises(ValueError):
        score_source(SourceEvidence(1.0, 1.0, 1.0, consecutive_failures=-1))
    with pytest.raises(ValueError):
        score_source(SourceEvidence(1.0, 1.0, 1.0, consecutive_failures=True))


def test_failure_penalty_is_bounded():
    result = score_source(SourceEvidence(1.0, 1.0, 1.0, consecutive_failures=100))
    assert result.score == 0.65
