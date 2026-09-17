"""V3 input normalizer replacing the retired 2.X normalize stage."""
from __future__ import annotations

from typing import Any

# IR / adapter use both underscore and hyphen forms.
_SUFFIX_TYPES = {"domain_suffix", "domain-suffix"}
_KEYWORD_TYPES = {"domain_keyword", "domain-keyword"}
_DOMAIN_EXACT = {"domain"}


def _looks_like_fqdn(value: str) -> bool:
    """True when value has a dot and is not a pure glob keyword."""
    if "." not in value:
        return False
    if value.startswith("*"):
        return False
    return True


def normalize_domain_rule_type(rule_type: str, value: str) -> tuple[str, str]:
    """Enforce suffix vs keyword semantics before IR / adapters.

    - Bare labels (no '.') MUST NOT be domain_suffix → become domain_keyword.
    - FQDN-looking values MUST NOT stay as domain_keyword → become domain_suffix.
    """
    t = rule_type.strip().lower().replace("_", "-")
    v = value.strip()
    if t in {"domain-suffix", "domain_suffix"} or t == "domain-suffix":
        t_norm = "domain_suffix"
    elif t in {"domain-keyword", "domain_keyword"} or t == "domain-keyword":
        t_norm = "domain_keyword"
    elif t == "domain":
        t_norm = "domain"
    else:
        # preserve non-domain types as lowercase underscore-ish from caller
        return rule_type.strip().lower(), v

    if t_norm == "domain_suffix":
        v = v.rstrip(".")
        if "." not in v:
            return "domain_keyword", v
        return "domain_suffix", v

    if t_norm == "domain_keyword":
        v = v.rstrip(".")
        if _looks_like_fqdn(v):
            return "domain_suffix", v
        return "domain_keyword", v

    if t_norm == "domain":
        return "domain", v.rstrip(".")

    return rule_type.strip().lower(), v


def normalize_record(
    service: str,
    rule_type: str,
    value: str,
    *,
    category: str = "other",
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    service = service.strip().lower()
    rule_type = rule_type.strip().lower()
    if rule_type.startswith("domain") or rule_type.replace("_", "-").startswith("domain"):
        rule_type, value = normalize_domain_rule_type(rule_type, value)
        value = value.strip().rstrip(".") if rule_type.startswith("domain") else value.strip()
    else:
        value = value.strip()
    if not service or not rule_type or not value:
        raise ValueError("service, type and value are required")
    return {
        "service": service,
        "type": rule_type,
        "value": value,
        "category": category.strip().lower() or "other",
        "provenance": provenance or {},
    }
