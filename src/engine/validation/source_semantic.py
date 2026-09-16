"""Source -> Semantic IR admission gate.

This gate validates that parser-produced rule semantics are plausible for the
identified input format before records enter Quarantine/Canonical.
"""
from __future__ import annotations

import ipaddress
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DOMAIN_TYPES = {"domain", "domain_suffix", "domain_keyword", "domain_regex"}
SUFFIX_WITHOUT_DOT_ALLOWED = {"metacubex_geosite", "v2fly"}


def _invalid(record: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "service": record.get("service"),
        "type": record.get("type"),
        "value": record.get("value"),
        "provenance": record.get("provenance"),
        "reason": reason,
    }


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for record in records:
        typ = str(record.get("type") or "").strip().lower().replace("-", "_")
        value = str(record.get("value") or "").strip()
        provenance = record.get("provenance") or {}
        source_format = str(provenance.get("format") or "auto")

        if not typ or not value:
            failures.append(_invalid(record, "missing_type_or_value"))
            continue

        if typ in {"domain", "domain_suffix"}:
            if any(ch.isspace() for ch in value) or "/" in value:
                failures.append(_invalid(record, "domain_contains_space_or_path_separator"))
            if typ == "domain_suffix" and "." not in value and source_format not in SUFFIX_WITHOUT_DOT_ALLOWED:
                failures.append(_invalid(record, "suffix_without_dot_requires_explicit_suffix_format"))

        elif typ == "domain_keyword":
            if any(ch.isspace() for ch in value):
                failures.append(_invalid(record, "keyword_contains_whitespace"))

        elif typ == "domain_regex":
            try:
                re.compile(value)
            except re.error as exc:
                failures.append(_invalid(record, f"invalid_regex:{exc}"))

        elif typ in {"ip_cidr", "ip_cidr6"}:
            try:
                net = ipaddress.ip_network(value, strict=False)
                if typ == "ip_cidr" and net.version != 4:
                    failures.append(_invalid(record, "ipv4_rule_contains_ipv6_network"))
                if typ == "ip_cidr6" and net.version != 6:
                    failures.append(_invalid(record, "ipv6_rule_contains_ipv4_network"))
            except ValueError as exc:
                failures.append(_invalid(record, f"invalid_cidr:{exc}"))

    return {
        "schema": "source_semantic_gate_v1",
        "checked": len(records),
        "failures": failures,
        "pass": not failures,
    }


def run_source_semantic_gate(
    ingest_result: dict[str, Any],
    out_dir: Path,
) -> dict[str, Any]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = validate_records(list(ingest_result.get("records") or []))
    report.update({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_id": ingest_result.get("snapshot_id"),
        "v2_runtime_dependency": 0,
    })
    (out_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report
