"""Fail-closed validation for rule/generated distribution manifests."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.engine.distribution.path_resolver import EntityPathResolver


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _duplicates(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for path in paths:
        if path in seen:
            duplicates.add(path)
        seen.add(path)
    return sorted(duplicates)


def _legacy_rule(paths: list[str]) -> list[str]:
    result: list[str] = []
    for path in paths:
        parts = Path(path).parts
        if len(parts) == 2 and parts[0] not in {"china", "category", "group", "aggregate", "unmapped"}:
            if parts[1] == f"{parts[0]}.yaml":
                result.append(path)
    return sorted(set(result))


def _legacy_generated(paths: list[str]) -> list[str]:
    result: list[str] = []
    for path in paths:
        parts = Path(path).parts
        if len(parts) == 2 and parts[0] not in {"china", "categories", "_promotion"}:
            if Path(parts[1]).stem == parts[0]:
                result.append(path)
    return sorted(set(result))


def validate_distribution(
    *,
    rule_root: Path,
    artifacts_root: Path,
    build_report: dict[str, Any],
    expected_run_id: str,
) -> dict[str, Any]:
    rule_manifest = _load_json(Path(rule_root) / "manifest.json")
    errors: list[str] = []

    rule_paths = [str(x) for x in (rule_manifest.get("files") or [])]
    duplicates = _duplicates(rule_paths)
    legacy_rule = _legacy_rule(rule_paths)

    if duplicates:
        errors.append("duplicate_paths: " + ", ".join(duplicates))
    if legacy_rule:
        errors.append("legacy_layout: " + ", ".join(legacy_rule))
    if rule_manifest.get("schema_version") != 2:
        errors.append("rule manifest schema_version mismatch")
    if rule_manifest.get("layout_schema") != EntityPathResolver.LAYOUT_SCHEMA:
        errors.append("rule manifest layout_schema mismatch")
    if rule_manifest.get("run_id") != expected_run_id:
        errors.append("rule manifest run_id mismatch")

    rule_ir = str(rule_manifest.get("ir_digest") or "").strip()
    generated_run = str(build_report.get("run_id") or "").strip()
    generated_ir = str(build_report.get("ir_digest") or "").strip()

    if generated_run != expected_run_id:
        errors.append("generated build_report run_id mismatch")
    if not generated_ir:
        errors.append("generated build_report missing ir_digest")
    if rule_ir != generated_ir:
        errors.append("rule/generated ir_digest mismatch")
    if build_report.get("schema_version") != 2:
        errors.append("generated build_report schema_version mismatch")
    if build_report.get("layout_schema") != EntityPathResolver.LAYOUT_SCHEMA:
        errors.append("generated build_report layout_schema mismatch")
    if build_report.get("resolver") != "EntityPathResolver":
        errors.append("generated build_report resolver mismatch")

    generated_duplicates = 0
    generated_legacy = 0
    for client, details in sorted((build_report.get("clients") or {}).items()):
        paths = [str(x) for x in (details.get("paths") or [])]
        dups = _duplicates(paths)
        legacy = _legacy_generated(paths)
        generated_duplicates += len(dups)
        generated_legacy += len(legacy)
        if dups:
            errors.append(f"generated duplicate_paths[{client}]: " + ", ".join(dups))
        if legacy:
            errors.append(f"generated legacy_layout[{client}]: " + ", ".join(legacy))

    return {
        "schema": "distribution_manifest_validation_v1",
        "layout_schema": EntityPathResolver.LAYOUT_SCHEMA,
        "pass": not errors,
        "errors": errors,
        "duplicate_paths": len(duplicates) + generated_duplicates,
        "legacy_layout": len(legacy_rule) + generated_legacy,
        "rule_run_id": rule_manifest.get("run_id"),
        "generated_run_id": generated_run,
        "ir_digest_match": bool(rule_ir) and rule_ir == generated_ir,
        "resolver": build_report.get("resolver"),
        "artifacts_root": str(Path(artifacts_root)),
    }


__all__ = ["validate_distribution"]
