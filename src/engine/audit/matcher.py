"""Deterministic matcher used by executable semantic/overlap audits.

The matcher consumes canonical normalized rule records and deliberately uses
boundary-aware suffix matching. It is kept small and side-effect free so audit
results are reproducible in CI and can be reused by later production stages.
"""
from __future__ import annotations

from typing import Any


def _norm_host(value: str) -> str:
    return value.strip().lower().rstrip(".")


def _suffix_match(host: str, suffix: str) -> bool:
    host = _norm_host(host)
    suffix = _norm_host(suffix)
    return host == suffix or host.endswith("." + suffix)


def rule_matches(rule: dict[str, Any], host: str) -> bool:
    """Return whether a normalized canonical rule matches a hostname."""
    typ = str(rule.get("type") or "").strip().lower().replace("_", "-")
    value = str(rule.get("value") or "").strip()
    host = _norm_host(host)
    if not typ or not value or not host:
        return False
    if typ in {"host", "domain"}:
        return host == _norm_host(value)
    if typ in {"host-suffix", "domain-suffix"}:
        return _suffix_match(host, value)
    if typ in {"host-keyword", "domain-keyword"}:
        return _norm_host(value) in host
    return False


def matching_rules(rules: list[dict[str, Any]], host: str) -> list[dict[str, Any]]:
    """Return all rules matching *host*, preserving canonical rule order."""
    return [rule for rule in rules if rule_matches(rule, host)]
