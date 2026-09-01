"""V3 input normalizer replacing the retired 2.X normalize stage."""
from __future__ import annotations

from typing import Any


def normalize_record(service: str, rule_type: str, value: str, *, category: str = "other", provenance: dict[str, Any] | None = None) -> dict[str, Any]:
    service = service.strip().lower()
    rule_type = rule_type.strip().lower()
    value = value.strip().rstrip(".") if rule_type.startswith("domain") else value.strip()
    if not service or not rule_type or not value:
        raise ValueError("service, type and value are required")
    return {"service": service, "type": rule_type, "value": value, "category": category.strip().lower() or "other", "provenance": provenance or {}}
