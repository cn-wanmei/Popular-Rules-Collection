"""Canonical Rule model — identity & hashing (no V2 dependency)."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any


def identity_key(typ: str, value: str) -> str:
    """Stable identity for a rule (type + normalized value)."""
    return f"{typ.strip().lower()}|{value.strip().lower()}"


def full_rule_id(typ: str, value: str) -> str:
    """Full SHA-256 hex (256-bit) — no silent truncation to 64-bit."""
    return hashlib.sha256(identity_key(typ, value).encode("utf-8")).hexdigest()


@dataclass
class Rule:
    id: str
    type: str
    value: str
    identity_key: str
    provenance: dict[str, Any] = field(default_factory=dict)
    classification: dict[str, Any] = field(default_factory=dict)
    memberships: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "value": self.value,
            "identity_key": self.identity_key,
            "provenance": self.provenance,
            "classification": self.classification,
            "memberships": self.memberships,
        }
