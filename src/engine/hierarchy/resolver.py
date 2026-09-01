"""View Resolver — DAG expand + union from Canonical Store."""
from __future__ import annotations

from src.engine.core.hashing import sha256_lines
from src.engine.core.models.entity import EntityGraph

MAX_DEPTH = 16


def expand_members(graph: EntityGraph, member_ids: list[str], exclude: list[str] | None = None) -> list[str]:
    exclude_set = set(exclude or [])
    expanded: list[str] = []
    seen: set[str] = set()

    def walk(node: str, depth: int) -> None:
        if node in seen or depth > MAX_DEPTH:
            return
        seen.add(node)
        if node in graph.groups:
            for child in graph.groups[node].members:
                walk(child, depth + 1)
        elif node not in expanded:
            expanded.append(node)

    for m in member_ids:
        walk(m, 0)
    return [m for m in expanded if m not in exclude_set]


def body_service_id(graph: EntityGraph, service_id: str) -> str:
    s = graph.services.get(service_id)
    if s and s.body_service_id:
        return s.body_service_id
    if service_id.endswith("-core"):
        return service_id[: -len("-core")]
    return service_id


def resolve_aggregate(graph: EntityGraph, view_id: str, memberships: dict[str, list[str]], rules: dict[str, dict]) -> dict:
    agg = graph.aggregates.get(view_id)
    if not agg:
        raise KeyError(f"unknown aggregate: {view_id}")
    members = expand_members(graph, agg.members, agg.exclude)
    rule_ids: set[str] = set()
    per_member: dict[str, int] = {}
    for mid in members:
        body = body_service_id(graph, mid)
        rids = memberships.get(body) or memberships.get(mid) or []
        per_member[mid] = len(rids)
        rule_ids.update(rids)
    ordered = sorted(rule_ids)
    resolved_rules = [rules[rid] for rid in ordered if rid in rules]
    keys = [r.get("identity_key") or f"{r.get('type')}|{r.get('value')}" for r in resolved_rules]
    return {
        "view": view_id,
        "mode": "aggregate",
        "members": members,
        "per_member_rule_rows": per_member,
        "rule_count": len(resolved_rules),
        "sha256": sha256_lines(keys),
        "rules": resolved_rules,
    }
