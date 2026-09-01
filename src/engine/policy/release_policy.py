"""Production release policy: deterministic hard gates and explainable risk score."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class PolicyDecision:
    decision: str
    score: float
    checks: dict[str, dict[str, Any]]

    @property
    def passed(self) -> bool:
        return self.decision == "PASS"


def _load_policy(path: Path) -> dict[str, Any]:
    if not Path(path).exists():
        return {}
    import yaml
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def evaluate_quality(metrics: dict[str, Any], policy: dict[str, Any]) -> PolicyDecision:
    cfg = policy.get("quality", {})
    rates = metrics.get("rates", {})
    parser = metrics.get("parser_coverage", {})
    diff = metrics.get("diff", {})
    source = metrics.get("source_health", {})

    checks: dict[str, dict[str, Any]] = {}
    checks["clean_rate"] = {
        "value": float(rates.get("clean_rate", 0.0)),
        "min": float(cfg.get("min_clean_rate", 0.995)),
    }
    checks["quarantine_rate"] = {
        "value": float(rates.get("quarantine_rate", 1.0)),
        "max": float(cfg.get("max_quarantine_rate", 0.01)),
    }
    checks["canonical_error_rate"] = {
        "value": float(rates.get("canonical_error_rate", 1.0)),
        "max": float(cfg.get("max_canonical_error_rate", 0.0)),
    }
    checks["parser_recognition_rate"] = {
        "value": float(parser.get("recognition_rate", 0.0)),
        "min": float(cfg.get("min_parser_recognition_rate", 0.995)),
    }
    checks["removed_rules"] = {
        "value": int(diff.get("removed", 0)),
        "max": int(cfg.get("max_removed_rules", 10000)),
    }
    checks["source_error_count"] = {
        "value": sum(int(v.get("errors", 0)) for v in source.values() if isinstance(v, dict)),
        "max": int(cfg.get("max_source_errors", 0)),
    }
    checks["v2_runtime_dependency"] = {"value": metrics.get("v2_runtime_dependency", -1), "expected": 0}

    for item in checks.values():
        if "min" in item:
            item["pass"] = item["value"] >= item["min"]
        elif "max" in item:
            item["pass"] = item["value"] <= item["max"]
        else:
            item["pass"] = item["value"] == item["expected"]

    weights = {
        "clean_rate": 20,
        "quarantine_rate": 15,
        "canonical_error_rate": 15,
        "parser_recognition_rate": 15,
        "removed_rules": 15,
        "source_error_count": 10,
        "v2_runtime_dependency": 10,
    }
    score = round(sum(weights[name] for name, check in checks.items() if check["pass"]), 2)
    hard_required = set(cfg.get("hard_checks", list(checks)))
    hard_failures = [name for name in hard_required if not checks.get(name, {}).get("pass", False)]
    decision = "PASS" if not hard_failures else "BLOCK"
    return PolicyDecision(decision, score, checks)


def write_quality_report(run_dir: Path, metrics: dict[str, Any], policy_path: Path) -> dict[str, Any]:
    policy = _load_policy(policy_path)
    decision = evaluate_quality(metrics, policy)
    report = {
        "schema": "data_quality_v2",
        "decision": decision.decision,
        "score": decision.score,
        "all_hard_pass": decision.passed,
        "checks": decision.checks,
        "policy_file": str(policy_path),
    }
    out = Path(run_dir) / "quality.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
