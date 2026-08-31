#!/usr/bin/env python3
"""V2.3 Failure injection against ci_gates.yaml expectations."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "config" / "ci_gates.yaml"
OUT = ROOT / "reports" / "gate_injection.json"


def main() -> int:
    doc = yaml.safe_load(GATES.read_text(encoding="utf-8")) if GATES.exists() else {}
    gates = doc.get("gates") or {}
    scenarios = [
        {"name": "schema_fail", "gate": "schema_validate", "expect_action": "BLOCK_BUILD"},
        {"name": "size_fail", "gate": "size_gate", "expect_action": "BLOCK_RELEASE"},
        {"name": "icon_soft", "gate": "icon_coverage", "expect_action": "INFO"},
        {"name": "growth_warn", "gate": "growth_anomaly", "expect_action": "WARN"},
    ]
    results = []
    for s in scenarios:
        actual = gates.get(s["gate"])
        results.append({**s, "actual": actual, "pass": actual == s["expect_action"]})
    report = {"mode": doc.get("mode"), "results": results, "all_pass": all(r["pass"] for r in results)}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[gate_injection] all_pass={report['all_pass']} mode={report['mode']}")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
