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
    result: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for rec in records:
        result[rec["service"]].add((rec["type"], rec["value"]))
    return dict(result)


def audit_legacy_equivalence(
    legacy_records: list[dict[str, str]],
    v1_records: list[dict[str, str]],
    legacy_counts: dict[str, int],
    v1_counts: dict[str, int],
    intentional_ids: set[str],
) -> dict[str, Any]:
    legacy = _asset_sets(legacy_records)
    v1 = _asset_sets(v1_records)
    legacy_services = set(legacy) | set(legacy_counts)
    v1_services = set(v1) | set(v1_counts)

    missing_services = sorted(legacy_services - v1_services)
    extra_services = sorted(s for s in (v1_services - legacy_services) if s not in intentional_ids)
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
        "legacy_services": len(legacy_services),
        "v1_services": len(v1_services),
    }


def check_production_run(run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    manifest_path = run_dir / "run_manifest.json"
    release_path = run_dir / "release" / "manifest.json"
    if not manifest_path.is_file():
        errors.append(f"missing {manifest_path}")
        return {"pass": False, "errors": errors}
    manifest = _json(manifest_path)
    if manifest.get("status") != "ok":
        errors.append(f"run status={manifest.get('status')!r}")
    release = manifest.get("stages", {}).get("release", {})
    if release.get("state") != "RC_READY":
        errors.append(f"release state={release.get('state')!r}")
    if manifest.get("v2_runtime_dependency") != 0:
        errors.append(f"v2_runtime_dependency={manifest.get('v2_runtime_dependency')!r}")
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
    args = ap.parse_args()

    intentional = load_intentional_registry(ROOT / "config/intentional_unmaterialized.yaml")
    index = load_v1_index(args.rule_root)

    legacy_records, legacy_counts, legacy_errors = load_legacy_source_assets(args.legacy_root)
    v1_records, v1_counts, v1_errors = load_v1_source_assets(args.rule_root)

    registered = {e.id for e in index.entries}
    materialized = set(v1_counts)
    catalogue = compute_coverage(registered, materialized, intentional)

    equivalence = audit_legacy_equivalence(
        legacy_records, v1_records, legacy_counts, v1_counts, set(intentional)
    )

    legacy_for_regression = load_assets_from_records(legacy_records, "legacy")
    v1_for_regression = load_assets_from_records(v1_records, "v1")
    phase7 = compare_legacy_to_v1(legacy_for_regression, v1_for_regression)

    golden = run_v1_golden(args.rule_root)
    golden_ok = (
        not golden.unmatched
        and not golden.errors
        and golden.graph_ok
        and all(golden.coverage.get(key, False) for key in REQUIRED_COVERAGE)
    )

    run_dir = args.data_root / "runs" / args.run_id
    client_report = run_client_regression(run_dir)
    required_clients = ("mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon")
    client_ok = all(client_report.client_artifacts_ok.get(c, False) for c in required_clients) and not client_report.errors
    kind_ok = {
        kind: any(item.present for item in client_report.results if item.kind == kind)
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
    phase7_ok = not phase7.unexplained_removed and not phase7.errors and equivalence["at_100"] and equivalence["passed"]

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
        phase8 = request_legacy_delete(phase8, allow_legacy_delete=False, final_gate_passed=True)
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
            "errors": client_report.errors,
        },
        "phase6_full_determinism": determinism,
        "phase7_asset_regression": {
            "pass": phase7_ok,
            "counts": phase7.counts,
            "unexplained_removed": phase7.unexplained_removed,
            "errors": phase7.errors,
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
