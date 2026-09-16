"""Auditable semantic-intent overrides and behavioral probes.

The canonical store preserves source semantics verbatim.  This module is the
explicit policy layer between canonical rules and the semantic IR.  Policies
are source/service/value scoped so the engine never guesses that a rule type
should change merely because a value has or lacks a dot.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

DEFAULT_POLICY_PATH = Path(__file__).resolve().parents[2] / "config" / "semantic_intent.yaml"


class SemanticIntentError(ValueError):
    """Raised when semantic-intent policy is invalid or contradictory."""


def _source_ids(rule: dict[str, Any]) -> set[str]:
    provenance = rule.get("provenance") or {}
    raw_sources = provenance.get("sources") or []
    out: set[str] = set()
    for source in raw_sources:
        if isinstance(source, dict):
            value = source.get("id") or source.get("name")
        else:
            value = source
        if value:
            out.add(str(value))
    return out


def _normalize_rule_type(value: Any) -> str:
    return str(value).strip().upper().replace("_", "-")


def _load_policy(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SemanticIntentError(f"semantic-intent policy missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SemanticIntentError("semantic-intent policy must be a mapping")
    if data.get("version") != 1:
        raise SemanticIntentError("unsupported semantic-intent policy version")
    policies = data.get("policies")
    if not isinstance(policies, list):
        raise SemanticIntentError("semantic-intent policy must contain policies")
    return data


def _policy_matches(policy: dict[str, Any], rule: dict[str, Any], service_names: set[str]) -> bool:
    services = {str(x) for x in policy.get("services") or []}
    if services and not services.intersection(service_names):
        return False

    source_ids = {str(x) for x in policy.get("source_ids") or []}
    if source_ids and not source_ids.intersection(_source_ids(rule)):
        return False

    match = policy.get("match") or {}
    if not isinstance(match, dict):
        raise SemanticIntentError(f"policy {policy.get('id')!r} has invalid match")
    types = {_normalize_rule_type(x) for x in match.get("types") or []}
    if types and _normalize_rule_type(rule.get("type")) not in types:
        return False
    values = {str(x) for x in match.get("values") or []}
    if values and str(rule.get("value")) not in values:
        return False
    return True


def _transformation_marker(policy: dict[str, Any], old_type: str, new_type: str, value: str) -> dict[str, Any]:
    return {
        "policy_id": str(policy["id"]),
        "action": "convert_type",
        "from_type": old_type,
        "to_type": new_type,
        "value": value,
        "reason": str(policy.get("reason") or "explicit semantic intent override"),
    }


def apply_semantic_intent(
    rules: list[dict[str, Any]],
    memberships: dict[str, list[str]],
    *,
    policy_path: Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Apply explicit semantic policies and return transformed rules + audit report."""
    path = Path(policy_path or DEFAULT_POLICY_PATH)
    data = _load_policy(path)
    policies = data["policies"]
    rules_out = [deepcopy(r) for r in rules]
    reverse_memberships: dict[str, set[str]] = {}
    for service, ids in memberships.items():
        for rule_id in ids:
            reverse_memberships.setdefault(str(rule_id), set()).add(str(service))

    applied: list[dict[str, Any]] = []
    applied_policy_by_rule: dict[str, str] = {}

    for policy in policies:
        if not isinstance(policy, dict) or not policy.get("id"):
            raise SemanticIntentError("every semantic-intent policy needs an id")
        action = policy.get("action")
        if not isinstance(action, dict) or _normalize_rule_type(action.get("type")) == "":
            raise SemanticIntentError(f"policy {policy['id']!r} must define action.type")
        target_type = _normalize_rule_type(action["type"])

        for rule in rules_out:
            if not _policy_matches(policy, rule, reverse_memberships.get(str(rule["id"]), set())):
                continue
            rule_id = str(rule["id"])
            previous_policy = applied_policy_by_rule.get(rule_id)
            if previous_policy and previous_policy != str(policy["id"]):
                existing_type = _normalize_rule_type(rule["type"])
                if existing_type != target_type:
                    raise SemanticIntentError(
                        f"conflicting semantic-intent policies for rule {rule_id}: "
                        f"{previous_policy!r} vs {policy['id']!r}"
                    )
                continue

            old_type = _normalize_rule_type(rule["type"])
            if old_type == target_type:
                continue
            value = str(rule["value"])
            rule["type"] = target_type
            provenance = rule.setdefault("provenance", {})
            transformations = provenance.setdefault("semantic_transformations", [])
            transformations.append(_transformation_marker(policy, old_type, target_type, value))
            applied_policy_by_rule[rule_id] = str(policy["id"])
            applied.append({
                "policy_id": str(policy["id"]),
                "rule_id": rule_id,
                "service_memberships": sorted(reverse_memberships.get(rule_id, set())),
                "from_type": old_type,
                "to_type": target_type,
                "value": value,
            })

    report = {
        "schema": "semantic_intent_v1",
        "policy_file": str(path),
        "policy_version": data["version"],
        "policies": [str(p["id"]) for p in policies],
        "applied": applied,
        "applied_count": len(applied),
    }
    return rules_out, report


