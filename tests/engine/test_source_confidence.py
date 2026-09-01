import pytest

from src.engine.decision.source_confidence import SourceEvidence, score_source


def test_verified_healthy_source_is_high_confidence():
    result = score_source(SourceEvidence(1.0, 1.0, 1.0))
    assert result.level == "high"
    assert result.score == 1.0
    assert result.reasons == ()


def test_integrity_failure_forces_low_confidence():
    result = score_source(SourceEvidence(1.0, 1.0, 0.99))
    assert result.level == "low"
    assert "integrity_failures_present" in result.reasons


def test_repeated_failures_are_penalized_explainably():
    result = score_source(SourceEvidence(0.9, 0.9, 1.0, consecutive_failures=3, degraded=True))
    assert result.score < 0.8
    assert "consecutive_failures=3" in result.reasons
    assert "source_degraded" in result.reasons


def test_ratios_are_validated():
    with pytest.raises(ValueError):
        score_source(SourceEvidence(1.1, 1.0, 1.0))
