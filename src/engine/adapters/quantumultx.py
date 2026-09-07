"""Native Quantumult X adapter.

Quantumult X uses its own lowercase filter syntax (host/host-suffix/etc.),
not the DOMAIN-* syntax used by Surge/Shadowrocket/Loon.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from src.engine.adapters.registry import CLIENTS

CLIENT = "quantumultx"
EXT = CLIENTS[CLIENT]["ext"]
FMT = CLIENTS[CLIENT]["format"]

TYPE_TO_PREFIX = {
    "DOMAIN": "host",
    "DOMAIN-SUFFIX": "host-suffix",
    "DOMAIN-KEYWORD": "host-keyword",
    "IP-CIDR": "ip-cidr",
    "IP-CIDR6": "ip6-cidr",
}


def _native_prefix(rule_type: str) -> str:
    key = str(rule_type).strip().upper().replace("_", "-")
    try:
        return TYPE_TO_PREFIX[key]
    except KeyError as exc:
        raise ValueError(f"Unsupported Quantumult X rule type: {rule_type!r}") from exc


def render(rules: list[dict[str, Any]], out_path: Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if FMT != "list":
        raise ValueError(f"Quantumult X adapter registry format must be list, got {FMT!r}")

    lines: list[str] = []
    for rule in rules:
        if not isinstance(rule, dict) or "type" not in rule or "value" not in rule:
            raise ValueError(f"Quantumult X adapter received incomplete rule: {rule!r}")
        value = str(rule["value"]).strip()
        if not value:
            raise ValueError(f"Quantumult X adapter received empty rule value: {rule!r}")
        lines.append(f"{_native_prefix(str(rule['type']))}, {value}, proxy")

    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return out_path
