#!/usr/bin/env python3
"""Phase 8 final migration gate: Legacy Asset Equivalence + Phase 4-7 + V3 production."""
from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from src.engine.ingest.legacy_asset_extractor import iter_service_assets
from src.engine.ingest.legacy_asset_reconciliation import reconcile_legacy_assets
from src.engine.legacy_finalization.finalizer import finalize_legacy
from src.engine.ingest.v1_index import load_v1_index
from src.engine.v1.client_regression import RULE_KINDS, run_client_regression
from src.engine.v1.golden import REQUIRED_COVERAGE, run_v1_golden
from src.engine.v1.legacy_regression import compare_legacy_to_v1, load_assets_from_records
from src.engine.v1.phase8 import (
    compute_coverage,
    evaluate_phase8_gates,
    load_intentional_registry,
    request_legacy_delete,
    switch_sot_to_v1,
)

ROOT = Path(__file__).resolve().parents[1]


def _yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _norm(service: str, typ: str, value: str) -> dict[str, str]:
    from src.engine.v1.dedup import normalize_record
    rec = normalize_record({"service": service, "type": typ, "value": value})
    return {
        "service": str(rec["service"]).strip().casefold(),
        "type": str(rec["type"]).strip().casefold(),
        "value": str(rec["value"]),
    }


def load_legacy_source_assets(root: Path) -> tuple[list[dict[str, str]], dict[str, int], list[str]]:
    """Read the frozen Legacy Source: database/services/*.yaml."""
    records: list[dict[str, str]] = []
    counts: dict[str, int] = defaultdict(int)
    errors: list[str] = []
    for path in sorted(root.glob("*.yaml")):
        try:
            doc = _yaml(path)
        except Exception as exc:
            errors.append(f"{path}: {exc}")
            continue
        service = str(doc.get("id") or path.stem).strip().casefold()
        rules = doc.get("rules") or []
        if not isinstance(rules, list):
            errors.append(f"{path}: rules must be list")
            continue
        for row in rules:
            if not isinstance(row, dict):
                errors.append(f"{path}: non-mapping rule")
                continue
            typ = str(row.get("type", "")).strip()
            value = str(row.get("value", "")).strip()
            if not typ or not value:
                errors.append(f"{path}: rule missing type/value")
                continue
            records.append(_norm(service, typ, value))
            counts[service] += 1
    return records, dict(counts), errors


def load_v1_source_assets(root: Path) -> tuple[list[dict[str, str]], dict[str, int], list[str]]:
    """Read V1 Canonical service assets under rule/."""
    records: list[dict[str, str]] = []
    counts: dict[str, int] = defaultdict(int)
    errors: list[str] = []
    try:
        for evidence in iter_service_assets(root, include_aggregates=True):
            rec = _norm(evidence.asset.service, evidence.asset.asset_type, evidence.asset.value)
            records.append(rec)
            counts[rec["service"]] += 1
    except Exception as exc:
        errors.append(str(exc))
    return records, dict(counts), errors


def _asset_sets(records: list[dict[str, str]]) -> dict[str, set[tuple[str, str]]]:
    """Build per-service (type, value) sets with canonical normalization applied.

    Records passed to ``audit_legacy_equivalence`` may arrive pre-normalised
    (from ``load_*_source_assets``) or as raw dicts (from tests / callers that
    construct records directly).  Applying ``normalize_record`` here ensures
    that type aliases such as ``ip_cidr6 → ip_cidr`` are resolved before the
    set comparison, preventing false "missing asset" reports.
    """
    from src.engine.v1.dedup import normalize_record

    result: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for rec in records:
        normed = normalize_record(rec)
        result[normed["service"]].add((normed["type"], normed["value"]))
    return dict(result)


