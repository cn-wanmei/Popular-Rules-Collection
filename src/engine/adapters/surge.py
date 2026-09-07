"""Native Surge rule-set adapter."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from src.engine.adapters.registry import CLIENTS

CLIENT = "surge"
EXT = CLIENTS[CLIENT]["ext"]
FMT = CLIENTS[CLIENT]["format"]
SUPPORTED = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6"}


def render(rules: list[dict[str, Any]], out_path: Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if FMT != "list":
        raise ValueError(f"Surge adapter registry format must be list, got {FMT!r}")

    lines: list[str] = []
    for rule in rules:
        if not isinstance(rule, dict) or "type" not in rule or "value" not in rule:
            raise ValueError(f"Surge adapter received incomplete rule: {rule!r}")
        rule_type = str(rule["type"]).strip().upper().replace("_", "-")
        if rule_type not in SUPPORTED:
            raise ValueError(f"Unsupported Surge rule type: {rule_type!r}")
        value = str(rule["value"]).strip()
        if not value:
            raise ValueError(f"Surge adapter received empty rule value: {rule!r}")
        lines.append(f"{rule_type},{value}")

    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return out_path
