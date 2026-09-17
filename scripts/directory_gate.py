#!/usr/bin/env python3
"""Validate canonical and generated rule directory invariants."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "service_model" / "directories.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping: {path}")
    return data


def _rule_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    allowed = {".yaml", ".yml", ".json", ".jsonl", ".list", ".txt", ".mmdb"}
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in allowed]


def validate(root: Path = ROOT) -> dict[str, Any]:
    policy = load_yaml(root / "config" / "service_model" / "directories.yaml")
    if policy.get("schema") != "rule_directory_policy_v1":
        raise ValueError("unsupported directory policy schema")

    errors: list[str] = []
    rules_root = root / "rules"
    generated_root = root / "generated"
    semantics = policy.get("semantics") or {}
    if semantics.get("no_flattened_service_files") is not True:
        errors.append("policy must forbid flattened service files")

    # Canonical rules: rules/<provider>/<all|service>/file.
    for path in _rule_files(rules_root):
        rel = path.relative_to(rules_root).parts
        if len(rel) < 3:
            errors.append(f"canonical rule file is too shallow: {path.relative_to(root)}")
            continue
        provider, scope = rel[0], rel[1]
        if scope == "all":
            continue
        if scope in {"china", "all"}:
            errors.append(f"invalid canonical scope placement: {path.relative_to(root)}")
        # A service is always a directory below its provider; no provider-root files.
        if provider == "china" and scope != "all":
            errors.append(f"China may only contain the all aggregate: {path.relative_to(root)}")

    # Generated rules mirror provider/service identity and may not be flat.
    for path in _rule_files(generated_root):
        rel = path.relative_to(generated_root).parts
        if len(rel) < 4:
            errors.append(f"generated rule file is too shallow: {path.relative_to(root)}")
            continue
        client, provider, scope = rel[0], rel[1], rel[2]
        if scope == "all":
            pass
        elif provider == "china" and scope != "all":
            errors.append(f"generated China may only contain all: {path.relative_to(root)}")

    china = policy.get("china") or {}
    excluded = {str(x).strip().lower() for x in china.get("exclude_independent_providers") or []}
    if len(excluded) != len(china.get("exclude_independent_providers") or []):
        errors.append("China exclusion list contains duplicates or empty provider ids")
    if china.get("require_domain_and_ip_coverage") is not True:
        errors.append("China aggregate must require domain and IP coverage")

    return {
        "schema": "rule_directory_gate_v1",
        "pass": not errors,
        "errors": errors,
        "canonical_rule_files": len(_rule_files(rules_root)),
        "generated_rule_files": len(_rule_files(generated_root)),
        "china_excluded_independent_providers": sorted(excluded),
        "policy": str(POLICY.relative_to(root)),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()
    report = validate(args.root)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
