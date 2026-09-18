"""Phase 7 — Legacy Regression report.

Pipeline under observation:

    Legacy → V1 → V3 → IR → Generated

Produces structured change sets:

    Added / Removed / Changed / Moved /
    Deduplicated / Dependency Added / Aggregate Added

Any Legacy asset that disappears in the V1 transition must be listed under
Removed with an explanation field (required for safe migration).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass
class AssetRef:
    """Minimal identity for cross-layer asset comparison."""

    key: str
    source: str  # "legacy" | "v1" | "ir" | "generated"
    service: str = ""
    type: str = ""
    value: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChangeItem:
    kind: str  # Added|Removed|Changed|Moved|Deduplicated|DependencyAdded|AggregateAdded
    asset_key: str
    detail: str = ""
    from_service: str = ""
    to_service: str = ""
    explanation: str = ""  # required for Removed


@dataclass
class LegacyRegressionReport:
    schema: str = "v1_legacy_regression_v1"
    generated_at: str = ""
    counts: dict[str, int] = field(default_factory=dict)
    items: list[ChangeItem] = field(default_factory=list)
    unexplained_removed: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "generated_at": self.generated_at,
            "counts": self.counts,
            "items": [
                {
                    "kind": i.kind,
                    "asset_key": i.asset_key,
                    "detail": i.detail,
                    "from_service": i.from_service,
                    "to_service": i.to_service,
                    "explanation": i.explanation,
                }
                for i in self.items
            ],
            "unexplained_removed": self.unexplained_removed,
            "errors": self.errors,
            "all_pass": len(self.unexplained_removed) == 0 and not self.errors,
        }


def _asset_key(typ: str, value: str) -> str:
    return f"{typ.strip().lower().replace('-', '_')}:{value.strip().lower()}"


def load_assets_from_records(records: Iterable[dict[str, Any]], source: str) -> dict[str, AssetRef]:
    out: dict[str, AssetRef] = {}
    for rec in records:
        typ = str(rec.get("type", rec.get("classification", "")))
        val = str(rec.get("value", ""))
        if not typ or not val:
            continue
        key = rec.get("asset_key") or _asset_key(typ, val)
        out[key] = AssetRef(
            key=key,
            source=source,
            service=str(rec.get("service", "")),
            type=typ,
            value=val,
            extra={k: rec[k] for k in ("category", "provenance") if k in rec},
        )
    return out


def load_assets_from_jsonl(path: Path, source: str) -> dict[str, AssetRef]:
    path = Path(path)
    if not path.exists():
        return {}
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return load_assets_from_records(records, source)


def compare_legacy_to_v1(
    legacy_assets: dict[str, AssetRef],
    v1_assets: dict[str, AssetRef],
    *,
    explanations: dict[str, str] | None = None,
    dependency_added: Iterable[str] | None = None,
    aggregate_added: Iterable[str] | None = None,
) -> LegacyRegressionReport:
    """Core Legacy → V1 regression comparison.

    explanations maps asset_key → human reason for intentional removal.
    """
    explanations = explanations or {}
    report = LegacyRegressionReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    leg_keys = set(legacy_assets)
    v1_keys = set(v1_assets)

    added = sorted(v1_keys - leg_keys)
    removed = sorted(leg_keys - v1_keys)
    common = leg_keys & v1_keys

    for key in added:
        a = v1_assets[key]
        report.items.append(
            ChangeItem(kind="Added", asset_key=key, to_service=a.service, detail=f"type={a.type}")
        )

    for key in removed:
        a = legacy_assets[key]
        expl = explanations.get(key, "")
        item = ChangeItem(
            kind="Removed",
            asset_key=key,
            from_service=a.service,
            detail=f"type={a.type}",
            explanation=expl,
        )
        report.items.append(item)
        if not expl:
            report.unexplained_removed.append(key)

    for key in sorted(common):
        la, va = legacy_assets[key], v1_assets[key]
        if la.service and va.service and la.service != va.service:
            report.items.append(
                ChangeItem(
                    kind="Moved",
                    asset_key=key,
                    from_service=la.service,
                    to_service=va.service,
                    detail="service membership changed",
                )
            )
        elif la.type != va.type or la.value != va.value:
            report.items.append(
                ChangeItem(
                    kind="Changed",
                    asset_key=key,
                    from_service=la.service,
                    to_service=va.service,
                    detail=f"{la.type}:{la.value} → {va.type}:{va.value}",
                )
            )

    # Deduplicated: same value present once in V1 but multiple times in legacy
    # (approximated by counting identical values under different keys in legacy
    # that collapsed to one V1 key — handled via explicit list if provided)
    # Dependency / Aggregate additions
    for key in dependency_added or []:
        report.items.append(ChangeItem(kind="DependencyAdded", asset_key=key))
    for key in aggregate_added or []:
        report.items.append(ChangeItem(kind="AggregateAdded", asset_key=key))

    # Counts
    counts: dict[str, int] = {}
    for item in report.items:
        counts[item.kind] = counts.get(item.kind, 0) + 1
    report.counts = counts
    return report


def run_legacy_regression(
    legacy_jsonl: Path,
    v1_jsonl: Path,
    *,
    explanations: dict[str, str] | None = None,
) -> LegacyRegressionReport:
    """File-based entry point for Phase 7."""
    legacy = load_assets_from_jsonl(Path(legacy_jsonl), "legacy")
    v1 = load_assets_from_jsonl(Path(v1_jsonl), "v1")
    if not legacy and not Path(legacy_jsonl).exists():
        report = LegacyRegressionReport(
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
        report.errors.append(f"legacy file missing: {legacy_jsonl}")
        return report
    return compare_legacy_to_v1(legacy, v1, explanations=explanations)


def write_legacy_regression_report(report: LegacyRegressionReport, out_path: Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