def audit_legacy_equivalence(
    legacy_records: list[dict[str, str]],
    v1_records: list[dict[str, str]],
    legacy_counts: dict[str, int],
    v1_counts: dict[str, int],
    intentional_ids: set[str],
    allowed_v1_only_services: set[str] | None = None,
) -> dict[str, Any]:
    allowed_v1_only_services = allowed_v1_only_services or set()
    legacy = _asset_sets(legacy_records)
    v1 = _asset_sets(v1_records)
    legacy_services = set(legacy) | set(legacy_counts)
    v1_services = set(v1) | set(v1_counts)

    missing_services = sorted(legacy_services - v1_services)
    extra_services = sorted(
        s for s in (v1_services - legacy_services)
        if s not in intentional_ids and s not in allowed_v1_only_services
    )
    intentional_with_assets = sorted(
        s for s in (v1_services - legacy_services)
        if s in intentional_ids and v1.get(s)
    )

    missing_assets: dict[str, list[str]] = {}
    extra_assets: dict[str, list[str]] = {}
    total = 0
    covered = 0
    for service in sorted(legacy_services):
        expected = legacy.get(service, set())
        actual = v1.get(service, set())
        total += len(expected)
        covered += len(expected & actual)
        missing = expected - actual
        extra = actual - expected
        if missing:
            missing_assets[service] = [f"{t}:{v}" for t, v in sorted(missing)]
        if extra:
            extra_assets[service] = [f"{t}:{v}" for t, v in sorted(extra)]

    pct = 0.0 if total == 0 else 100.0 * covered / total
    at_100 = total > 0 and covered == total
    passed = (
        at_100
        and not missing_services
        and not extra_services
        and not intentional_with_assets
        and not missing_assets
    )
    return {
        "schema": "legacy_asset_equivalence_v1",
        "legacy_asset_keys": total,
        "covered_asset_keys": covered,
        "coverage_pct": round(pct, 6),
        "at_100": at_100,
        "passed": passed,
        "missing_services": missing_services,
        "missing_assets": missing_assets,
        "extra_v1_assets": extra_assets,
        "unexpected_extra_services": extra_services,
        "extra_intentional_services_with_assets": intentional_with_assets,
        "allowed_v1_only_services": sorted(allowed_v1_only_services),
        "legacy_services": len(legacy_services),
        "v1_services": len(v1_services),
    }


