#!/usr/bin/env python3
"""Validate Provider/Service identity invariants before production builds."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = yaml.safe_load(fh) or {}
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping: {path}")
    return value


def validate(root: Path = ROOT) -> list[str]:
    gate = load_yaml(root / "config/service_production_gate.yaml")
    paths = gate["inputs"]
    p0 = load_yaml(root / paths["p0_materialization"])
    hierarchy = load_yaml(root / paths["hierarchy"])
    primary = load_yaml(root / paths["primary"])
    model = load_yaml(root / paths["service_model"])
    memberships = load_yaml(root / paths["memberships"])

    errors: list[str] = []
    entries = p0.get("services", [])
    ids = [entry.get("id") for entry in entries]
    if len(ids) != len(set(ids)):
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        errors.append(f"P0 duplicate service ids: {duplicates}")

    for entry in entries:
        service_id = entry.get("id")
        if not service_id or not entry.get("provider"):
            errors.append(f"P0 identity incomplete: {entry!r}")
        if not entry.get("region"):
            errors.append(f"P0 region missing: {service_id}")
        if not entry.get("source_hints"):
            errors.append(f"P0 source_hints missing: {service_id}")

    providers = hierarchy.get("providers", {})
    primary_services = primary.get("services", {})
    model_services = model.get("services", {})
    aggregates = memberships.get("aggregates", {})

    for entry in entries:
        service_id = entry.get("id")
        provider = entry.get("provider")
        hierarchy_provider = next(
            (name for name, data in providers.items() if service_id in data.get("services", {})),
            None,
        )
        if hierarchy_provider and hierarchy_provider != provider:
            errors.append(
                f"hierarchy provider mismatch: {service_id}: P0={provider}, hierarchy={hierarchy_provider}"
            )

        primary_entry = primary_services.get(service_id)
        if isinstance(primary_entry, dict) and primary_entry.get("parent"):
            parent = primary_entry["parent"]
            parent_entry = primary_services.get(parent, {})
            parent_provider = parent_entry.get("primary_category")
            if parent_provider and parent_provider != provider:
                errors.append(
                    f"primary parent provider mismatch: {service_id}: P0={provider}, primary parent={parent_provider}"
                )

        model_entry = model_services.get(service_id)
        if isinstance(model_entry, dict) and model_entry.get("provider") != provider:
            errors.append(
                f"service model provider mismatch: {service_id}: P0={provider}, model={model_entry.get('provider')}"
            )

    for service_id, entry in model_services.items():
        if not isinstance(entry, dict) or not entry.get("provider"):
            errors.append(f"service model provider missing: {service_id}")

    for aggregate_id, aggregate in aggregates.items():
        aggregate_provider = aggregate.get("provider")
        if not aggregate_provider:
            errors.append(f"aggregate provider missing: {aggregate_id}")
            continue
        for member in aggregate.get("members", []):
            member_entry = model_services.get(member)
            if isinstance(member_entry, dict) and member_entry.get("provider") != aggregate_provider:
                errors.append(
                    f"aggregate membership provider mismatch: {aggregate_id} -> {member}: "
                    f"aggregate={aggregate_provider}, member={member_entry.get('provider')}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("SERVICE PRODUCTION HARD GATE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SERVICE PRODUCTION HARD GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
