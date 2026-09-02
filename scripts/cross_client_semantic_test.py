#!/usr/bin/env python3
"""Verify every client artifact preserves the Semantic IR rule set."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import yaml

TYPE_FIELDS = {
    "domain": "domain",
    "domain_suffix": "domain_suffix",
    "domain_keyword": "domain_keyword",
    "domain_regex": "domain_regex",
    "ip_cidr": "ip_cidr",
    "ip_cidr6": "ip_cidr",
}
LINE_TYPES = {
    "DOMAIN": "domain",
    "DOMAIN-SUFFIX": "domain_suffix",
    "DOMAIN-KEYWORD": "domain_keyword",
    "DOMAIN-REGEX": "domain_regex",
    "IP-CIDR": "ip_cidr",
    "IP-CIDR6": "ip_cidr6",
}


def _norm_type(value: str) -> str:
    return value.strip().lower().replace("-", "_")


def _load_ir(path: Path) -> set[tuple[str, str]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema") != "semantic_ir_v2":
        raise RuntimeError("unsupported IR schema")
    return {(_norm_type(str(r["type"])), str(r["value"]).strip()) for r in obj.get("rules", [])}


def _extract_json(path: Path) -> set[tuple[str, str]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    found: set[tuple[str, str]] = set()

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in TYPE_FIELDS and isinstance(value, list):
                    found.update((TYPE_FIELDS[key], str(item).strip()) for item in value)
                visit(value)
        elif isinstance(node, list):
            for item in node:
                visit(item)

    visit(obj)
    return found


def _extract_lines(path: Path) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip().strip('"\'')
        if not line or line.startswith("#") or "," not in line:
            continue
        head, rest = line.split(",", 1)
        typ = LINE_TYPES.get(head.strip().upper())
        if not typ:
            continue
        value = rest.split(",", 1)[0].strip().strip('"\'')
        if value:
            found.add((typ, value))
    return found


def _extract_client(client_dir: Path, artifact: str) -> set[tuple[str, str]]:
    pattern = {"json": "*.json", "yaml": "*.yaml", "list": "*.list"}[artifact]
    files = sorted(client_dir.glob(pattern))
    if not files:
        raise RuntimeError(f"no {artifact} artifacts in {client_dir}")
    found: set[tuple[str, str]] = set()
    for path in files:
        found |= _extract_json(path) if artifact == "json" else _extract_lines(path)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ir", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, default=Path("config/client_capability_matrix.yaml"))
    args = parser.parse_args()

    ir_rules = _load_ir(args.ir)
    matrix = yaml.safe_load(args.matrix.read_text(encoding="utf-8")) or {}
    clients = matrix.get("clients") or {}
    failures: list[dict[str, Any]] = []
    passed: list[str] = []

    for client, cfg in sorted(clients.items()):
        capability = {_norm_type(str(x)) for x in cfg.get("native_rule_types", [])}
        expected = {(typ, value) for typ, value in ir_rules if typ in capability}
        actual = _extract_client(args.generated / client, str(cfg["artifact"]))
        missing = sorted(expected - actual)
        unexpected = sorted(actual - ir_rules)
        if missing or unexpected:
            failures.append({"client": client, "missing": missing, "unexpected": unexpected})
        else:
            passed.append(client)

    report = {"schema": "cross_client_semantic_v1", "pass": not failures, "passed": passed, "failures": failures}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
