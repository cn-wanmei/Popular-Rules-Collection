"""Explainable source health/confidence scoring.

Scores are advisory until the Release Policy consumes them. No single metric
can silently override a hard acquisition or integrity failure.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SourceEvidence:
    success_rate: float
    freshness_ratio: float
    integrity_rate: float
    consecutive_failures: int = 0
    degraded: bool = False


@dataclass(frozen=True)
class SourceConfidence:
    score: float
    level: str
    reasons: tuple[str, ...]


def _validate_ratio(name: str, value: float) -> None:
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must be a finite ratio between 0 and 1")


def score_source(evidence: SourceEvidence) -> SourceConfidence:
    _validate_ratio("success_rate", evidence.success_rate)
    _validate_ratio("freshness_ratio", evidence.freshness_ratio)
    _validate_ratio("integrity_rate", evidence.integrity_rate)
    if isinstance(evidence.consecutive_failures, bool) or evidence.consecutive_failures < 0:
        raise ValueError("consecutive_failures must be a non-negative integer")

    raw = (
        evidence.success_rate * 0.30
        + evidence.freshness_ratio * 0.20
        + evidence.integrity_rate * 0.50
    )
    penalty = min(0.35, evidence.consecutive_failures * 0.05)
    score = max(0.0, min(1.0, raw - penalty - (0.10 if evidence.degraded else 0.0)))

    reasons: list[str] = []
    if evidence.integrity_rate < 1:
        reasons.append("integrity_failures_present")
    if evidence.success_rate < 0.95:
        reasons.append("fetch_success_below_target")
    if evidence.freshness_ratio < 0.95:
        reasons.append("freshness_below_target")
    if evidence.consecutive_failures:
        reasons.append(f"consecutive_failures={evidence.consecutive_failures}")
    if evidence.degraded:
        reasons.append("source_degraded")

    if evidence.integrity_rate < 1 or score < 0.50:
        level = "low"
    elif score < 0.80:
        level = "medium"
    else:
        level = "high"
    return SourceConfidence(round(score, 6), level, tuple(reasons))
