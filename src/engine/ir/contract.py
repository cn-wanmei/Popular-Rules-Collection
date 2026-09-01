"""Semantic IR contract validation and deterministic identity.

The contract is intentionally dependency-free so every producer/consumer can
validate the same artifact before it crosses a stage boundary.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

SCHEMA = "semantic_ir_v2"
CONTRACT_VERSION = "2.0"
_REQUIRED_TYPES = {
    "schema": str,
    "generated_at": str,
    "engine_version": str,
    "v2_runtime_dependency": int,
    "entities": dict,
    "views": dict,
    "memberships": dict,
    "rules": list,
    "decisions": list,
    "stats": dict,
}


class IRContractError(ValueError):
    """Raised when a semantic IR artifact violates the published contract."""


def validate_ir(ir: dict[str, Any], *, allow_legacy_aliases: bool = True) -> None:
    if not isinstance(ir, dict):
        raise IRContractError("IR must be an object")
    missing = [name for name in _REQUIRED_TYPES if name not in ir]
    if missing:
        raise IRContractError(f"missing required fields: {', '.join(missing)}")
    if ir["schema"] != SCHEMA:
        raise IRContractError(f"unsupported schema: {ir['schema']!r}")
    for name, expected in _REQUIRED_TYPES.items():
        value = ir[name]
        if not isinstance(value, expected) or (name == "v2_runtime_dependency" and isinstance(value, bool)):
            raise IRContractError(f"invalid type for {name}: expected {expected.__name__}")
    if ir["v2_runtime_dependency"] != 0:
        raise IRContractError("v2_runtime_dependency must remain 0")
    if set(ir["entities"]) != {"services", "groups", "aggregates"}:
        raise IRContractError("entities must contain services, groups, aggregates")
    for name, values in ir["entities"].items():
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise IRContractError(f"entities.{name} must be a string list")
    if not allow_legacy_aliases and ("entity" in ir or "view" in ir):
        raise IRContractError("legacy IR aliases are forbidden")
    for index, rule in enumerate(ir["rules"]):
        if not isinstance(rule, dict):
            raise IRContractError(f"rules[{index}] must be an object")
        for field in ("id", "type", "value", "identity_key", "classification", "provenance"):
            if field not in rule:
                raise IRContractError(f"rules[{index}] missing {field}")
        if not all(isinstance(rule[field], str) for field in ("id", "type", "value", "identity_key")):
            raise IRContractError(f"rules[{index}] has invalid scalar types")
        if not isinstance(rule["classification"], (dict, type(None))) or not isinstance(rule["provenance"], (dict, type(None))):
            raise IRContractError(f"rules[{index}] metadata must be objects or null")


def canonical_ir_bytes(ir: dict[str, Any]) -> bytes:
    """Return the stable semantic representation; volatile generated_at is excluded."""
    validate_ir(ir)
    stable = {k: v for k, v in ir.items() if k not in {"generated_at", "entity", "view"}}
    return json.dumps(stable, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def ir_digest(ir: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_ir_bytes(ir)).hexdigest()
