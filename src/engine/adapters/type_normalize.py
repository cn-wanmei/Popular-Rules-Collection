"""Adapter-level defense: correct bare DOMAIN-SUFFIX before emit."""
from __future__ import annotations

from typing import Any

from src.engine.ingest.normalizer import normalize_domain_rule_type


def normalize_rule_for_client(rule: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(rule, dict) or "type" not in rule or "value" not in rule:
        return rule
    raw_type = str(rule["type"])
    raw_value = str(rule["value"])
    # Map to IR-ish then back to adapter upper form
    ir_type, value = normalize_domain_rule_type(raw_type, raw_value)
    # non-domain types pass through
    if not ir_type.startswith("domain"):
        out = dict(rule)
        out["type"] = raw_type.strip().upper().replace("_", "-")
        out["value"] = raw_value.strip()
        return out
    # domain family → Clash-style upper for list adapters
    mapping = {
        "domain": "DOMAIN",
        "domain_suffix": "DOMAIN-SUFFIX",
        "domain_keyword": "DOMAIN-KEYWORD",
    }
    out = dict(rule)
    out["type"] = mapping.get(ir_type, raw_type.strip().upper().replace("_", "-"))
    out["value"] = value
    return out
