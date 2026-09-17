"""Automated Legacy Asset Extractor for Phase 2.1.1.

The extractor treats ``rule/**`` as evidence, not as the canonical V1 model.
It walks service directories, reads metadata, parses generated ``*.list``
assets, preserves provenance, performs deterministic service-local
 de-duplication, and can stream a JSONL Legacy Asset IR without retaining the
full 835k+ domain inventory in memory.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import yaml

from src.engine.ingest.rule_parser import iter_rule_records_with_line

URL_RE = re.compile(r"^https?://[^\s]+$", re.I)
ASSET_LIST_RE = re.compile(r"^[^/]+(?:\.list)$", re.I)


@dataclass(frozen=True)
class LegacyAsset:
    service: str
    category: str
    service_type: str
    parent: str | None
    asset_type: str
    value: str
    generated_file: str
    path: str
    line: int
    detected_format: str
    sources: tuple[str, ...] = ()

    def identity(self) -> tuple[str, str, str]:
        return self.service, self.asset_type, self.value

    def as_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "category": self.category,
            "service_type": self.service_type,
            "parent": self.parent,
            "asset": {"type": self.asset_type, "value": self.value},
            "provenance": {
                "generated_file": self.generated_file,
                "path": self.path,
                "line": self.line,
                "detected_format": self.detected_format,
                "sources": list(self.sources),
            },
        }


@dataclass
class AssetEvidence:
    asset: LegacyAsset
    occurrences: int = 1
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        item = self.asset.as_dict()
        item["evidence"] = list(self.evidence)
        item["occurrences"] = self.occurrences
        return item


@dataclass
class ServiceAssetSummary:
    id: str
    name: str
    category: str
    categories: list[str]
    service_type: str
    parent: str | None
    children: list[str]
    domains: int = 0
    domain_suffixes: int = 0
    domain_keywords: int = 0
    domain_regexes: int = 0
    cidrs: int = 0
    urls: int = 0
    hosts: int = 0
    process_rules: int = 0
    records: int = 0
    source_files: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    metadata_present: bool = False
    index_present: bool = False
    index_domains: int | None = None
    index_ips: int | None = None
    metadata_statistics: dict[str, Any] = field(default_factory=dict)
    generated_files: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "categories": self.categories,
            "service_type": self.service_type,
            "parent": self.parent,
            "children": self.children,
            "assets": {
                "domains": self.domains,
                "domain_suffixes": self.domain_suffixes,
                "domain_keywords": self.domain_keywords,
                "domain_regexes": self.domain_regexes,
                "ip_cidrs": self.cidrs,
                "urls": self.urls,
                "hosts": self.hosts,
                "process_rules": self.process_rules,
            },
            "records": self.records,
            "source_files": sorted(self.source_files),
            "sources": sorted(set(self.sources)),
            "metadata_present": self.metadata_present,
            "index_present": self.index_present,
            "index_statistics": {
                "domains": self.index_domains,
                "ips": self.index_ips,
            },
            "metadata_statistics": self.metadata_statistics,
            "generated_files": self.generated_files,
            "errors": self.errors,
        }


@dataclass
class LegacyAssetIR:
    schema: str
    generated_at: str
    source: dict[str, Any]
    services: list[ServiceAssetSummary]
    totals: dict[str, int]
    relation_drift: list[dict[str, Any]]
    profile: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "generated_at": self.generated_at,
            "source": self.source,
            "summary": {"services": len(self.services), **self.totals},
            "services": [item.as_dict() for item in self.services],
            "relation_drift": self.relation_drift,
            "profile": self.profile,
        }


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    return data if isinstance(data, dict) else {}


def _index_records(index_path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    data = _load_yaml(index_path)
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for category, payload in (data.get("categories") or {}).items():
        if not isinstance(payload, dict):
            continue
        for rule in payload.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            rid = str(rule.get("id", "")).strip().lower()
            if not rid:
                continue
            result[(str(category), rid)] = {
                "category": str(category),
                "id": rid,
                "name": rule.get("name") or rid,
                "path": rule.get("path"),
                "service_type": rule.get("service_type", "service"),
                "domains": rule.get("domains"),
                "ips": rule.get("ips"),
            }
    return result


def _metadata_for(directory: Path) -> dict[str, Any]:
    return _load_yaml(directory / "metadata.yaml")


def _asset_type(raw_type: str, value: str) -> str:
    if URL_RE.match(value):
        return "url"
    mapping = {
        "domain": "domain",
        "domain_suffix": "domain_suffix",
        "domain_keyword": "domain_keyword",
        "domain_regex": "domain_regex",
        "host": "host",
        "host_keyword": "host_keyword",
        "ip_cidr": "ip_cidr",
        "ip_cidr6": "ip_cidr",
        "process_name": "process_name",
        "process_path": "process_path",
    }
    return mapping.get(raw_type, raw_type)


def _iter_asset_records(path: Path) -> Iterator[tuple[Path, int, str, str, str]]:
    """Yield exact source provenance from the parser in one pass."""
    yield from iter_rule_records_with_line(path)


def _update_counts(summary: ServiceAssetSummary, asset_type: str) -> None:
    if asset_type == "domain":
        summary.domains += 1
    elif asset_type == "domain_suffix":
        summary.domain_suffixes += 1
    elif asset_type == "domain_keyword":
        summary.domain_keywords += 1
    elif asset_type == "domain_regex":
        summary.domain_regexes += 1
    elif asset_type == "ip_cidr":
        summary.cidrs += 1
    elif asset_type == "url":
        summary.urls += 1
    elif asset_type in {"host", "host_keyword"}:
        summary.hosts += 1
    elif asset_type in {"process_name", "process_path"}:
        summary.process_rules += 1


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _profile_file(profile: dict[str, Any], item: dict[str, Any]) -> None:
    profile.setdefault("files", []).append(item)
    totals = profile.setdefault("totals", {})
    totals["files"] = totals.get("files", 0) + 1
    for key in ("parser_seconds", "dedup_seconds", "total_seconds"):
        totals[key] = totals.get(key, 0.0) + float(item.get(key, 0.0))


def iter_service_assets(
    rule_root: Path,
    *,
    include_aggregates: bool = True,
    profile: dict[str, Any] | None = None,
) -> Iterator[AssetEvidence]:
    """Stream de-duplicated evidence, retaining state only for one service."""
    rule_root = Path(rule_root)
    profile = profile if profile is not None else {}
    services_profile = profile.setdefault("services", {})
    for category_dir in sorted(p for p in rule_root.iterdir() if p.is_dir()):
        for service_dir in sorted(p for p in category_dir.iterdir() if p.is_dir()):
            service_start = time.perf_counter()
            metadata_start = time.perf_counter()
            metadata = _metadata_for(service_dir)
            metadata_seconds = time.perf_counter() - metadata_start
            service_id = str(metadata.get("id") or service_dir.name).strip().lower()
            service_type = str(metadata.get("service_type") or "service").strip().lower()
            if not include_aggregates and service_type == "aggregate":
                continue
            parent = metadata.get("parent")
            parent = str(parent).strip().lower() if parent else None
            sources = tuple(sorted({str(v).strip() for v in (metadata.get("sources") or []) if str(v).strip()}))
            seen: dict[tuple[str, str, str], AssetEvidence] = {}
            service_file_count = 0
            service_raw_records = 0
            for list_path in sorted(p for p in service_dir.iterdir() if p.is_file() and ASSET_LIST_RE.match(p.name)):
                service_file_count += 1
                file_start = time.perf_counter()
                parser_seconds = 0.0
                dedup_seconds = 0.0
                file_records = 0
                iterator = iter(_iter_asset_records(list_path))
                while True:
                    parser_start = time.perf_counter()
                    try:
                        source_path, line_no, raw_type, value, fmt = next(iterator)
                    except StopIteration:
                        parser_seconds += time.perf_counter() - parser_start
                        break
                    parser_seconds += time.perf_counter() - parser_start
                    file_records += 1
                    service_raw_records += 1
                    dedup_start = time.perf_counter()
                    asset_type = _asset_type(raw_type, value)
                    asset = LegacyAsset(
                        service=service_id,
                        category=category_dir.name.lower(),
                        service_type=service_type,
                        parent=parent,
                        asset_type=asset_type,
                        value=value,
                        generated_file=source_path.name,
                        path=str(source_path.as_posix()),
                        line=line_no,
                        detected_format=fmt,
                        sources=sources,
                    )
                    key = asset.identity()
                    evidence = {
                        "generated_file": source_path.name,
                        "path": str(source_path.as_posix()),
                        "line": line_no,
                        "detected_format": fmt,
                        "sources": list(sources),
                    }
                    current = seen.get(key)
                    if current is None:
                        seen[key] = AssetEvidence(asset=asset, evidence=[evidence])
                    else:
                        current.occurrences += 1
                        if evidence not in current.evidence:
                            current.evidence.append(evidence)
                    dedup_seconds += time.perf_counter() - dedup_start
                _profile_file(profile, {
                    "service": service_id,
                    "path": str(list_path.as_posix()),
                    "records": file_records,
                    "parser_seconds": round(parser_seconds, 6),
                    "dedup_seconds": round(dedup_seconds, 6),
                    "total_seconds": round(time.perf_counter() - file_start, 6),
                })
            service_seconds = time.perf_counter() - service_start
            services_profile[service_id] = {
                "metadata_seconds": round(metadata_seconds, 6),
                "asset_seconds": round(max(service_seconds - metadata_seconds, 0.0), 6),
                "total_seconds": round(service_seconds, 6),
                "files": service_file_count,
                "raw_records": service_raw_records,
                "unique_records": len(seen),
            }
            for evidence in seen.values():
                yield evidence


def extract_legacy_asset_ir(
    rule_root: Path,
    *,
    index_path: Path | None = None,
    include_aggregates: bool = True,
) -> LegacyAssetIR:
    """Build the service-level IR manifest without embedding every asset value."""
    rule_root = Path(rule_root)
    index_path = Path(index_path) if index_path else rule_root / "_index.yaml"
    index = _index_records(index_path)
    summaries: dict[str, ServiceAssetSummary] = {}
    profile: dict[str, Any] = {"services": {}, "files": [], "totals": {}}

    for (category, service_id), item in sorted(index.items()):
        if not include_aggregates and item["service_type"] == "aggregate":
            continue
        directory = rule_root / category / str(item["name"])
        if item.get("path"):
            path_parts = Path(str(item["path"])).parts
            if len(path_parts) >= 3:
                directory = rule_root / path_parts[-2] / path_parts[-1]
        metadata = _metadata_for(directory)
        children = [str(v).strip().lower() for v in (metadata.get("children") or []) if str(v).strip()]
        categories = [str(v).strip().lower() for v in (metadata.get("categories") or []) if str(v).strip()]
        if not categories:
            categories = [category]
        summaries[service_id] = ServiceAssetSummary(
            id=service_id,
            name=str(metadata.get("name") or item.get("name") or service_id),
            category=category,
            categories=categories,
            service_type=str(metadata.get("service_type") or item.get("service_type") or "service"),
            parent=(str(metadata.get("parent")).strip().lower() if metadata.get("parent") else None),
            children=children,
            metadata_present=bool(metadata),
            index_present=True,
            index_domains=item.get("domains"),
            index_ips=item.get("ips"),
            metadata_statistics=dict(metadata.get("statistics") or {}),
            generated_files=dict(metadata.get("generated_files") or {}),
            sources=[str(v).strip() for v in (metadata.get("sources") or []) if str(v).strip()],
        )

    for category_dir in sorted(p for p in rule_root.iterdir() if p.is_dir()):
        for directory in sorted(p for p in category_dir.iterdir() if p.is_dir()):
            metadata = _metadata_for(directory)
            service_id = str(metadata.get("id") or directory.name).strip().lower()
            if not service_id or service_id in summaries:
                continue
            service_type = str(metadata.get("service_type") or "service").strip().lower()
            if not include_aggregates and service_type == "aggregate":
                continue
            summaries[service_id] = ServiceAssetSummary(
                id=service_id,
                name=str(metadata.get("name") or directory.name),
                category=category_dir.name.lower(),
                categories=[str(v).strip().lower() for v in (metadata.get("categories") or [category_dir.name])],
                service_type=service_type,
                parent=(str(metadata.get("parent")).strip().lower() if metadata.get("parent") else None),
                children=[str(v).strip().lower() for v in (metadata.get("children") or []) if str(v).strip()],
                metadata_present=True,
                index_present=False,
                metadata_statistics=dict(metadata.get("statistics") or {}),
                generated_files=dict(metadata.get("generated_files") or {}),
                sources=[str(v).strip() for v in (metadata.get("sources") or []) if str(v).strip()],
                errors=["metadata-only: service is absent from rule/_index.yaml"],
            )

    for evidence in iter_service_assets(rule_root, include_aggregates=include_aggregates, profile=profile):
        summary = summaries.get(evidence.asset.service)
        if summary is None:
            continue
        summary.records += 1
        _update_counts(summary, evidence.asset.asset_type)
        if evidence.asset.path not in summary.source_files:
            summary.source_files.append(evidence.asset.path)
        for source in evidence.asset.sources:
            if source not in summary.sources:
                summary.sources.append(source)

    relation_drift: list[dict[str, Any]] = []
    index_service_ids = {service_id for (_category, service_id) in index}
    for summary in summaries.values():
        if summary.service_type != "aggregate":
            continue
        metadata_children = set(summary.children)
        indexed_children = {
            child.id
            for child in summaries.values()
            if child.id in index_service_ids and child.parent == summary.id
        }
        missing = sorted(metadata_children - indexed_children)
        metadata_only = sorted(metadata_children - index_service_ids)
        index_only = sorted(indexed_children - metadata_children)
        if missing or metadata_only or index_only:
            relation_drift.append({
                "aggregate": summary.id,
                "category": summary.category,
                "metadata_children": sorted(metadata_children),
                "indexed_children": sorted(indexed_children),
                "metadata_only": metadata_only,
                "index_only": index_only,
                "missing_from_index": missing,
                "status": "drift",
            })

    totals = {
        "records": sum(s.records for s in summaries.values()),
        "domains": sum(s.domains for s in summaries.values()),
        "domain_suffixes": sum(s.domain_suffixes for s in summaries.values()),
        "domain_keywords": sum(s.domain_keywords for s in summaries.values()),
        "domain_regexes": sum(s.domain_regexes for s in summaries.values()),
        "cidrs": sum(s.cidrs for s in summaries.values()),
        "urls": sum(s.urls for s in summaries.values()),
        "hosts": sum(s.hosts for s in summaries.values()),
        "process_rules": sum(s.process_rules for s in summaries.values()),
    }
    profile["totals"]["services"] = len(summaries)
    profile["totals"]["metadata_only_services"] = sum(1 for s in summaries.values() if not s.index_present)
    profile["totals"]["total_seconds"] = round(sum(v["total_seconds"] for v in profile["services"].values()), 6)
    return LegacyAssetIR(
        schema="legacy_asset_ir_v1",
        generated_at=datetime.now(timezone.utc).isoformat(),
        source={
            "rule_root": str(rule_root),
            "index": str(index_path),
            "description": "legacy evidence only; not canonical V1 source of truth",
        },
        services=sorted(summaries.values(), key=lambda item: item.id),
        totals=totals,
        relation_drift=relation_drift,
        profile=profile,
    )


def write_asset_jsonl(rule_root: Path, output: Path, *, include_aggregates: bool = True) -> dict[str, Any]:
    """Write the complete de-duplicated asset stream and return file metadata."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    records = 0
    with output.open("w", encoding="utf-8") as handle:
        for evidence in iter_service_assets(rule_root, include_aggregates=include_aggregates):
            handle.write(json.dumps(evidence.as_dict(), ensure_ascii=False, sort_keys=True) + "\n")
            records += 1
    return {"records": records, "sha256": _sha256(output), "path": str(output)}


__all__ = [
    "AssetEvidence",
    "LegacyAsset",
    "LegacyAssetIR",
    "ServiceAssetSummary",
    "extract_legacy_asset_ir",
    "iter_service_assets",
    "write_asset_jsonl",
]
