"""V1 Rule Loader — rule/ directory → Canonical ingest_result.

This is the Phase 3.1 entry point.  It reads the V1 source of truth
(rule/_index.yaml + per-service metadata.yaml + .list rule files) and
produces the ``ingest_result`` dict expected by
``src.engine.canonical.store.build_canonical``.

Pipeline position:
    rule/                 ← V1 authoritative repository layout
      ↓  v1_loader.load_v1_rules()
    ingest_result         ← {records, errors, manifest}
      ↓  canonical.store.build_canonical()
    data/.../canonical/   ← rules.jsonl / memberships.jsonl / manifest.json
      ↓  ir.builder.build_ir()
    Semantic IR           ← entities / views / rules / decisions

Design constraints (from Phase 2 safety boundary):
    - Never delete or modify Legacy assets
    - Never treat generated outputs as Source of Truth
    - Every parse error goes to errors[], never silently dropped
    - Rule deduplication uses full SHA-256 identity_key (Rule model)
    - Aggregate entries produce records only for their declared
      direct rules, NOT a synthetic union of children's rules
      (children are resolved by the Hierarchy resolver at IR stage)
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.ingest.rule_parser import iter_rules
from src.engine.ingest.v1_index import ServiceEntry, V1IndexResult, load_v1_index

# Rule list file preference order: mixed > domain-only > ip-only
_LIST_PREFERENCE = [
    lambda sid: f"{sid}.list",
    lambda sid: f"{sid}_domain.list",
    lambda sid: f"{sid}_ip.list",
]

# Hard limit: skip per-file parse if estimated line count exceeds threshold
# to avoid pathological runtimes on very large aggregates during Loader init.
_LINE_LIMIT = 500_000


def _find_rule_files(entry: ServiceEntry, rule_root: Path) -> list[Path]:
    """Return all .list files for an entry, sorted by preference then name."""
    if not entry.path:
        return []
    service_dir = rule_root.parent / entry.path
    if not service_dir.is_dir():
        return []
    # Collect all .list files; exclude README/metadata
    all_lists = sorted(
        (p for p in service_dir.iterdir() if p.suffix == ".list" and p.is_file()),
        key=lambda p: p.name,
    )
    return all_lists


def _parse_list_file(
    path: Path,
    service_id: str,
    category: str,
    errors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Parse a single .list file into raw records."""
    records: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        errors.append({
            "stage": "v1_loader",
            "service": service_id,
            "path": str(path),
            "error": f"read error: {exc}",
        })
        return records

    line_count = text.count("\n")
    if line_count > _LINE_LIMIT:
        errors.append({
            "stage": "v1_loader",
            "service": service_id,
            "path": str(path),
            "error": f"file too large ({line_count} lines > {_LINE_LIMIT}), skipped",
            "severity": "warning",
        })
        return records

    # Use the engine's existing rule_parser which handles all known formats
    try:
        for typ, val in iter_rules(path):
            records.append({
                "service": service_id,
                "type": typ,
                "value": val,
                "category": category,
                "provenance": {
                    "loader": "v1_loader",
                    "path": str(path.relative_to(path.parents[3])),
                    "format": "v1_list",
                },
            })
    except Exception as exc:
        errors.append({
            "stage": "v1_loader",
            "service": service_id,
            "path": str(path),
            "error": f"parse error: {exc}",
        })

    return records


def load_v1_rules(
    rule_root: Path,
    *,
    include_aggregates: bool = False,
    service_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Load all V1 rule assets into Canonical ingest_result format.

    Args:
        rule_root: Path to the ``rule/`` directory.
        include_aggregates: If True, also load rule files for aggregate entries.
            Default False — aggregates are resolved by the Hierarchy layer.
        service_ids: If provided, only load these service IDs (useful for
            incremental / targeted reloads).

    Returns:
        ingest_result dict with keys:
            records  — list of {service, type, value, category, provenance}
            errors   — list of {stage, service, path, error}
            manifest — metadata about this load run
    """
    rule_root = Path(rule_root)
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    # Phase 1: load the index
    index: V1IndexResult = load_v1_index(rule_root)
    errors.extend(index.errors)

    # Phase 2: for each entry, parse rule files
    loaded_services: list[str] = []
    skipped_aggregates: list[str] = []

    for entry in index.entries:
        # Filter by caller-specified service set
        if service_ids is not None and entry.id not in service_ids:
            continue

        # Aggregates are skipped unless explicitly requested
        if entry.is_aggregate and not include_aggregates:
            skipped_aggregates.append(entry.id)
            continue

        primary_category = next(iter(sorted(entry.categories)), "unknown")
        rule_files = _find_rule_files(entry, rule_root)

        if not rule_files:
            # Index entry has no rule files yet — record as warning, not error
            errors.append({
                "stage": "v1_loader",
                "service": entry.id,
                "path": entry.path,
                "error": "no .list files found",
                "severity": "warning",
            })
            continue

        file_records = 0
        for rfile in rule_files:
            batch = _parse_list_file(rfile, entry.id, primary_category, errors)
            records.extend(batch)
            file_records += len(batch)

        if file_records > 0:
            loaded_services.append(entry.id)

    manifest = {
        "schema": "v1_loader_manifest_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "loader": "v1_loader",
        "rule_root": str(rule_root),
        "index_path": index.index_path,
        "index_entry_count": index.entry_count,
        "service_count": index.service_count,
        "aggregate_count": index.aggregate_count,
        "category_count": index.category_count,
        "loaded_services": sorted(loaded_services),
        "skipped_aggregates": sorted(skipped_aggregates),
        "records_total": len(records),
        "errors_total": len(errors),
        "include_aggregates": include_aggregates,
    }

    return {
        "records": records,
        "errors": errors,
        "manifest": manifest,
    }


def load_v1_rules_for_service(rule_root: Path, service_id: str) -> dict[str, Any]:
    """Convenience wrapper: load a single service's rules."""
    return load_v1_rules(rule_root, service_ids={service_id}, include_aggregates=True)


# ---------------------------------------------------------------------------
# CLI entry point (python -m src.engine.ingest.v1_loader rule/)
# ---------------------------------------------------------------------------

def _main() -> None:
    import argparse
    import sys

    ap = argparse.ArgumentParser(description="V1 Loader — dump ingest_result as JSON")
    ap.add_argument("rule_root", type=Path, help="Path to rule/ directory")
    ap.add_argument("--service", help="Only load this service ID")
    ap.add_argument("--include-aggregates", action="store_true")
    ap.add_argument("--manifest-only", action="store_true", help="Print manifest only")
    args = ap.parse_args()

    result = load_v1_rules(
        args.rule_root,
        include_aggregates=args.include_aggregates,
        service_ids={args.service} if args.service else None,
    )

    if args.manifest_only:
        print(json.dumps(result["manifest"], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    if result["errors"]:
        hard_errors = [e for e in result["errors"] if e.get("severity") != "warning"]
        if hard_errors:
            sys.exit(1)


if __name__ == "__main__":
    _main()
