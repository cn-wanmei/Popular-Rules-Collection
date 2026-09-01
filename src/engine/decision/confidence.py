"""Explainable rule/source confidence scoring for P3 policy decisions."""
from __future__ import annotations

from typing import Any


def score_rule(rule: dict[str, Any]) -> dict[str, Any]:
    provenance = rule.get("provenance") or {}
    sources = provenance.get("sources") or []
    score = 0.5
    reasons = ["base=0.50"]
    if len(sources) >= 2:
        score += 0.2
        reasons.append("multi_source=+0.20")
    elif len(sources) == 1:
        score += 0.1
        reasons.append("source_present=+0.10")
    classification = rule.get("classification") or {}
    if classification.get("category") and classification.get("category") != "other":
        score += 0.1
        reasons.append("classified=+0.10")
    if rule.get("identity_key"):
        score += 0.1
        reasons.append("identity_key=+0.10")
    score = min(1.0, round(score, 4))
    return {"score": score, "band": "high" if score >= 0.8 else "medium" if score >= 0.6 else "low", "reasons": reasons}
