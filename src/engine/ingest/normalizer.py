"""V3 input normalizer replacing the retired 2.X normalize stage."""
from __future__ import annotations

from typing import Any


def normalize_domain_rule_type(rule_type: str, value: str) -> tuple[str, str]:
    """Enforce suffix vs keyword semantics before IR / adapters.

    - Bare labels (no '.') MUST NOT be domain_suffix unless they look like a
      public suffix / TLD (e.g. ``cn``, ``com``) — those stay domain_suffix.
    - Brand-like bare labels (alibaba, google, …) become domain_keyword.
    - domain_keyword values with dots are left as keyword (CDN / partial
      patterns such as ``dualstack.apiproxy-`` must not become suffix).
    """
    t = rule_type.strip().lower().replace("_", "-")
    v = value.strip()
    if t in {"domain-suffix", "domain_suffix"}:
        t_norm = "domain_suffix"
    elif t in {"domain-keyword", "domain_keyword"}:
        t_norm = "domain_keyword"
    elif t == "domain":
        t_norm = "domain"
    else:
        return rule_type.strip().lower(), v

    if t_norm == "domain_suffix":
        v = v.rstrip(".")
        if "." not in v:
            # Keep short alphabetic public-suffix style labels as suffix.
            if len(v) <= 3 and v.isalpha():
                return "domain_suffix", v
            return "domain_keyword", v
        return "domain_suffix", v

    if t_norm == "domain_keyword":
        # Do not promote keyword→suffix; partial/CDN keywords often contain dots.
        return "domain_keyword", v.rstrip(".")

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