def _matches_host(rule_type: str, value: str, host: str) -> bool:
    typ = _normalize_rule_type(rule_type)
    normalized_host = host.strip().lower().rstrip(".")
    normalized_value = value.strip().lower().rstrip(".")
    if typ == "DOMAIN":
        return normalized_host == normalized_value
    if typ == "DOMAIN-SUFFIX":
        return normalized_host == normalized_value or normalized_host.endswith("." + normalized_value)
    if typ == "DOMAIN-KEYWORD":
        return normalized_value in normalized_host
    raise SemanticIntentError(f"unsupported probe rule type: {rule_type!r}")


def validate_semantic_probes(
    rules: list[dict[str, Any]],
    memberships: dict[str, list[str]],
    *,
    policy_path: Path | None = None,
) -> dict[str, Any]:
    """Run configured behavioral probes against the post-policy semantic IR."""
    path = Path(policy_path or DEFAULT_POLICY_PATH)
    data = _load_policy(path)
    rules_by_id = {str(r["id"]): r for r in rules}
    results: list[dict[str, Any]] = []

    for policy in data["policies"]:
        probes = policy.get("probes") or {}
        if not probes:
            continue
        services = {str(x) for x in policy.get("services") or []}
        if services and not services.intersection(str(name) for name in memberships):
            continue
        target_ids = set()
        for service in services:
            target_ids.update(str(rid) for rid in memberships.get(service, []))
        target_rules = [rules_by_id[rid] for rid in sorted(target_ids) if rid in rules_by_id]
        policy_id = str(policy["id"])
        scoped_rules = []
        for rule in target_rules:
            markers = ((rule.get("provenance") or {}).get("semantic_transformations") or [])
            if any(str(m.get("policy_id")) == policy_id for m in markers if isinstance(m, dict)):
                scoped_rules.append(rule)

        for host in [str(x) for x in probes.get("matches") or []]:
            matched = any(_matches_host(str(r["type"]), str(r["value"]), host) for r in scoped_rules)
            results.append({"policy_id": policy_id, "host": host, "expected": True, "matched": matched})
            if not matched:
                raise SemanticIntentError(f"semantic probe failed: {policy_id} should match {host}")
        for host in [str(x) for x in probes.get("non_matches") or []]:
            matched = any(_matches_host(str(r["type"]), str(r["value"]), host) for r in scoped_rules)
            results.append({"policy_id": policy_id, "host": host, "expected": False, "matched": matched})
            if matched:
                raise SemanticIntentError(f"semantic probe failed: {policy_id} should not match {host}")

    return {
        "schema": "semantic_probe_v1",
        "policy_file": str(path),
        "probes": results,
        "probe_count": len(results),
    }
