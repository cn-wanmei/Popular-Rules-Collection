#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / "config/p0_service_identity.yaml"
SERVICE_MODEL = ROOT / "config/service_model/services.yaml"
ALIASES = ROOT / "config/service_model/aliases.yaml"
RELATIONS = ROOT / "config/service_model/relations.yaml"
LEGACY_INDEX = ROOT / "rule/_index.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"required input missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"expected mapping YAML: {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Evidence-bound Q-02 Service Identity reconciliation audit")
    parser.add_argument("--output", default="reports/phase2/service_identity_reconciliation.json")
    parser.add_argument("--decision-log", default="")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    identity = load_yaml(IDENTITY)
    model = load_yaml(SERVICE_MODEL)
    aliases_doc = load_yaml(ALIASES)
    relations_doc = load_yaml(RELATIONS)
    legacy = load_yaml(LEGACY_INDEX)

    p0 = identity.get("services") or []
    model_services = model.get("services") or {}
    aliases = aliases_doc.get("aliases") or {}
    ownership = relations_doc.get("ownership") or {}
    categories = legacy.get("categories") or {}

    ids = [str(x.get("id", "")).strip() for x in p0 if isinstance(x, dict)]
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1})

    provider_mismatches = []
    aggregate_violations = []
    missing_model = []

    for item in p0:
        if not isinstance(item, dict):
            continue
        sid = str(item.get("id", "")).strip()
        provider = str(item.get("provider", "")).strip()
        aggregate = str(item.get("aggregate", "")).strip()
        model_item = model_services.get(sid)
        if model_item is None:
            missing_model.append(sid)
        elif isinstance(model_item, dict):
            model_provider = str(model_item.get("provider", "")).strip()
            if provider and model_provider and provider != model_provider:
                provider_mismatches.append(
                    {"id": sid, "p0_provider": provider, "service_model_provider": model_provider}
                )
        if identity.get("identity_rules", {}).get("aggregate_and_service_must_differ"):
            if sid and aggregate and sid == aggregate:
                aggregate_violations.append(sid)

    dangling_aliases = sorted(
        str(alias_id)
        for alias_id, item in aliases.items()
        if isinstance(item, dict)
        and str(item.get("canonical", "")).strip()
        and str(item.get("canonical", "")).strip() not in model_services
    )

    legacy_ids = set()
    legacy_rule_count = 0
    for category in categories.values():
        if not isinstance(category, dict):
            continue
        for rule in category.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            legacy_rule_count += 1
            rid = str(rule.get("id", "")).strip()
            if rid:
                legacy_ids.add(rid)

    legacy_exact = sorted(x for x in ids if x in legacy_ids)
    legacy_unmapped = sorted(x for x in ids if x not in legacy_ids)

    decision_log_present = bool(args.decision_log) and Path(args.decision_log).exists()
    structural_pass = not (
        duplicate_ids
        or missing_model
        or provider_mismatches
        or aggregate_violations
        or dangling_aliases
    )
    reconciliation_pass = structural_pass and decision_log_present

    report = {
        "schema": "phase2_service_identity_reconciliation_v1",
        "status": "PASS" if reconciliation_pass else "NOT_COMPLETE",
        "evidence_bound": True,
        "population": {
            "p0_identity_count": len(ids),
            "service_model_count": len(model_services),
            "legacy_rule_count": legacy_rule_count,
            "ownership_relation_count": len(ownership),
            "alias_count": len(aliases),
        },
        "structural_checks": {
            "duplicate_identity_ids": duplicate_ids,
            "missing_service_model_ids": sorted(set(missing_model)),
            "provider_mismatches": provider_mismatches,
            "aggregate_service_id_violations": sorted(set(aggregate_violations)),
            "dangling_alias_targets": dangling_aliases,
            "structural_pass": structural_pass,
        },
        "legacy_mapping": {
            "exact_id_matches": legacy_exact,
            "unmapped_p0_ids": legacy_unmapped,
        },
        "evidence": {
            "reviewed_decision_log_present": decision_log_present,
            "reconciliation_pass": reconciliation_pass,
        },
        "inputs": {
            "identity": str(IDENTITY),
            "service_model": str(SERVICE_MODEL),
            "aliases": str(ALIASES),
            "relations": str(RELATIONS),
            "legacy_index": str(LEGACY_INDEX),
            "decision_log": args.decision_log or None,
        },
    }

    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.enforce and not reconciliation_pass:
        print("Q-02 is not complete: reviewed evidence is still required.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
