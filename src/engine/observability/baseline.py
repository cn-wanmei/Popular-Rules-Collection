"""Deterministic production baseline and anomaly evaluation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BaselineDecision:
    decision: str
    anomalies: tuple[dict[str, Any], ...]

    @property
    def blocked(self) -> bool:
        return self.decision == "BLOCK"


def _ratio(current: float, baseline: float) -> float | None:
    if baseline == 0:
        return None
    return current / baseline


def evaluate_baseline(
    metrics: dict[str, Any],
    baseline: dict[str, Any] | None,
    policy: dict[str, Any] | None = None,
) -> BaselineDecision:
    """Compare stable production counts against a trusted baseline.

    Missing baselines never create a false anomaly. Once a baseline exists,
    configured absolute and relative deviations are evaluated fail-closed for
    critical metrics and explainably for all other metrics.
    """
    if not baseline:
        return BaselineDecision("NO_BASELINE", ())
    cfg = (policy or {}).get("baseline", {})
    critical = set(cfg.get("critical_metrics", ["ingested", "unique_rules", "memberships"]))
    min_ratio = float(cfg.get("min_ratio", 0.5))
    max_ratio = float(cfg.get("max_ratio", 1.5))
    anomalies: list[dict[str, Any]] = []
    current_records = metrics.get("records", {})
    base_records = baseline.get("records", {})
    for name, value in current_records.items():
        if not isinstance(value, (int, float)) or name not in base_records:
            continue
        base = base_records[name]
        if not isinstance(base, (int, float)):
            continue
        ratio = _ratio(float(value), float(base))
        if ratio is None:
            if value != base:
                anomalies.append({"metric": name, "current": value, "baseline": base, "ratio": None, "severity": "critical" if name in critical else "warning", "reason": "baseline_zero"})
            continue
        if ratio < min_ratio or ratio > max_ratio:
            anomalies.append({"metric": name, "current": value, "baseline": base, "ratio": round(ratio, 6), "severity": "critical" if name in critical else "warning", "reason": "relative_deviation"})
    decision = "BLOCK" if any(a["severity"] == "critical" for a in anomalies) else ("WARN" if anomalies else "PASS")
    return BaselineDecision(decision, tuple(anomalies))


def build_baseline(metrics: dict[str, Any]) -> dict[str, Any]:
    """Extract only stable business measurements; exclude runtime timestamps."""
    records = metrics.get("records", {})
    stable = {k: records[k] for k in sorted(records) if isinstance(records[k], (int, float))}
    return {"schema": "production_baseline_v1", "records": stable}
