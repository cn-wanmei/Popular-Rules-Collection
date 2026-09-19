"""Phase 2.1.2 reconciliation for the Legacy Asset IR.

This module compares extractor evidence with rule/_index.yaml without
promoting anything into the canonical V1 model. Counts are classified as
exact, duplicate-induced, count-delta, or unresolved; hierarchy and aggregate
asset evidence remain separate from promotion decisions.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from src.engine.ingest.legacy_asset_extractor import extract_legacy_asset_ir

SCHEMA = "legacy_asset_reconciliation_v1"


def _load_jsonl(path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, set[tuple[str, str]]]]:
    services: dict[str, dict[str, Any]] = defaultdict(lambda: {"raw": Counter(), "unique": Counter()})
    assets_by_service: dict[str, set[tuple[str, str]]] = defaultdict(set)
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            service = str(item["service"]).strip().lower()
            asset = item["asset"]
            kind = str(asset["type"])
            value = str(asset["value"])
            occurrences = int(item.get("occurrences", 1))
            services[service]["unique"][kind] += 1
            services[service]["raw"][kind] += occurrences
            assets_by_service[service].add((kind, value))
    return services, assets_by_service


def _classify(index_count: int | None, unique_count: int, raw_count: int) -> dict[str, Any]:
    duplicate_delta = max(raw_count - unique_count, 0)
    count_delta = None if index_count is None else unique_count - index_count
    if index_count is None:
        status = "no-index-stat"
    elif unique_count == index_count:
        status = "exact-match"
    elif raw_count == index_count and duplicate_delta:
        status = "duplicate-induced-delta"
    else:
        status = "count-delta"
    return {
        "index": index_count,
        "unique_extracted": unique_count,
        "raw_occurrences": raw_count,
        "count_delta": count_delta,
        "duplicate_induced_delta": duplicate_delta,
        "status": status,
    }


def reconcile_legacy_assets(rule_root: Path, *, jsonl_output: Path, report_path: Path | None = None, candidates_path: Path | None = None) -> dict[str, Any]:
    """Extract once, reconcile the generated JSONL, and optionally write reports."""
    # Reconciliation compares ordinary generated *.list evidence against
    # rule/_index.yaml. The Phase 8 migration supplement is separate evidence
    # and must not inflate indexed domain/IP counts.
    ir = extract_legacy_asset_ir(
        Path(rule_root),
        include_phase8_equivalence=False,
        jsonl_output=Path(jsonl_output),
    )
    raw, assets_by_service = _load_jsonl(Path(jsonl_output))
    services: list[dict[str, Any]] = []
    summary_by_id = {s.id: s.as_dict() for s in ir.services}
    indexed_ids = {s.id for s in ir.services if s.index_present}
    metadata_ids = {s.id for s in ir.services if s.metadata_present}
    aggregate_ids = {s.id for s in ir.services if s.service_type == "aggregate"}

    for item in ir.services:
        s = summary_by_id[item.id]
        data = raw.get(item.id, {"raw": Counter(), "unique": Counter()})
        domain_unique = sum(data["unique"][k] for k in ("domain", "domain_suffix", "domain_keyword", "domain_regex"))
        domain_raw = sum(data["raw"][k] for k in ("domain", "domain_suffix", "domain_keyword", "domain_regex"))
        cidr_unique = data["unique"]["ip_cidr"]
        cidr_raw = data["raw"]["ip_cidr"]
        metadata_index_status = "both-present" if item.metadata_present and item.index_present else ("metadata-only" if item.metadata_present else "index-only")
        services.append({
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "service_type": item.service_type,
            "parent": item.parent,
            "metadata_index_status": metadata_index_status,
            "domain": _classify(item.index_domains, domain_unique, domain_raw),
            "ip_cidr": _classify(item.index_ips, cidr_unique, cidr_raw),
            "urls": int(item.urls),
            "records": int(item.records),
            "source_files": sorted(item.source_files),
            "metadata_statistics": item.metadata_statistics,
            "generated_files": item.generated_files,
            "errors": list(item.errors),
            "relation_drift": next((d for d in ir.relation_drift if d["aggregate"] == item.id), None),
            "profile": ir.profile.get("services", {}).get(item.id, {}),
        })

    # source_files contains only files represented by an emitted unique asset.
    # profile.files is the authoritative extractor-level inventory of every
    # parsed *.list file, including files whose records were all duplicates.
    known_files = {str(entry["path"]) for entry in ir.profile.get("files", [])}
    all_list_files = {p.as_posix() for p in Path(rule_root).rglob("*.list") if p.is_file()}
    orphan_files = sorted(all_list_files - known_files)

    aggregate_evidence: list[dict[str, Any]] = []
    for aggregate in sorted(aggregate_ids):
        indexed_children = next((d["indexed_children"] for d in ir.relation_drift if d["aggregate"] == aggregate), [])
        if not indexed_children:
            indexed_children = [s.id for s in ir.services if s.parent == aggregate and s.id in indexed_ids]
        own = assets_by_service.get(aggregate, set())
        child_union: set[tuple[str, str]] = set()
        for child in indexed_children:
            child_union.update(assets_by_service.get(child, set()))
        aggregate_evidence.append({
            "aggregate": aggregate,
            "indexed_children": sorted(indexed_children),
            "own_unique_assets": len(own),
            "child_union_unique_assets": len(child_union),
            "own_assets_not_in_child_union": len(own - child_union),
            "child_union_assets_in_own": len(own & child_union),
            "parent_own_assets_first_class": True,
            "status": "own-assets-present" if own - child_union else "child-union-only-or-empty",
            "relation_drift": next((d for d in ir.relation_drift if d["aggregate"] == aggregate), None),
        })

    candidates: list[dict[str, Any]] = []
    for s in services:
        blocking: list[str] = []
        if s["metadata_index_status"] != "both-present":
            blocking.append(s["metadata_index_status"])
        if s["errors"]:
            blocking.append("extractor-errors")
        if s["domain"]["status"] not in {"exact-match", "duplicate-induced-delta"}:
            blocking.append("domain-reconciliation")
        if s["ip_cidr"]["status"] not in {"exact-match", "duplicate-induced-delta"}:
            blocking.append("ip-reconciliation")
        if s["service_type"] == "aggregate":
            blocking.append("aggregate-requires-explicit-mapping")
        if s["relation_drift"]:
            blocking.append("aggregate-relation-drift")
        candidates.append({
            "id": s["id"],
            "candidate": not blocking,
            "promotion_status": "blocked-until-canonical-review",
            "blocking_evidence": blocking,
            "evidence": {
                "domain_status": s["domain"]["status"],
                "ip_status": s["ip_cidr"]["status"],
                "url_count": s["urls"],
                "records": s["records"],
            },
        })

    report = {
        "schema": SCHEMA,
        "phase": "phase2.1.2-legacy-asset-reconciliation",
        "promotion": {"blocked": True, "canonical_v1_write": False},
        "source": {
            "legacy_asset_ir": "generated from rule/**",
            "index": "rule/_index.yaml",
            "note": "Legacy evidence is not canonical V1 source of truth.",
        },
        "summary": {
            "services": len(services),
            "indexed_services": len(indexed_ids),
            "metadata_services": len(metadata_ids),
            "metadata_only_services": len(metadata_ids - indexed_ids),
            "index_only_services": len(indexed_ids - metadata_ids),
            "aggregate_services": len(aggregate_ids),
            "orphan_list_files": len(orphan_files),
            "exact_domain_services": sum(1 for s in services if s["domain"]["status"] == "exact-match"),
            "exact_ip_services": sum(1 for s in services if s["ip_cidr"]["status"] == "exact-match"),
            "duplicate_domain_services": sum(1 for s in services if s["domain"]["status"] == "duplicate-induced-delta"),
            "duplicate_ip_services": sum(1 for s in services if s["ip_cidr"]["status"] == "duplicate-induced-delta"),
            "domain_count_delta_services": sum(1 for s in services if s["domain"]["status"] == "count-delta"),
            "ip_count_delta_services": sum(1 for s in services if s["ip_cidr"]["status"] == "count-delta"),
            "url_assets": sum(s["urls"] for s in services),
        },
        "orphan_assets": {"files": orphan_files, "definition": "*.list files not parsed by the extractor file inventory"},
        "aggregate_own_assets": aggregate_evidence,
        "relation_drift": ir.relation_drift,
        "services": services,
        "promotion_candidates": candidates,
    }
    if report_path is not None:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(report, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if candidates_path is not None:
        path = Path(candidates_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump({
            "schema": "v1_promotion_candidates_v1",
            "phase": "phase2.1.2-legacy-asset-reconciliation",
            "promotion": {"blocked": True, "canonical_v1_write": False},
            "candidate_count": sum(1 for item in candidates if item["candidate"]),
            "candidates": candidates,
        }, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return report


__all__ = ["reconcile_legacy_assets"]
