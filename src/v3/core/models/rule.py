"""V3 Canonical Rule model."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

def normalize_value(typ: str, value: str) -> str:
    v = (value or "").strip()
    t = (typ or "").lower()
    if t in ("domain", "domain_suffix", "domain_keyword"):
        return v.lower().rstrip(".")
    if t in ("ip_cidr", "ip_cidr6"):
        return v.lower()
    if t == "domain_regex":
        return v
    return v.lower().rstrip(".") if v else v

def identity_key(typ: str, value: str) -> str:
    return f"{(typ or '').lower()}|{normalize_value(typ, value)}"

@dataclass(frozen=True)
class RuleIdentity:
    type: str
    value: str
    @property
    def key(self) -> str:
        return identity_key(self.type, self.value)

@dataclass
class CanonicalRule:
    id: str
    identity: RuleIdentity
    provenance: dict[str, Any] = field(default_factory=dict)
    classification: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.identity.type, "value": self.identity.value,
                "identity_key": self.identity.key, "provenance": self.provenance,
                "classification": self.classification}
