"""Phase 8 — Ordered migration controller.

Hard order (must not be reordered):

    1. Complete catalogue (materialize OR register intentional)
    2. Coverage == 100%
    3. Formal migration: Legacy → V1 Canonical as Source of Truth
    4. Only then: allow deletion of Legacy Source

This module never deletes Legacy by itself.  Deletion is a separate,
explicit action that refuses to run unless every prior gate has passed
and ``allow_legacy_delete=True`` is supplied by an operator.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# SSOT intentional codes (docs/RELEASE_AND_QC.md)
INTENTIONAL_CODES: frozenset[str] = frozenset(
    {
        "NO_UPSTREAM",
        "COVERED_BY_AGGREGATE",
        "MAPS_TO",
        "DEFERRED_PROFILE",
        "KEYWORD_ONLY",
        "SOURCE_DRIFT",
    }
)

DEFAULT_INTENTIONAL_PATH = Path("config/intentional_unmaterialized.yaml")


# ---------------------------------------------------------------------------
# Intentional registry
# ---------------------------------------------------------------------------

@dataclass
class IntentionalEntry:
    service_id: str
    code: str
    reason: str = ""


def load_intentional_registry(path: Path | None = None) -> dict[str, IntentionalEntry]:
    """Load config/intentional_unmaterialized.yaml → {service_id: entry}."""
    path = Path(path or DEFAULT_INTENTIONAL_PATH)
    if not path.exists():
        return {}
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    services = doc.get("services") or {}
    out: dict[str, IntentionalEntry] = {}
    for sid, meta in services.items():
        if not isinstance(meta, dict):
            continue
        out[str(sid).strip().casefold()] = IntentionalEntry(
            service_id=str(sid).strip(),
            code=str(meta.get("code", "")).strip().upper(),
            reason=str(meta.get("reason", "")).strip(),
        )
    return out


def validate_intentional_registry(
    registry: dict[str, IntentionalEntry],
) -> list[str]:
    """Return list of validation errors (empty = OK)."""
    errors: list[str] = []
    for key, entry in registry.items():
        if entry.code not in INTENTIONAL_CODES:
            errors.append(
                f"invalid intentional code for {entry.service_id!r}: {entry.code!r} "
                f"(allowed: {sorted(INTENTIONAL_CODES)})"
            )
        if not entry.reason:
            errors.append(f"intentional entry {entry.service_id!r} missing reason")
    return errors


# ---------------------------------------------------------------------------
# Coverage
# ---------------------------------------------------------------------------

@dataclass
class CoverageReport:
    schema: str = "v1_phase8_coverage_v1"
    registered: int = 0
    materialized: int = 0
    intentional: int = 0
    missing: list[str] = field(default_factory=list)
    coverage_ratio: float = 0.0
    coverage_pct: float = 0.0
    coverage_kind: str = "catalogue_coverage"
    at_100: bool = False
    intentional_errors: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "registered": self.registered,
            "materialized": self.materialized,
            "intentional": self.intentional,
            "missing": self.missing,
            "coverage_ratio": self.coverage_ratio,
            "coverage_pct": round(self.coverage_pct, 4),
            "coverage_kind": self.coverage_kind,
            "at_100": self.at_100,
            "intentional_errors": self.intentional_errors,
            "details": self.details,
            "formula": "(materialized + intentional_unmaterialized) / registered",
        }


def compute_coverage(
    registered_ids: set[str],
    materialized_ids: set[str],
    intentional: dict[str, IntentionalEntry] | None = None,
) -> CoverageReport:
    """Daily Coverage = (materialized + intentional) / registered.

    registered_ids: all service ids expected in the catalogue
    materialized_ids: ids that have real rule assets in V1
    intentional: map of casefold id → IntentionalEntry
    """
    intentional = intentional or {}
    reg = {s.casefold() for s in registered_ids if s}
    mat = {s.casefold() for s in materialized_ids if s}
    int_ids = set(intentional.keys())

    # A service can be both materialized and intentional; count once as covered
    covered = (mat | (reg & int_ids))
    missing = sorted(reg - covered)

    intentional_only = (reg & int_ids) - mat
    report = CoverageReport(
        registered=len(reg),
        materialized=len(reg & mat),
        intentional=len(intentional_only),
        missing=missing,
    )
    if report.registered == 0:
        report.coverage_ratio = 0.0
        report.coverage_pct = 0.0
        report.at_100 = False
    else:
        report.coverage_ratio = len(covered) / report.registered
        report.coverage_pct = report.coverage_ratio * 100.0
        report.at_100 = len(missing) == 0

    report.intentional_errors = validate_intentional_registry(
        {k: v for k, v in intentional.items() if k in reg}
    )
    report.details = {
        "covered_count": len(covered),
        "intentional_only": sorted(intentional_only),
        "materialized_and_intentional": sorted(reg & mat & int_ids),
        "materialized_plus_intentional": report.materialized + report.intentional,
    }
    return report


def compute_coverage_from_index(
    rule_root: Path,
    intentional_path: Path | None = None,
) -> CoverageReport:
    """Convenience: registered = V1 index entries; materialized = leaf services
    with domains+ips > 0 or non-aggregate with a path.
    """
    from src.engine.ingest.v1_index import load_v1_index

    index = load_v1_index(Path(rule_root))
    registered = {e.id for e in index.entries}
    # Materialized: non-aggregate with path, or aggregate that declares children
    materialized: set[str] = set()
    for e in index.entries:
        if e.is_aggregate:
            if e.children or e.domains > 0 or e.ips > 0:
                materialized.add(e.id)
        else:
            if e.path:
                service_dir = Path(rule_root).parent / e.path
                if service_dir.is_dir() and any(
                    p.is_file() and p.suffix == ".list" and p.stat().st_size > 0
                    for p in service_dir.iterdir()
                ):
                    materialized.add(e.id)
    intentional = load_intentional_registry(intentional_path)
    return compute_coverage(registered, materialized, intentional)


# ---------------------------------------------------------------------------
# Migration gates
# ---------------------------------------------------------------------------

@dataclass
class MigrationGateResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class Phase8Report:
    schema: str = "v1_phase8_migration_v1"
    generated_at: str = ""
    stage: str = "inventory"  # inventory|coverage|ready|switched|legacy_deleted
    coverage: dict[str, Any] = field(default_factory=dict)
    legacy_asset_equivalence: dict[str, Any] = field(default_factory=dict)
    gates: list[MigrationGateResult] = field(default_factory=list)
    sot: str = "legacy"  # "legacy" | "v1_canonical"
    legacy_delete_allowed: bool = False
    legacy_deleted: bool = False
    errors: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "generated_at": self.generated_at,
            "stage": self.stage,
            "coverage": self.coverage,
            "legacy_asset_equivalence": self.legacy_asset_equivalence,
            "gates": [{"name": g.name, "passed": g.passed, "detail": g.detail} for g in self.gates],
            "sot": self.sot,
            "legacy_delete_allowed": self.legacy_delete_allowed,
            "legacy_deleted": self.legacy_deleted,
            "errors": self.errors,
            "blockers": self.blockers,
            "all_pass": (
                not self.errors
                and not self.blockers
                and all(g.passed for g in self.gates)
            ),
        }


def evaluate_phase8_gates(
    coverage: CoverageReport,
    *,
    unexplained_removed: list[str] | None = None,
    intentional_valid: bool = True,
    graph_ok: bool = True,
    golden_ok: bool = False,
    legacy_asset_equivalence_ok: bool = False,
    client_regression_ok: bool = False,
    deterministic_ok: bool = False,
    production_run_ok: bool = False,
    current_head_ok: bool = False,
) -> Phase8Report:
    """Evaluate ordered Phase 8 gates. Does not mutate any Source of Truth."""
    report = Phase8Report(
        generated_at=datetime.now(timezone.utc).isoformat(),
        coverage=coverage.to_dict(),
    )
    unexplained_removed = unexplained_removed or []

    gates = [
        MigrationGateResult(
            name="intentional_registry_valid",
            passed=intentional_valid and not coverage.intentional_errors,
            detail="; ".join(coverage.intentional_errors) or "ok",
        ),
        MigrationGateResult(
            name="coverage_100",
            passed=coverage.at_100,
            detail=(
                f"{coverage.coverage_pct:.2f}% "
                f"(materialized={coverage.materialized}, intentional_unmaterialized={coverage.intentional}, "
                f"registered={coverage.registered}, missing={len(coverage.missing)})"
            ),
        ),
        MigrationGateResult(
            name="no_unexplained_removed",
            passed=len(unexplained_removed) == 0,
            detail=f"unexplained={len(unexplained_removed)}",
        ),
        MigrationGateResult(
            name="graph_acyclic",
            passed=graph_ok,
            detail="ok" if graph_ok else "cycle or graph failure",
        ),
        MigrationGateResult(
            name="golden_gate",
            passed=golden_ok,
            detail="ok" if golden_ok else "golden coverage incomplete",
        ),
        MigrationGateResult(
            name="legacy_asset_equivalence_100",
            passed=legacy_asset_equivalence_ok,
            detail="ok" if legacy_asset_equivalence_ok else "Legacy Asset Equivalence not proven",
        ),
        MigrationGateResult(
            name="phase5_client_regression",
            passed=client_regression_ok,
            detail="ok" if client_regression_ok else "client regression incomplete",
        ),
        MigrationGateResult(
            name="phase6_full_determinism",
            passed=deterministic_ok,
            detail="ok" if deterministic_ok else "full V3 determinism not proven",
        ),
        MigrationGateResult(
            name="production_run_rc_ready",
            passed=production_run_ok,
            detail="ok" if production_run_ok else "production run is not RC_READY",
        ),
        MigrationGateResult(
            name="current_head_binding",
            passed=current_head_ok,
            detail="ok" if current_head_ok else "evidence not bound to current HEAD",
        ),
    ]
    report.gates = gates

    for g in gates:
        if not g.passed:
            report.blockers.append(f"{g.name}: {g.detail}")

    if coverage.at_100 and not report.blockers:
        report.stage = "ready"
        report.sot = "legacy"  # still legacy until explicit switch
    elif coverage.at_100:
        report.stage = "coverage"
    else:
        report.stage = "inventory"
        if coverage.missing:
            report.errors.append(
                f"coverage incomplete: {len(coverage.missing)} services missing "
                f"(neither materialized nor intentional)"
            )

    # Legacy delete only when ready AND operator would switch SoT first
    report.legacy_delete_allowed = False
    return report


def switch_sot_to_v1(report: Phase8Report) -> Phase8Report:
    """Mark formal migration: V1 Canonical becomes Source of Truth.

    Refuses if gates have not all passed.
    """
    if not all(g.passed for g in report.gates):
        report.errors.append("refuse SoT switch: not all Phase 8 gates passed")
        return report
    if not report.coverage.get("at_100"):
        report.errors.append("refuse SoT switch: coverage not 100%")
        return report
    report.sot = "v1_canonical"
    report.stage = "switched"
    report.legacy_delete_allowed = False
    return report


def request_legacy_delete(
    report: Phase8Report,
    *,
    allow_legacy_delete: bool = False,
    final_gate_passed: bool = False,
) -> Phase8Report:
    """Final step: only deletes conceptually when allow_legacy_delete=True.

    This function does **not** remove files.  It records authorization.
    Actual filesystem deletion must be a separate operator script that
    checks report.legacy_deleted authorization and report.sot == v1_canonical.
    """
    if report.sot != "v1_canonical":
        report.errors.append(
            "refuse legacy delete: SoT is still 'legacy'; run switch_sot_to_v1 first"
        )
        report.legacy_delete_allowed = False
        return report
    if not final_gate_passed:
        report.errors.append("refuse legacy delete: final migration gate is not PASS")
        report.legacy_delete_allowed = False
        return report
    if not allow_legacy_delete:
        report.errors.append(
            "refuse legacy delete: pass allow_legacy_delete=True after explicit operator approval"
        )
        return report
    if not all(g.passed for g in report.gates):
        report.errors.append("refuse legacy delete: gates no longer all green")
        return report
    report.legacy_delete_allowed = True
    report.legacy_deleted = True  # authorization flag only
    report.stage = "legacy_deleted"
    return report


def write_phase8_report(report: Phase8Report, out_path: Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
