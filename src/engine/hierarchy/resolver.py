"""Hierarchy Resolver — produces Service / Group / Aggregate views (P0-7/8).

Output:
  hierarchy/
    graph.json          # full DAG-ish structure
    services.jsonl      # per-service rule membership
    groups.jsonl
    aggregates.jsonl
    manifest.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.canonical.store import load_rules, load_memberships


def build_hierarchy(canonical_dir: Path, out_dir: Path) -> dict[str, Any]:
    canonical_dir = Path(canonical_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rules = load_rules(canonical_dir)
    memberships = load_memberships(canonical_dir)  # entity → [rule_id]

    # Simple hierarchy inference:
    # - every entity is a Service
    # - entities sharing a common prefix become a Group (e.g. google-*)
    # - top-level provider becomes Aggregate
    services: dict[str, dict] = {}
    groups: dict[str, dict] = {}
    aggregates: dict[str, dict] = {}

    for entity, rids in memberships.items():
        services[entity] = {
            "id": entity,
            "type": "service",
            "rule_ids": rids,
            "rule_count": len(rids),
        }
        # derive group / aggregate from naming convention
        if "-" in entity:
            prefix = entity.split("-")[0]
            groups.setdefault(prefix, {"id": prefix, "type": "group", "services": [], "rule_ids": set()})
            groups[prefix]["services"].append(entity)
            groups[prefix]["rule_ids"].update(rids)
            aggregates.setdefault(prefix, {"id": prefix, "type": "aggregate", "groups": set(), "rule_ids": set()})
            aggregates[prefix]["groups"].add(prefix)
            aggregates[prefix]["rule_ids"].update(rids)
        else:
            aggregates.setdefault(entity, {"id": entity, "type": "aggregate", "groups": set(), "rule_ids": set()})
            aggregates[entity]["rule_ids"].update(rids)

    # serialize sets
    for g in groups.values():
        g["rule_ids"] = sorted(g["rule_ids"])
        g["service_count"] = len(g["services"])
    for a in aggregates.values():
        a["groups"] = sorted(a["groups"])
        a["rule_ids"] = sorted(a["rule_ids"])
        a["rule_count"] = len(a["rule_ids"])

    graph = {
        "schema": "hierarchy_v1",
        "services": services,
        "groups": groups,
        "aggregates": aggregates,
    }

    (out_dir / "graph.json").write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with (out_dir / "services.jsonl").open("w", encoding="utf-8") as f:
        for s in services.values():
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with (out_dir / "groups.jsonl").open("w", encoding="utf-8") as f:
        for g in groups.values():
            f.write(json.dumps(g, ensure_ascii=False) + "\n")
    with (out_dir / "aggregates.jsonl").open("w", encoding="utf-8") as f:
        for a in aggregates.values():
            f.write(json.dumps(a, ensure_ascii=False) + "\n")

    manifest = {
        "schema": "hierarchy_manifest_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "service_count": len(services),
        "group_count": len(groups),
        "aggregate_count": len(aggregates),
        "v2_runtime_dependency": 0,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def load_hierarchy(out_dir: Path) -> dict[str, Any]:
    path = Path(out_dir) / "graph.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
