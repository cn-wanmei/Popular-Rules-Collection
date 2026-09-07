"""Parallel native client projections from the Semantic IR contract."""
from __future__ import annotations

import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import yaml

from src.engine.adapters.registry import CLIENTS, get_adapter


_CAPABILITY_MATRIX = Path(__file__).resolve().parents[3] / "config" / "client_capability_matrix.yaml"


def _load_ir(ir_dir: Path) -> tuple[list[dict[str, Any]], dict[str, list[str]], dict[str, Any]]:
    ir_path = Path(ir_dir) / "ir.json"
    if not ir_path.exists():
        raise RuntimeError(f"Semantic IR missing: {ir_path}")
    data = json.loads(ir_path.read_text(encoding="utf-8"))
    if data.get("schema") != "semantic_ir_v2":
        raise RuntimeError(f"Unsupported semantic IR schema: {data.get('schema')}")
    if data.get("v2_runtime_dependency") != 0:
        raise RuntimeError("Semantic IR reports V2 runtime dependency")
    rules = data.get("rules")
    memberships = data.get("memberships")
    entities = data.get("entities")
    if not isinstance(rules, list) or not isinstance(memberships, dict) or not isinstance(entities, dict):
        raise RuntimeError("Semantic IR contract is incomplete")
    return rules, {str(k): [str(x) for x in v] for k, v in memberships.items()}, entities


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


def _project_rules(
    client: str, rules: list[dict[str, Any]], capabilities: dict[str, set[str]]
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    supported = capabilities[client]
    projected: list[dict[str, Any]] = []
    skipped: Counter[str] = Counter()
    for rule in rules:
        key = _rule_type_key(rule)
        if key in supported:
            projected.append(rule)
        else:
            skipped[key or "unknown"] += 1
    return projected, dict(sorted(skipped.items()))


def _build_client(
    client: str,
    meta: dict[str, str],
    rules: list[dict[str, Any]],
    memberships: dict[str, list[str]],
    artifacts_dir: Path,
    capabilities: dict[str, set[str]],
) -> tuple[str, dict[str, Any]]:
    cdir = artifacts_dir / client
    cdir.mkdir(parents=True, exist_ok=True)
    render = get_adapter(client)
    rules_by_id = {r["id"]: r for r in rules}
    projected_rules, skipped_types = _project_rules(client, rules, capabilities)
    projected_ids = {r["id"] for r in projected_rules}

    render(projected_rules, cdir / f"aggregate{meta['ext']}")
    for entity in sorted(memberships):
        entity_rules = [
            rules_by_id[rid]
            for rid in memberships[entity]
            if rid in projected_ids and rid in rules_by_id
        ]
        if entity_rules:
            render(entity_rules, cdir / f"{entity}{meta['ext']}")
    files = sorted(cdir.glob(f"*{meta['ext']}"))
    if not files or any(p.stat().st_size == 0 for p in files):
        raise RuntimeError(f"Adapter {client} produced missing or empty artifacts")
    return client, {
        "ext": meta["ext"],
        "files": len(files),
        "source": "semantic_ir_v2",
        "input_rules": len(rules),
        "emitted_rules": len(projected_rules),
        "skipped_unsupported_rule_types": skipped_types,
    }


def build_all_clients(ir_dir: Path, artifacts_dir: Path, *, views: list[str] | None = None) -> dict[str, Any]:
    """Build all client artifacts from IR, projecting only each client's native capabilities."""
    artifacts_dir = Path(artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    rules, memberships, entities = _load_ir(Path(ir_dir))
    capabilities = _load_capabilities()
    report: dict[str, Any] = {
        "schema": "adapter_build_v2",
        "clients": {},
        "views": {"services": sorted(entities.get("services", [])), "aggregate": True},
        "source_contract": "semantic_ir_v2",
        "v2_runtime_dependency": 0,
        "parallel": True,
    }
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(CLIENTS))), thread_name_prefix="adapter") as pool:
        futures = {
            pool.submit(_build_client, client, meta, rules, memberships, artifacts_dir, capabilities): client
            for client, meta in CLIENTS.items()
        }
        for future in as_completed(futures):
            client, details = future.result()
            report["clients"][client] = details
    report["clients"] = {k: report["clients"][k] for k in sorted(report["clients"])}
    (artifacts_dir / "build_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report
