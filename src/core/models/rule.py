"""Canonical rule identity — type-aware normalization."""
from __future__ import annotations

from dataclasses import dataclass


def normalize_value(typ: str, value: str) -> str:
    v = (value or "").strip()
    t = (typ or "").lower()
    if t in ("domain", "domain_suffix", "domain_keyword"):
        return v.lower().rstrip(".")
    if t in ("ip_cidr", "ip_cidr6"):
        return v.lower()
    if t in ("domain_regex",):
        return v
    return v.lower().rstrip(".") if v else v


def identity_key(typ: str, value: str) -> str:
    return f"{typ}|{normalize_value(typ, value)}"


@dataclass(frozen=True)
class RuleIdentity:
    type: str
    value: str

    @property
    def key(self) -> str:
        return identity_key(self.type, self.value)
