#!/usr/bin/env python3
"""Verify every client artifact preserves the Semantic IR rule set."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

TYPE_FIELDS = {
    "domain": "domain",
    "domain_suffix": "domain_suffix",
    "domain_keyword": "domain_keyword",
    "domain_regex": "domain_regex",
    "ip_cidr": "ip_cidr",
    "ip_cidr6": "ip_cidr6",
}

EGERN_FIELDS = {
    "domain_set": "domain",
    "domain_suffix_set": "domain_suffix",
    "domain_keyword_set": "domain_keyword",
    "domain_regex_set": "domain_regex",
    "ip_cidr_set": "ip_cidr",
    "ip_cidr6_set": "ip_cidr6",
}

LINE_TYPES = {
    "DOMAIN": "domain",
    "DOMAIN-SUFFIX": "domain_suffix",
    "DOMAIN-KEYWORD": "domain_keyword",
    "DOMAIN-REGEX": "domain_regex",
    "HOST": "domain",
    "HOST-SUFFIX": "domain_suffix",
    "HOST-KEYWORD": "domain_keyword",
    "IP-CIDR": "ip_cidr",
    "IP-CIDR6": "ip_cidr6",
    "IP6-CIDR": "ip_cidr6",
}

EXAMPLE_LIMIT = 20


def _norm_type(value: str) -> str:
    return value.strip().lower().replace("-", "_")


def _load_ir(path: Path) -> list[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = data.get("rules") or []
    return [(_norm_type(str(r.get("type", ""))), str(r.get("value", ""))) for r in rules]


def _project_ir_rules(path: Path) -> set[tuple[str, str]]:
    return {
        (_norm_type(str(r.get("type", ""))), str(r.get("value", "")))
        for r in (json.loads(path.read_text(encoding="utf-8")).get("rules") or [])
    }


def _strip_policy(value: str) -> str:
    value = value.strip()
    # Native line-list clients append a routing policy after the rule value.
    value = re.sub(r",\s*(REJECT|DIRECT|PROXY|PASS|REJECT-DROP)\s*$", "", value, flags=re.I)
    return value.strip()


def _extract_json(path: Path) -> set[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    found: set[tuple[str, str]] = set()
    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, values in node.items():
                typ = TYPE_FIELDS.get(_norm_type(str(key)))
                if typ and isinstance(values, list):
                    for item in values:
                        if isinstance(item, str) and item.strip():
                            found.add((typ, item.strip()))
                walk(values)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    walk(data)
    return found


def _extract_egern_yaml(path: Path) -> set[tuple[str, str]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    found: set[tuple[str, str]] = set()
    if not isinstance(data, dict):
        return found
    for key, values in data.items():
        typ = EGERN_FIELDS.get(str(key))
        if not typ or not isinstance(values, list):
            continue
        for item in values:
            val = str(item).strip()
            if val:
                found.add((typ, val))
    return found


def _extract_lines(path: Path) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        line = line[1:].strip() if line.startswith("-") else line
        line = line.strip("\"'")
        if not line or line.startswith("#") or "," not in line:
            continue
        head, rest = line.split(",", 1)
        typ = LINE_TYPES.get(head.strip().upper().replace("_", "-"))
        if not typ:
            continue
        value = _strip_policy(rest.strip().strip("\"'"))
        if value:
            found.add((typ, value))
    return found


def _extract_yaml(path: Path) -> set[tuple[str, str]]:
    """YAML may be Clash payload or native Egern collections."""
    egern = _extract_egern_yaml(path)
    if egern:
        return egern
    return _extract_lines(path)


def _extract_client(client_dir: Path, artifact: str) -> set[tuple[str, str]]:
    pattern = {"json": "*.json", "yaml": "*.yaml", "list": "*.list"}[artifact]
    files = sorted(p for p in client_dir.rglob(pattern) if p.is_file())
    if not files:
        raise RuntimeError(f"no {artifact} artifacts in {client_dir}")
    found: set[tuple[str, str]] = set()
    for path in files:
        if artifact == "json":
            found |= _extract_json(path)
        elif artifact == "yaml":
            found |= _extract_yaml(path)
        else:
            found |= _extract_lines(path)
    return found


def _clip(items: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return items[:EXAMPLE_LIMIT]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ir", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, default=Path("config/client_capability_matrix.yaml"))
    args = parser.parse_args()

    ir_rules = _project_ir_rules(args.ir)
    matrix = yaml.safe_load(args.matrix.read_text(encoding="utf-8")) or {}
    clients = matrix.get("clients") or {}
    failures: list[dict[str, Any]] = []
    passed: list[str] = []

    for client, cfg in sorted(clients.items()):
        capability = {_norm_type(str(x)) for x in cfg.get("native_rule_types", [])}
        if client == "singbox":
            expected = {
                ("ip_cidr" if typ == "ip_cidr6" else typ, value)
                for typ, value in ir_rules
                if typ in capability
            }
        else:
            expected = {(typ, value) for typ, value in ir_rules if typ in capability}
        actual = _extract_client(args.generated / client, str(cfg["artifact"]))
        normalized_ir = {
            ("ip_cidr" if typ == "ip_cidr6" else typ, value)
            for typ, value in ir_rules
        } if client == "singbox" else ir_rules
        missing = sorted(expected - actual)
        unexpected = sorted(actual - normalized_ir)
        if missing or unexpected:
            failures.append({
                "client": client,
                "missing_count": len(missing),
                "unexpected_count": len(unexpected),
                "missing": _clip(missing),
                "unexpected": _clip(unexpected),
            })
        else:
            passed.append(client)

    report = {"schema": "cross_client_semantic_v1", "pass": not failures, "passed": passed, "failures": failures}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not failures else 1
