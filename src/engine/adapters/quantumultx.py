"""Native Quantumult X adapter.

Quantumult X uses lowercase host/ip filter syntax. Policy binding is loaded
from config/client_policy.yaml instead of being hard-coded in the adapter.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.engine.adapters.registry import CLIENTS
from src.engine.adapters.type_normalize import normalize_rule_for_client

CLIENT = "quantumultx"
EXT = CLIENTS[CLIENT]["ext"]
FMT = CLIENTS[CLIENT]["format"]
ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = ROOT / "config" / "client_policy.yaml"

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


def _policy() -> str:
    try:
        data = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
        policy = str((data.get("clients") or {}).get(CLIENT, {}).get("default_rule_policy") or "proxy").strip()
    except (OSError, yaml.YAMLError, AttributeError):
        policy = "proxy"
    if not policy:
        raise ValueError("Quantumult X policy binding is empty")
    return policy


def render(rules: list[dict[str, Any]], out_path: Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if FMT != "list":
        raise ValueError(f"Quantumult X adapter registry format must be list, got {FMT!r}")
    policy = _policy()
    lines: list[str] = []
    for rule in (normalize_rule_for_client(r) for r in rules):
        if not isinstance(rule, dict) or "type" not in rule or "value" not in rule:
            raise ValueError(f"Quantumult X adapter received incomplete rule: {rule!r}")
        value = str(rule["value"]).strip()
        if not value:
            raise ValueError(f"Quantumult X adapter received empty rule value: {rule!r}")
        lines.append(f"{_native_prefix(str(rule['type']))}, {value}, {policy}")
    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return out_path
