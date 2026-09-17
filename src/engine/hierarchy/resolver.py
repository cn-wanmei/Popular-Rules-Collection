"""Explicit Provider → Aggregate → Service hierarchy resolver.

The resolver is declaration-driven. Provider ownership is unique, while category
membership may intentionally overlap providers (for example AWS belongs to Amazon
and the Developer ecosystem).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from src.engine.canonical.store import load_memberships, load_rules

DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "config" / "ruleset_hierarchy.yaml"


class HierarchyConfigError(ValueError):
    """Invalid explicit provider/service hierarchy configuration."""


def load_hierarchy_config(config_path: Path | None = None) -> dict[str, Any]:
    path = Path(config_path or DEFAULT_CONFIG)
    if not path.exists():
        raise HierarchyConfigError(f"Hierarchy config does not exist: {path}")
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - parser-specific error text
        raise HierarchyConfigError(f"Failed to parse hierarchy config {path}: {exc}") from exc
    if not isinstance(doc, dict) or doc.get("schema") != "provider_service_hierarchy_v1":
        raise HierarchyConfigError("Unsupported hierarchy config schema")
    if not isinstance(doc.get("providers"), dict):
        raise HierarchyConfigError("Hierarchy config requires providers mapping")
    if "categories" in doc and not isinstance(doc.get("categories"), dict):
        raise HierarchyConfigError("Hierarchy config categories must be a mapping")
    return doc


def validate_hierarchy_config(config: dict[str, Any]) -> None:
    _validate_config(config)


def _validate_config(
    config: dict[str, Any],
) -> tuple[dict[str, str], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    providers = config["providers"]
    categories = config.get("categories") or {}
    service_to_provider: dict[str, str] = {}
    aggregate_to_provider: dict[str, str] = {}
    metadata: dict[str, dict[str, Any]] = {}
    category_metadata: dict[str, dict[str, Any]] = {}

    for provider_id, provider in providers.items():
        if not isinstance(provider, dict):
            raise HierarchyConfigError(f"Provider {provider_id!r} must be a mapping")
        aggregate = str(provider.get("aggregate") or provider_id)
        if aggregate in aggregate_to_provider:
            raise HierarchyConfigError(
                f"Aggregate {aggregate!r} is owned by multiple providers: "
                f"{aggregate_to_provider[aggregate]!r}, {provider_id!r}"
            )
        aggregate_to_provider[aggregate] = provider_id
        metadata[aggregate] = {
            "id": aggregate,
            "type": "aggregate",
            "provider": provider_id,
            "display_name": provider.get("display_name", provider_id),
            "services": [],
        }
        for service_id, service in (provider.get("services") or {}).items():
            if not isinstance(service, dict):
                raise HierarchyConfigError(
                    f"Service {service_id!r} under provider {provider_id!r} must be a mapping"
                )
            if service_id in service_to_provider and service_to_provider[service_id] != provider_id:
                raise HierarchyConfigError(
                    f"Service {service_id!r} is declared under multiple providers: "
                    f"{service_to_provider[service_id]!r}, {provider_id!r}"
                )
            if service_id == aggregate:
                raise HierarchyConfigError(
                    f"Service {service_id!r} cannot equal aggregate {aggregate!r}"
                )
            if service_id in aggregate_to_provider:
                raise HierarchyConfigError(
                    f"Service {service_id!r} collides with provider aggregate "
                    f"owned by {aggregate_to_provider[service_id]!r}"
                )
            service_to_provider[service_id] = provider_id
            metadata[service_id] = {
                "id": service_id,
                "type": "service",
                "provider": provider_id,
                "parent": aggregate,
                "display_name": service.get("display_name", service_id),
                "status": service.get("status", "planned"),
            }
            metadata[aggregate]["services"].append(service_id)

    for category_id, category in categories.items():
        if not isinstance(category, dict):
            raise HierarchyConfigError(f"Category {category_id!r} must be a mapping")
        aggregate = str(category.get("aggregate") or category_id)
        if aggregate != category_id:
            raise HierarchyConfigError(
                f"Category {category_id!r} aggregate must equal category id; got {aggregate!r}"
            )
        if aggregate in metadata:
            raise HierarchyConfigError(
                f"Category aggregate {aggregate!r} collides with provider hierarchy node"
            )
        service_ids: list[str] = []
        for service_id, service in (category.get("services") or {}).items():
            if not isinstance(service, dict):
                raise HierarchyConfigError(
                    f"Category service {service_id!r} under {category_id!r} must be a mapping"
                )
            service_ids.append(service_id)
        category_metadata[aggregate] = {
            "id": aggregate,
            "type": "category_aggregate",
            "category": category_id,
            "display_name": category.get("display_name", category_id),
            "services": service_ids,
        }

    return service_to_provider, metadata, category_metadata


def build_hierarchy(
    canonical_dir: Path,
    out_dir: Path,
    config_path: Path | None = None,
) -> dict[str, Any]:
    canonical_dir = Path(canonical_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    memberships = load_memberships(canonical_dir)
    load_rules(canonical_dir)
    config = load_hierarchy_config(config_path)
    service_to_provider, metadata, category_metadata = _validate_config(config)

    services: dict[str, dict[str, Any]] = {}
    aggregates: dict[str, dict[str, Any]] = {}
    categories: dict[str, dict[str, Any]] = {}

    for node_id, node in metadata.items():
        if node["type"] == "service":
            rids = list(memberships.get(node_id, []))
            services[node_id] = {**node, "rule_ids": rids, "rule_count": len(rids)}
        else:
            aggregates[node_id] = {**node, "rule_ids": [], "rule_count": 0}

    for node_id, node in category_metadata.items():
        categories[node_id] = {**node, "rule_ids": [], "rule_count": 0}

    for entity, rids in memberships.items():
        if entity in services or entity in aggregates or entity in categories:
            continue
        services[entity] = {
            "id": entity,
            "type": "service",
            "rule_ids": list(rids),
            "rule_count": len(rids),
            "provider": None,
            "status": "unmodeled",
        }

    for provider_id, provider in config["providers"].items():
        aggregate_id = str(provider["aggregate"])
        child_ids = list((provider.get("services") or {}).keys())
        rule_ids: set[str] = set(memberships.get(aggregate_id, []))
        for child_id in child_ids:
            rule_ids.update(memberships.get(child_id, []))
        aggregates[aggregate_id]["rule_ids"] = sorted(rule_ids)
        aggregates[aggregate_id]["rule_count"] = len(rule_ids)
        aggregates[aggregate_id]["services"] = child_ids

    for category_id, category in (config.get("categories") or {}).items():
        aggregate_id = str(category["aggregate"])
        child_ids = list((category.get("services") or {}).keys())
        rule_ids: set[str] = set(memberships.get(aggregate_id, []))
        for child_id in child_ids:
            rule_ids.update(memberships.get(child_id, []))
        categories[aggregate_id]["rule_ids"] = sorted(rule_ids)
        categories[aggregate_id]["rule_count"] = len(rule_ids)
        categories[aggregate_id]["services"] = child_ids

    groups: dict[str, dict[str, Any]] = {}
    graph = {
        "schema": "provider_service_hierarchy_v2",
        "config_schema": config.get("schema"),
        "rules": config.get("rules", {}),
        "services": services,
        "groups": groups,
        "aggregates": aggregates,
        "categories": categories,
        "unmodeled_services": sorted(
            entity for entity, node in services.items() if node.get("status") == "unmodeled"
        ),
    }

    (out_dir / "graph.json").write_text(
        json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (out_dir / "services.jsonl").open("w", encoding="utf-8") as f:
        for service in services.values():
            f.write(json.dumps(service, ensure_ascii=False) + "\n")
    with (out_dir / "groups.jsonl").open("w", encoding="utf-8") as f:
        for group in groups.values():
            f.write(json.dumps(group, ensure_ascii=False) + "\n")
    with (out_dir / "aggregates.jsonl").open("w", encoding="utf-8") as f:
        for aggregate in aggregates.values():
            f.write(json.dumps(aggregate, ensure_ascii=False) + "\n")
    with (out_dir / "categories.jsonl").open("w", encoding="utf-8") as f:
        for category in categories.values():
            f.write(json.dumps(category, ensure_ascii=False) + "\n")

    configured_service_count = len(service_to_provider)
    materialized_service_count = sum(1 for service in services.values() if service.get("rule_count", 0) > 0)
    manifest = {
        "schema": "hierarchy_manifest_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "service_count": len(services),
        "group_count": 0,
        "aggregate_count": len(aggregates),
        "category_count": len(categories),
        "configured_service_count": configured_service_count,
        "materialized_service_count": materialized_service_count,
        "unmodeled_service_count": len(graph["unmodeled_services"]),
        "v2_runtime_dependency": 0,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest


def load_hierarchy(out_dir: Path) -> dict[str, Any]:
    path = Path(out_dir) / "graph.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
