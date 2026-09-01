"""Stage performance baseline with explainable regression decisions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PERFORMANCE_SCHEMA = "performance_baseline_v1"

@dataclass(frozen=True)
class PerformanceDecision:
    decision: str
    regressions: tuple[dict[str, Any], ...]

    @property
    def blocked(self) -> bool:
        return self.decision == "BLOCK"

def build_performance_baseline(samples: dict[str, list[float]]) -> dict[str, Any]:
    """Build stable p50/p95 stage timings from millisecond samples."""
    records = {}
    for stage in sorted(samples):
        values = sorted(float(v) for v in samples[stage] if float(v) >= 0)
        if not values:
            continue
        def percentile(p: float) -> float:
            index = (len(values) - 1) * p
            lo, hi = int(index), min(int(index) + 1, len(values) - 1)
            return round(values[lo] + (values[hi] - values[lo]) * (index - lo), 3)
        records[stage] = {"count": len(values), "p50_ms": percentile(0.50), "p95_ms": percentile(0.95)}
    return {"schema": PERFORMANCE_SCHEMA, "records": records}

def evaluate_performance(
    current: dict[str, Any],
    baseline: dict[str, Any] | None,
    *,
    max_regression_ratio: float = 1.20,
    min_samples: int = 1,
) -> PerformanceDecision:
    if not baseline:
        return PerformanceDecision("NO_BASELINE", ())
    regressions = []
    for stage in sorted(current.get("records", {})):
        now = current["records"][stage]
        old = baseline.get("records", {}).get(stage)
        if not isinstance(now, dict) or not isinstance(old, dict):
            continue
        if int(now.get("count", 0)) < min_samples:
            continue
        for metric in ("p50_ms", "p95_ms"):
            current_ms, baseline_ms = now.get(metric), old.get(metric)
            if not isinstance(current_ms, (int, float)) or not isinstance(baseline_ms, (int, float)) or baseline_ms <= 0:
                continue
            ratio = float(current_ms) / float(baseline_ms)
            if ratio > max_regression_ratio:
                regressions.append({"stage": stage, "metric": metric, "current_ms": current_ms, "baseline_ms": baseline_ms, "ratio": round(ratio, 6)})
    return PerformanceDecision("BLOCK" if regressions else "PASS", tuple(regressions))
