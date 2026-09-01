"""Decision Engine — SSOT (no substring heuristics, no svcs[0]).

Decision = f(rule, view, policy_profile, precedence)
"""
from __future__ import annotations

from typing import Any


# Explicit policy profile (can later be loaded from config)
DEFAULT_PROFILE = {
    "adblock": "REJECT",
    "china": "DIRECT",
    "domestic": "DIRECT",
    "mail": "PROXY",
    "storage": "PROXY",
    "search": "PROXY",
    "default": "PROXY",
}

# Exact category / service overrides (never substring)
EXACT_DIRECT = {"china", "domestic", "cn", "lan", "private"}
EXACT_REJECT = {"adblock", "ads", "reject"}


def decide(
    rule: dict[str, Any],
    *,
    view: str | None = None,
    entity: str | None = None,
    category: str | None = None,
    profile: dict[str, str] | None = None,
) -> str:
    """
    Return action: PROXY | DIRECT | REJECT
    Deterministic. No membership order dependency.
    """
    profile = profile or DEFAULT_PROFILE
    cat = (category or rule.get("classification", {}).get("category") or "").lower()
    ent = (entity or "").lower()

    if cat in EXACT_REJECT or ent in EXACT_REJECT:
        return "REJECT"
    if cat in EXACT_DIRECT or ent in EXACT_DIRECT:
        return "DIRECT"
    if cat in profile:
        return profile[cat]
    return profile.get("default", "PROXY")


def decide_batch(
    rules: list[dict[str, Any]],
    memberships: dict[str, list[str]],
    *,
    profile: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """
    Attach decision to every rule under every entity it belongs to.
    One rule can have different decisions under different views/entities
    only if policy differs; currently same rule → same decision (deterministic).
    """
    rid_to_entities: dict[str, list[str]] = {}
    for ent, rids in memberships.items():
        for rid in rids:
            rid_to_entities.setdefault(rid, []).append(ent)

    out = []
    for rule in rules:
        rid = rule["id"]
        entities = rid_to_entities.get(rid, [])
        # Decision is based on rule classification, not on arbitrary first entity
        action = decide(rule, profile=profile)
        out.append({
            "rule_id": rid,
            "type": rule.get("type"),
            "value": rule.get("value"),
            "action": action,
            "entities": entities,
            "category": rule.get("classification", {}).get("category"),
        })
    return out