def check_production_run(run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    manifest_path = run_dir / "run_manifest.json"
    release_path = run_dir / "release" / "manifest.json"
    semantic_path = run_dir / "semantic" / "contract.json"
    observation_path = run_dir / "observation" / "report.json"
    if not manifest_path.is_file():
        errors.append(f"missing {manifest_path}")
        return {"pass": False, "errors": errors}
    manifest = _json(manifest_path)
    if manifest.get("status") != "ok":
        errors.append(f"run status={manifest.get('status')!r}")
    stages = manifest.get("stages", {})
    semantic_stage = stages.get("semantic_contract", {})
    if semantic_stage.get("status") != "ok" or semantic_stage.get("all_pass") is not True:
        errors.append("Phase 4 semantic contract stage is not PASS")
    observation_stage = stages.get("observation", {})
    if observation_stage.get("status") != "ok" or observation_stage.get("all_pass") is not True:
        errors.append("Phase 6 observation stage is not PASS")
    release = stages.get("release", {})
    if release.get("state") != "RC_READY":
        errors.append(f"release state={release.get('state')!r}")
    if manifest.get("v2_runtime_dependency") != 0:
        errors.append(f"v2_runtime_dependency={manifest.get('v2_runtime_dependency')!r}")
    if not semantic_path.is_file():
        errors.append(f"missing {semantic_path}")
    else:
        semantic_report = _json(semantic_path)
        if semantic_report.get("all_pass") is not True:
            errors.append("Phase 4 semantic contract report is not PASS")
    if not observation_path.is_file():
        errors.append(f"missing {observation_path}")
    else:
        observation_report = _json(observation_path)
        if observation_report.get("all_pass") is not True:
            errors.append("Phase 6 observation report is not PASS")
    if not release_path.is_file():
        errors.append(f"missing {release_path}")
    else:
        release_manifest = _json(release_path)
        if release_manifest.get("release_state") != "RC_READY":
            errors.append(f"release manifest state={release_manifest.get('release_state')!r}")
    return {"pass": not errors, "errors": errors}


def check_head(expected: str) -> dict[str, Any]:
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    ok = bool(expected) and actual == expected
    return {
        "pass": ok,
        "expected": expected,
        "actual": actual,
        "errors": [] if ok else [f"HEAD mismatch: {actual} != {expected}"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--rule-root", type=Path, default=ROOT / "rule")
    ap.add_argument("--legacy-root", type=Path, default=ROOT / "database" / "services")
    ap.add_argument("--data-root", type=Path, default=ROOT / "data")
    ap.add_argument("--determinism-report", type=Path, required=True)
    ap.add_argument("--expected-commit", required=True)
    ap.add_argument("--json-out", type=Path, default=ROOT / "reports/v1/FINAL_MIGRATION_GATE.json")
    ap.add_argument("--phase8-out", type=Path, default=ROOT / "reports/v1/PHASE8_GATE_REPORT.json")
    ap.add_argument("--legacy-regression-out", type=Path, default=ROOT / "reports/v1/LEGACY_REGRESSION_PHASE7.json")
    ap.add_argument("--config", type=Path, default=ROOT / "config/v1_final_migration_gate.yaml")
    args = ap.parse_args()

    config = _yaml(args.config)
    required_clients = tuple((config.get("clients") or {}).get("required") or ())
    if not required_clients:
        raise SystemExit("final migration gate config has no required clients")

    intentional = load_intentional_registry(ROOT / "config/intentional_unmaterialized.yaml")
    allowed_v1_only = set((config.get("equivalence") or {}).get("allowed_v1_only_services") or ())
    index = load_v1_index(args.rule_root)

    legacy_records, legacy_counts, legacy_errors = load_legacy_source_assets(args.legacy_root)
    v1_records, v1_counts, v1_errors = load_v1_source_assets(args.rule_root)

    registered = {e.id for e in index.entries}
    materialized = set(v1_counts)
    catalogue = compute_coverage(registered, materialized, intentional)

    equivalence = audit_legacy_equivalence(
        legacy_records,
        v1_records,
        legacy_counts,
        v1_counts,
        set(intentional),
        allowed_v1_only,
    )

    legacy_for_regression = load_assets_from_records(legacy_records, "legacy")
    v1_for_regression = load_assets_from_records(v1_records, "v1")
    phase7 = compare_legacy_to_v1(legacy_for_regression, v1_for_regression)

    run_dir = args.data_root / "runs" / args.run_id

    # Phase 7 finalization is a real production hard gate: generate the
    # reconciliation evidence, then aggregate regression + equivalence +
    # reconciliation into one terminal report. Finalization never authorizes
    # deletion; Phase 8 remains a separate explicit operator action.
    reconciliation_path = ROOT / "reports/v1/LEGACY_ASSET_RECONCILIATION.yaml"
    candidates_path = ROOT / "reports/v1/V1_PROMOTION_CANDIDATES.yaml"
    legacy_jsonl_path = args.data_root / "legacy_asset_ir.jsonl"
    reconciliation = reconcile_legacy_assets(
        args.rule_root,
        jsonl_output=legacy_jsonl_path,
        report_path=reconciliation_path,
        candidates_path=candidates_path,
    )
    equivalence_path = ROOT / "reports/v1/LEGACY_ASSET_EQUIVALENCE_PHASE7.json"
    equivalence_path.parent.mkdir(parents=True, exist_ok=True)
    equivalence_path.write_text(
        json.dumps(equivalence, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.legacy_regression_out.parent.mkdir(parents=True, exist_ok=True)
    args.legacy_regression_out.write_text(
        json.dumps({
            "schema": "v1_legacy_regression_final_v2",
            "counts": phase7.counts,
            "unexplained_removed": phase7.unexplained_removed,
            "errors": phase7.errors,
            "all_pass": not phase7.unexplained_removed and not phase7.errors,
            "asset_equivalence": equivalence,
        }, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    phase7_finalization = finalize_legacy(
        args.legacy_regression_out,
        equivalence_report=equivalence_path,
        reconciliation_report=reconciliation_path,
    )

    golden = run_v1_golden(args.rule_root)
    golden_ok = (
        not golden.unmatched
        and not golden.errors
        and golden.graph_ok
        and all(golden.coverage.get(key, False) for key in REQUIRED_COVERAGE)
    )

    client_report = run_client_regression(run_dir)
    client_ok = all(client_report.client_artifacts_ok.get(c, False) for c in required_clients) and not client_report.errors

    # Phase 5 rule-kind requirements are driven by the actual production IR and
    # the client capability matrix. URL is non-native for all seven clients in
    # the current matrix, and Aggregate is an entity type rather than a native
    # rule type; neither should become a false hard failure when the production
    # build cannot natively emit them.
    ir_path = run_dir / "ir" / "ir.json"
    semantic_contract_path = run_dir / "semantic" / "contract.json"
    aggregate_present = False
    if ir_path.is_file():
        ir = _json(ir_path)
        actual_types = {
            str(r.get("type", "")).strip().casefold()
            for r in (ir.get("rules") or [])
            if isinstance(r, dict)
        }
        aggregate_present = bool((ir.get("entities") or {}).get("aggregates"))
    elif semantic_contract_path.is_file():
        semantic_contract = _json(semantic_contract_path)
        actual_types = {
            str(t).strip().casefold()
            for t in (semantic_contract.get("rule_types") or [])
            if str(t).strip()
        }
    else:
        actual_types = set()
    kind_presence = {
        "domain": "domain" in actual_types,
        "suffix": "domain_suffix" in actual_types,
        "keyword": "domain_keyword" in actual_types,
        "CIDR": bool({"ip_cidr", "ip_cidr6"} & actual_types),
        "URL": "url" in actual_types,
        "Aggregate": aggregate_present,
    }
    matrix = _yaml(ROOT / "config/client_capability_matrix.yaml")
    supported_any = {
        "domain": any("domain" in {str(x).casefold() for x in (cfg.get("native_rule_types") or [])} for cfg in (matrix.get("clients") or {}).values() if isinstance(cfg, dict)),
        "suffix": any("domain_suffix" in {str(x).casefold() for x in (cfg.get("native_rule_types") or [])} for cfg in (matrix.get("clients") or {}).values() if isinstance(cfg, dict)),
        "keyword": any("domain_keyword" in {str(x).casefold() for x in (cfg.get("native_rule_types") or [])} for cfg in (matrix.get("clients") or {}).values() if isinstance(cfg, dict)),
        "CIDR": any({"ip_cidr", "ip_cidr6"} & {str(x).casefold() for x in (cfg.get("native_rule_types") or [])} for cfg in (matrix.get("clients") or {}).values() if isinstance(cfg, dict)),
        "URL": any("url" in {str(x).casefold() for x in (cfg.get("native_rule_types") or [])} for cfg in (matrix.get("clients") or {}).values() if isinstance(cfg, dict)),
        "Aggregate": False,
    }
    required_kind = {kind: bool(kind_presence[kind] and supported_any[kind]) for kind in RULE_KINDS}
    kind_ok = {
        kind: (not required_kind[kind]) or any(item.present for item in client_report.results if item.kind == kind)
        for kind in RULE_KINDS
    }
    phase5_ok = client_ok and all(kind_ok.values())

    determinism = _json(args.determinism_report)
    phase6_ok = bool(determinism.get("all_pass") and determinism.get("match"))

    production = check_production_run(run_dir)
    head = check_head(args.expected_commit)

    hard_errors = legacy_errors + v1_errors + [
        str(e.get("error", e)) if isinstance(e, dict) else str(e)
        for e in index.errors
    ]
    phase7_ok = (
        phase7_finalization.get("all_pass") is True
        and not phase7.unexplained_removed
        and not phase7.errors
        and equivalence["at_100"]
        and equivalence["passed"]
    )

    final_ok = (
        catalogue.at_100
        and equivalence["at_100"]
        and equivalence["passed"]
        and golden_ok
        and phase5_ok
        and phase6_ok
        and phase7_ok
        and production["pass"]
        and head["pass"]
        and not hard_errors
    )

    phase8 = evaluate_phase8_gates(
        catalogue,
        unexplained_removed=phase7.unexplained_removed,
        intentional_valid=not catalogue.intentional_errors,
        graph_ok=golden.graph_ok,
        golden_ok=golden_ok,
        legacy_asset_equivalence_ok=(equivalence["at_100"] and equivalence["passed"]),
        client_regression_ok=phase5_ok,
        deterministic_ok=phase6_ok,
        production_run_ok=production["pass"],
        current_head_ok=head["pass"],
    )
    if final_ok:
        phase8 = switch_sot_to_v1(phase8)
        phase8.legacy_asset_equivalence = equivalence
    else:
        phase8.legacy_asset_equivalence = equivalence

    final = {
        "schema": "v1_final_migration_gate_v1",
        "run_id": args.run_id,
        "status": "PASS" if final_ok else "BLOCKED",
        "legacy_source": str(args.legacy_root.relative_to(ROOT)),
        "v1_source": str(args.rule_root.relative_to(ROOT)),
        "catalogue_coverage": catalogue.to_dict(),
        "legacy_asset_equivalence": equivalence,
        "phase4_golden": {
            "pass": golden_ok,
            "coverage": golden.coverage,
            "unmatched": golden.unmatched,
            "errors": golden.errors,
        },
        "phase5_client_regression": {
            "pass": phase5_ok,
            "clients": client_report.client_artifacts_ok,
            "kind_coverage": kind_ok,
            "required_kind": required_kind,
            "production_kind_presence": kind_presence,
            "supported_by_any_client": supported_any,
            "errors": client_report.errors,
        },
        "phase6_full_determinism": determinism,
        "phase7_asset_regression": {
            "pass": bool(not phase7.unexplained_removed and not phase7.errors and equivalence["at_100"] and equivalence["passed"]),
            "counts": phase7.counts,
            "unexplained_removed": phase7.unexplained_removed,
            "errors": phase7.errors,
        },
        "phase7_finalization": {
            "pass": phase7_finalization.get("all_pass") is True,
            "regression_pass": phase7_finalization.get("regression_pass") is True,
            "equivalence_pass": phase7_finalization.get("equivalence_pass") is True,
            "reconciliation_pass": phase7_finalization.get("reconciliation_pass") is True,
            "migration_blocked": phase7_finalization.get("migration_blocked") is True,
            "blockers": phase7_finalization.get("blockers", []),
            "reconciliation_summary": reconciliation.get("summary", {}),
        },
        "production_run": production,
        "current_head": head,
        "hard_errors": hard_errors,
        "phase8": phase8.to_dict(),
        "deletion_boundary": {
            "target": str(args.legacy_root.relative_to(ROOT)),
            "authorized": bool(phase8.legacy_delete_allowed),
            "automatic_delete": False,
        },
    }

    finalization_path = ROOT / "reports/v1/LEGACY_FINALIZATION_PHASE7.json"
    finalization_path.parent.mkdir(parents=True, exist_ok=True)
    finalization_path.write_text(
        json.dumps(phase7_finalization, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for path, payload in (
        (args.json_out, final),
        (args.phase8_out, phase8.to_dict()),
        (args.legacy_regression_out, {
            "schema": "v1_legacy_regression_final_v2",
            "counts": phase7.counts,
            "unexplained_removed": phase7.unexplained_removed,
            "errors": phase7.errors,
            "all_pass": phase7_ok,
            "asset_equivalence": equivalence,
        }),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(final, indent=2, ensure_ascii=False))
    return 0 if final_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
