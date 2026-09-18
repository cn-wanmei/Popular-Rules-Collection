"""Phase 7 — finalization of Legacy migration evidence.

Finalization is evidence-only. It never changes the Legacy source or writes
V1 assets. It converts existing regression/reconciliation evidence into one
operator-readable terminal state.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
FINALIZATION_SCHEMA = "v1_legacy_finalization_v1"
@dataclass
class LegacyFinalizationReport:
    schema: str = FINALIZATION_SCHEMA
    regression_pass: bool = False
    equivalence_pass: bool = False
    reconciliation_pass: bool = False
    migration_blocked: bool = True
    blockers: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    @property
    def all_pass(self) -> bool:
        return self.regression_pass and self.equivalence_pass and self.reconciliation_pass and not self.blockers
    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "regression_pass": self.regression_pass,
            "equivalence_pass": self.equivalence_pass,
            "reconciliation_pass": self.reconciliation_pass,
            "migration_blocked": self.migration_blocked,
            "blockers": sorted(self.blockers),
            "evidence": self.evidence,
            "all_pass": self.all_pass,
        }
def _load(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError): return {}
    return data if isinstance(data, dict) else {}
def finalize_legacy(
    regression_report: Path,
    *,
    equivalence_report: Path | None = None,
    reconciliation_report: Path | None = None,
) -> dict[str, Any]:
    regression = _load(Path(regression_report))
    equivalence = _load(Path(equivalence_report)) if equivalence_report else {}
    reconciliation = _load(Path(reconciliation_report)) if reconciliation_report else {}
    regression_pass = regression.get("all_pass") is True and not regression.get("unexplained_removed")
    equivalence_pass = (equivalence.get("passed") is True and equivalence.get("at_100") is True) if equivalence else False
    reconciliation_summary = reconciliation.get("summary", {})
    reconciliation_pass = bool(
        reconciliation and reconciliation.get("promotion", {}).get("blocked") is True
        and reconciliation_summary.get("metadata_only_services", 1) == 0
        and reconciliation_summary.get("orphan_list_files", 1) == 0
        and reconciliation_summary.get("duplicate_domain_services", 1) == 0
        and reconciliation_summary.get("duplicate_ip_services", 1) == 0
        and reconciliation_summary.get("domain_count_delta_services", 1) == 0
        and reconciliation_summary.get("ip_count_delta_services", 1) == 0
    )
    report = LegacyFinalizationReport(
        regression_pass=bool(regression_pass),
        equivalence_pass=bool(equivalence_pass),
        reconciliation_pass=bool(reconciliation_pass),
        migration_blocked=True,
        evidence={"regression": regression, "equivalence": equivalence, "reconciliation": reconciliation},
    )
    if not report.regression_pass: report.blockers.append("legacy_regression_not_final")
    if not report.equivalence_pass: report.blockers.append("legacy_asset_equivalence_not_final")
    if not report.reconciliation_pass: report.blockers.append("legacy_reconciliation_not_final")
    return report.to_dict()
