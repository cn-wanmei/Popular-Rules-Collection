"""Native sing-box adapter — preserve IR rule semantics in source JSON."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.engine.adapters.registry import CLIENTS

CLIENT = "singbox"
EXT = CLIENTS[CLIENT]["ext"]
FMT = CLIENTS[CLIENT]["format"]

TYPE_TO_FIELD = {
    "DOMAIN": "domain",
    "DOMAIN-SUFFIX": "domain_suffix",
    "DOMAIN-KEYWORD": "domain_keyword",
    "DOMAIN-REGEX": "domain_regex",
    "IP-CIDR": "ip_cidr",
    "IP-CIDR6": "ip_cidr",
}


def _native_field(rule_type: str) -> str:
    key = str(rule_type).strip().upper().replace("_", "-")
    try:
        return TYPE_TO_FIELD[key]
    except KeyError as exc:
        raise ValueError(f"Unsupported sing-box rule type: {rule_type!r}") from exc


def render(rules: list[dict[str, Any]], out_path: Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if FMT != "json":
        raise ValueError(f"singbox adapter registry format must be json, got {FMT!r}")

    grouped: dict[str, list[str]] = defaultdict(list)
    for rule in rules:
        if not isinstance(rule, dict) or "type" not in rule or "value" not in rule:
            raise ValueError(f"sing-box adapter received invalid rule: {rule!r}")
        field = _native_field(str(rule["type"]))
        value = str(rule["value"]).strip()
        if not value:
            raise ValueError(f"sing-box adapter received empty rule value: {rule!r}")
        grouped[field].append(value)

    headless_rule = {field: values for field, values in grouped.items() if values}
    payload = {
        "version": 5,
        "rules": [headless_rule] if headless_rule else [],
    }
    out_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out_path
