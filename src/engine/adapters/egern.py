"""Native Egern adapter — render the official Egern Rule Set schema."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.engine.adapters.registry import CLIENTS

CLIENT = "egern"
EXT = CLIENTS[CLIENT]["ext"]
FMT = CLIENTS[CLIENT]["format"]

# Canonical IR rule types -> Egern Rule Set collection fields.
TYPE_TO_FIELD = {
    "DOMAIN": "domain_set",
    "DOMAIN-SUFFIX": "domain_suffix_set",
    "DOMAIN-KEYWORD": "domain_keyword_set",
    "DOMAIN-REGEX": "domain_regex_set",
    "DOMAIN-WILDCARD": "domain_wildcard_set",
    "GEOIP": "geoip_set",
    "IP-CIDR": "ip_cidr_set",
    "IP-CIDR6": "ip_cidr6_set",
    "URL-REGEX": "url_regex_set",
    "USER-AGENT": "user_agent_set",
    "SSID": "ssid_set",
    "BSSID": "bssid_set",
    "CELLULAR": "cellular_set",
    "PROTOCOL": "protocol_set",
    "DEST-PORT": "dest_port_set",
    "ASN": "asn_set",
}


def _native_field(rule_type: str) -> str:
    key = str(rule_type).strip().upper().replace("_", "-")
    try:
        return TYPE_TO_FIELD[key]
    except KeyError as exc:
        raise ValueError(f"Unsupported Egern rule type: {rule_type!r}") from exc


def render(rules: list[dict[str, Any]], out_path: Path) -> Path:
    """Render canonical rules as an Egern Rule Set YAML document.

    Egern Rule Sets are collections such as ``domain_suffix_set`` rather than
    Clash/Surge-style ``payload`` lines.  Keep each native collection distinct
    so the generated artifact can be consumed directly by Egern's ``rule_set``.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if FMT != "yaml":
        raise ValueError(f"Egern adapter registry format must be yaml, got {FMT!r}")

    grouped: dict[str, list[str]] = defaultdict(list)
    for rule in rules:
        if not isinstance(rule, dict):
            raise TypeError(f"Egern adapter received non-object rule: {rule!r}")
        if "type" not in rule or "value" not in rule:
            raise ValueError(f"Egern adapter received incomplete rule: {rule!r}")
        field = _native_field(str(rule["type"]))
        value = str(rule["value"]).strip()
        if not value:
            raise ValueError(f"Egern adapter received empty rule value: {rule!r}")
        grouped[field].append(value)

    # JSON string literals are valid YAML double-quoted scalars and safely
    # preserve regexes, punctuation, Unicode, and backslashes.
    lines: list[str] = []
    for field in TYPE_TO_FIELD.values():
        values = grouped.get(field)
        if not values:
            continue
        lines.append(f"{field}:")
        lines.extend(f"  - {json.dumps(value, ensure_ascii=False)}" for value in values)

    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return out_path
