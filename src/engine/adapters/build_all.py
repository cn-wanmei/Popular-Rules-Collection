"""Parallel native client projections from the Semantic IR contract."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import yaml

from src.engine.adapters.registry import CLIENTS, get_adapter
from src.engine.adapters.type_normalize import normalize_rule_for_client
from src.engine.distribution.path_resolver import EntityPathResolver
from src.engine.semantic_intent import validate_semantic_probes

_ROOT = Path(__file__).resolve().parents[3]
_CAPABILITY_MATRIX = _ROOT / "config" / "client_capability_matrix.yaml"
_DIRECTORY_POLICY = _ROOT / "config" / "service_model" / "directories.yaml"
_HIERARCHY = _ROOT / "config" / "ruleset_hierarchy.yaml"


def _load_ir(ir_dir: Path) -> tuple[list[dict[str, Any]], dict[str, list[str]], dict[str, Any], dict[str, Any], str]:
    ir_path = Path(ir_dir) / "ir.json"
    if not ir_path.exists():
        raise RuntimeError(f"Semantic IR missing: {ir_path}")
    data = json.loads(ir_path.read_text(encoding="utf-8"))
    if data.get("schema") != "semantic_ir_v2":
        raise RuntimeError(f"Unsupported semantic IR schema: {data.get('schema')}")
    if data.get("v2_runtime_dependency") != 0:
        raise RuntimeError("Semantic IR reports V2 runtime dependency")
    rules = data.get("rules")
    ir_manifest_path = Path(ir_dir) / "manifest.json"
    ir_manifest = json.loads(ir_manifest_path.read_text(encoding="utf-8")) if ir_manifest_path.is_file() else {}
    ir_digest = str(ir_manifest.get("ir_digest") or "").strip()
    if not ir_digest:
        raise RuntimeError("Semantic IR manifest is missing ir_digest")
    memberships = data.get("memberships")
    entities = data.get("entities")
    semantic_intent = data.get("semantic_intent") or {}
    if not isinstance(rules, list) or not isinstance(memberships, dict) or not isinstance(entities, dict):
        raise RuntimeError("Semantic IR contract is incomplete")
    if not isinstance(semantic_intent, dict):
        raise RuntimeError("Semantic IR semantic_intent report is invalid")
    return rules, {str(k): [str(x) for x in v] for k, v in memberships.items()}, entities, semantic_intent, ir_digest


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid mapping: {path}")
    return data


def _load_directory_contract() -> tuple[dict[str, str], dict[str, set[str]], dict[str, str], set[str]]:
    if not _DIRECTORY_POLICY.exists():
        raise RuntimeError(f"Directory policy missing: {_DIRECTORY_POLICY}")
    policy = _load_yaml(_DIRECTORY_POLICY)
    if policy.get("schema") != "rule_distribution_policy_v2":
        raise RuntimeError("Unsupported rule distribution policy schema")
    layout = policy.get("layout") or {}
    for key, expected in EntityPathResolver.GENERATED_LAYOUT.items():
        if str(layout.get(key) or "").strip() != expected:
            raise RuntimeError(f"Directory policy layout mismatch: {key} must be {expected}")
    hierarchy = _load_yaml(_HIERARCHY)
    providers = hierarchy.get("providers") or {}
    service_provider: dict[str, str] = {}
    provider_services: dict[str, set[str]] = {}
    provider_aggregates: dict[str, str] = {}
    for provider, node in providers.items():
        if not isinstance(node, dict):
            continue
        provider_id = str(provider).strip().casefold()
        aggregate = str(node.get("aggregate") or provider_id).strip()
        provider_aggregates[provider_id] = aggregate
        service_ids = {str(sid).strip().casefold() for sid in (node.get("services") or {})}
        provider_services[provider_id] = service_ids
        for sid in service_ids:
            if sid in service_provider and service_provider[sid] != provider_id:
                raise RuntimeError(f"Service {sid!r} belongs to multiple providers")
            service_provider[sid] = provider_id
    china = policy.get("china") or {}
    china_exclusions = {str(x).strip().casefold() for x in china.get("exclude_independent_providers") or [] if str(x).strip()}
    return service_provider, provider_services, provider_aggregates, china_exclusions

def _load_capabilities() -> dict[str, set[str]]:
    if not _CAPABILITY_MATRIX.exists():
        raise RuntimeError(f"Client capability matrix missing: {_CAPABILITY_MATRIX}")
    data = yaml.safe_load(_CAPABILITY_MATRIX.read_text(encoding="utf-8")) or {}
    clients = data.get("clients")
    if not isinstance(clients, dict):
        raise RuntimeError("Client capability matrix is missing clients")
    capabilities: dict[str, set[str]] = {}
    for client in CLIENTS:
        meta = clients.get(client)
        if not isinstance(meta, dict) or not isinstance(meta.get("native_rule_types"), list):
            raise RuntimeError(f"Client capability matrix is incomplete for {client}")
        capabilities[client] = {str(t).strip().lower().replace("-", "_") for t in meta["native_rule_types"]}
    return capabilities


def _rule_type_key(rule: dict[str, Any]) -> str:
    raw = str(rule.get("type", "")).strip().upper().replace("_", "-")
    return raw.lower().replace("-", "_")


def _project_rules(client: str, rules: list[dict[str, Any]], capabilities: dict[str, set[str]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    supported = capabilities[client]
    projected: list[dict[str, Any]] = []
    skipped: Counter[str] = Counter()
    for rule in rules:
        normalized = normalize_rule_for_client(rule)
        key = _rule_type_key(normalized)
        if key in supported:
            projected.append(normalized)
        else:
            skipped[key or "unknown"] += 1
    return projected, dict(sorted(skipped.items()))


def _render_view(render, rules: list[dict[str, Any]], path: Path) -> None:
    if not rules:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    render(rules, path)
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"Adapter produced missing or empty artifact: {path}")


def _build_client(
    client: str, meta: dict[str, str], rules: list[dict[str, Any]], memberships: dict[str, list[str]], artifacts_dir: Path,
    capabilities: dict[str, set[str]], service_provider: dict[str, str], provider_services: dict[str, set[str]],
    provider_aggregates: dict[str, str], china_exclusions: set[str],
) -> tuple[str, dict[str, Any]]:
    cdir = artifacts_dir / client
    cdir.mkdir(parents=True, exist_ok=True)
    render = get_adapter(client)
    rules_by_id = {r["id"]: r for r in rules}
    projected_rules, skipped_types = _project_rules(client, rules, capabilities)
    projected_ids = {r["id"] for r in projected_rules}
    emitted_files = 0
    emitted_paths: list[str] = []

    for provider in sorted(provider_services):
        aggregate = provider_aggregates[provider]
        provider_ids: set[str] = set(memberships.get(aggregate, []))
        for service in sorted(provider_services[provider]):
            provider_ids.update(memberships.get(service, []))
        entity_rules = [rules_by_id[rid] for rid in sorted(provider_ids) if rid in rules_by_id and rid in projected_ids]
        if entity_rules:
            path = artifacts_dir / EntityPathResolver.generated_provider(client, provider).relative_to("generated")
            collision_path = artifacts_dir / EntityPathResolver.generated_service(client, provider, provider).relative_to("generated")
            if path == collision_path:
                continue
            path = path.with_name(path.name + meta["ext"])
            _render_view(render, entity_rules, path)
            emitted_files += 1
            emitted_paths.append(path.relative_to(cdir).as_posix())

    for service, provider in sorted(service_provider.items()):
        entity_rules = [rules_by_id[rid] for rid in memberships.get(service, []) if rid in rules_by_id and rid in projected_ids]
        if entity_rules:
            path = artifacts_dir / EntityPathResolver.generated_service(client, provider, service).relative_to("generated")
            path = path.with_name(path.name + meta["ext"])
            _render_view(render, entity_rules, path)
            emitted_files += 1
            emitted_paths.append(path.relative_to(cdir).as_posix())

    china_ids: set[str] = set(memberships.get("china", []))
    excluded_ids: set[str] = set()
    for provider in china_exclusions:
        if provider not in provider_services:
            continue
        excluded_ids.update(memberships.get(provider_aggregates[provider], []))
        for service in provider_services[provider]:
            excluded_ids.update(memberships.get(service, []))
    china_ids.difference_update(excluded_ids)
    china_rules = [rules_by_id[rid] for rid in sorted(china_ids) if rid in rules_by_id and rid in projected_ids]
    if china_rules:
        path = artifacts_dir / EntityPathResolver.generated_china(client).relative_to("generated")
        path = path.with_name(path.name + meta["ext"])
        _render_view(render, china_rules, path)
        emitted_files += 1
        emitted_paths.append(path.relative_to(cdir).as_posix())

    # Categories are semantic cross-provider views. Prefer canonical rule
    # classification; retain synthetic membership fallback for test fixtures.
    category_rules: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for rule in projected_rules:
        classification = rule.get("classification") or {}
        category = str(classification.get("category") or "").strip()
        if category:
            category_rules[category][rule["id"]] = rule
    for entity in sorted(memberships):
        if entity in provider_aggregates.values() or entity in service_provider or entity == "china" or entity.endswith("_aggregate"):
            continue
        for rid in memberships[entity]:
            rule = rules_by_id.get(rid)
            if rule is not None and rid in projected_ids:
                category_rules[entity].setdefault(rid, rule)
    for category, by_id in sorted(category_rules.items()):
        entity_rules = [by_id[rid] for rid in sorted(by_id)]
        path = artifacts_dir / EntityPathResolver.generated_category(client, category).relative_to("generated")
        path = path.with_name(path.name + meta["ext"])
        _render_view(render, entity_rules, path)
        emitted_files += 1
        emitted_paths.append(path.relative_to(cdir).as_posix())

    files = sorted(p for p in cdir.rglob(f"*{meta['ext']}") if p.is_file())
    if not files or any(p.stat().st_size == 0 for p in files):
        raise RuntimeError(f"Adapter {client} produced missing or empty artifacts")
    return client, {"ext": meta["ext"], "files": emitted_files, "source": "semantic_ir_v2", "directory_schema": EntityPathResolver.LAYOUT_SCHEMA, "input_rules": len(rules), "emitted_rules": len(projected_rules), "skipped_unsupported_rule_types": skipped_types, "paths": emitted_paths}


def build_all_clients(ir_dir: Path, artifacts_dir: Path, *, views: list[str] | None = None, run_id: str | None = None) -> dict[str, Any]:
    """Build all client artifacts from IR using the canonical directory contract."""
    artifacts_dir = Path(artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    rules, memberships, entities, semantic_intent, ir_digest = _load_ir(Path(ir_dir))
    probe_report = validate_semantic_probes(rules, memberships)
    capabilities = _load_capabilities()
    service_provider, provider_services, provider_aggregates, china_exclusions = _load_directory_contract()
    report: dict[str, Any] = {"schema": "adapter_build_v5", "clients": {}, "views": {"services": sorted(entities.get("services", [])), "aggregate": True, "china": True}, "source_contract": "semantic_ir_v2", "directory_contract": EntityPathResolver.LAYOUT_SCHEMA, "resolver": "EntityPathResolver", "run_id": str(run_id or "").strip() or None, "ir_digest": ir_digest, "china_excluded_independent_providers": sorted(china_exclusions), "semantic_intent": semantic_intent, "semantic_probes": probe_report, "v2_runtime_dependency": 0, "parallel": True}
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(CLIENTS))), thread_name_prefix="adapter") as pool:
        futures = {pool.submit(_build_client, client, meta, rules, memberships, artifacts_dir, capabilities, service_provider, provider_services, provider_aggregates, china_exclusions, ): client for client, meta in CLIENTS.items()}
        for future in as_completed(futures):
            client, details = future.result()
            report["clients"][client] = details
    report["clients"] = {k: report["clients"][k] for k in sorted(report["clients"])}
    (artifacts_dir / "build_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
