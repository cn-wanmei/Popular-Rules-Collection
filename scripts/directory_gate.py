#!/usr/bin/env python3
"""Validate the V3 human-rule and generated distribution directory contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.engine.validation.directory_contract import validate

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LAYOUT = {
    "human_aggregate": "rule/{provider}/{provider}.yaml",
    "human_service": "rule/{provider}/{service}/{service}.yaml",
    "human_china": "rule/china/china.yaml",
    "human_category": "rule/category/{category}/{category}.yaml",
    "human_group": "rule/group/{group}/{group}.yaml",
    "human_aggregate_entity": "rule/aggregate/{aggregate}/{aggregate}.yaml",
    "human_unmapped_service": "rule/unmapped/{service}/{service}.yaml",
}


def _policy_report(root: Path) -> dict:
    import yaml

    root = root.resolve()
    policy_path = root / "config/service_model/directories.yaml"
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
    errors: list[str] = []
    if policy.get("schema") != "rule_distribution_policy_v2":
        errors.append("unsupported rule distribution policy schema")
    layout = policy.get("layout") or {}
    for key, expected in EXPECTED_LAYOUT.items():
        if str(layout.get(key) or "").strip() != expected:
            errors.append(f"directory policy layout mismatch: {key} must be {expected}")
    return {
        "schema": "rule_distribution_policy_gate_v3",
        "pass": not errors,
        "errors": errors,
        "policy": str(policy_path.relative_to(root)),
        "tree_validation": "skipped_during_pr_migration",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument(
        "--policy-only",
        action="store_true",
        help="Validate the V3 directory policy without requiring the already-published rule tree.",
    )
    args = parser.parse_args()
    report = _policy_report(args.root) if args.policy_only else validate(args.root)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
