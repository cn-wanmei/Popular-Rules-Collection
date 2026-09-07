"""Native Quantumult X adapter — emit native filter rule syntax."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from src.engine.adapters.base import normalize_type
from src.engine.adapters.registry import CLIENTS

CLIENT = "quantumultx"
EXT = CLIENTS[CLIENT]["ext"]
FMT = CLIENTS[CLIENT]["format"]

TYPE_TO_PREFIX = {
    "DOMAIN": "host",
    "DOMAIN-SUFFIX": "host-suffix",
    "DOMAIN-KEYWORD": "host-keyword",
    "DOMAIN-REGEX": "host-regex",
    "DOMAIN-WILDCARD": "host-wildcard",
    "IP-CIDR": "ip-cidr",
    "IP-CIDR6": "ip6-cidr",
    "URL-REGEX": "url-regex",
}


def _line(rule: dict[str, Any]) -> str:
    typ = normalize_type(rule["type"])
    try:
        prefix = TYPE_TO_PREFIX[typ]
    except KeyError as exc:
        raise ValueError(f"Unsupported Quantumult X rule type: {rule['type']!r}") from exc
    value = str(rule["value"]).strip()
    if not value:
        raise ValueError(f"Empty Quantumult X rule value: {rule!r}")
    return f"{prefix},{value}"


def render(rules: list[dict[str, Any]], out_path: Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if FMT != "list":
        raise ValueError(f"Quantumult X adapter registry format must be list, got {FMT!r}")
    out_path.write_text(
        "\n".join(_line(rule) for rule in rules) + "\n",
        encoding="utf-8",
    )
    return out_path
