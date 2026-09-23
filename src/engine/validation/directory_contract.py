"""V3 human rule and generated distribution directory validation."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
_METADATA_FILES = {"_index.yaml", "manifest.json", "README.md"}
_SPECIAL_ROOTS = {"category", "group", "aggregate", "unmapped"}
_ENTITY_TYPES = {
    "category": "category",
    "group": "group",
    "aggregate": "aggregate",
    "unmapped": "unmapped_service",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping: {path}")
    return data


def _all_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return [p for p in root.rglob("*") if p.is_file()]


def _rule_files(root: Path) -> list[Path]:
    return [
        p for p in _all_files(root)
        if p.name.endswith(".yaml") and p.name not in _METADATA_FILES
    ]


def _valid_rule_path(root: Path, path: Path) -> bool:
    parts = path.relative_to(root).parts
    if len(parts) == 1 and parts[0] in _METADATA_FILES:
        return True
    if any(part in {".", "..", "all", "rules"} for part in parts):
        return False
    if len(parts) == 2 and parts[1] == f"{parts[0]}.yaml":
        return bool(re.fullmatch(r"[a-z0-9][a-z0-9._-]*", parts[0]))
    if len(parts) == 3 and parts[2] == f"{parts[1]}.yaml":
        return all(
            bool(re.fullmatch(r"[a-z0-9][a-z0-9._-]*", part))
            for part in parts[:2]
        )
    return False


def _entity_expectation(root: Path, path: Path) -> tuple[str, str, str | None]:
    parts = path.relative_to(root).parts
    if len(parts) == 2:
        if parts[0] == "china":
            return "domestic_aggregate", "china", None
        return "provider_aggregate", parts[0], parts[0]
    if parts[0] in _ENTITY_TYPES:
        return _ENTITY_TYPES[parts[0]], parts[1], None
    return "service", parts[1], parts[0]


def _validate_rule_payload(
    root: Path,
    path: Path,
    expected_run_id: str | None,
) -> list[str]:
    errors: list[str] = []
    try:
        payload = _load_yaml(path)
    except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError) as exc:
        return [f"invalid human rule payload: {path.relative_to(root)}: {exc}"]

    entity, entity_id, provider = _entity_expectation(root, path)
    rel = path.relative_to(root).as_posix()

    if payload.get("schema") != "human_rule_distribution_v1":
        errors.append(f"invalid human rule schema: {rel}")
    if payload.get("entity") != entity:
        errors.append(f"human rule entity mismatch: {rel}")
    if str(payload.get("id") or "").strip() != entity_id:
        errors.append(f"human rule id mismatch: {rel}")

    actual_provider = str(payload.get("provider") or "").strip().casefold()
    if provider is not None and actual_provider != provider.casefold():
        errors.append(f"human rule provider mismatch: {rel}")
    if provider is None and payload.get("provider") not in {None, ""}:
        errors.append(f"unexpected human rule provider: {rel}")

    generated_from = payload.get("generated_from") or {}
    actual_run_id = str(generated_from.get("run_id") or "").strip()
    if expected_run_id and actual_run_id != expected_run_id:
        errors.append(
            f"human rule lineage mismatch: {rel} "
            f"(expected run_id={expected_run_id}, actual={actual_run_id or 'missing'})"
        )
    if not str(generated_from.get("ir_digest") or "").strip():
        errors.append(f"human rule missing ir_digest: {rel}")
    return errors


def validate(
    root: Path = ROOT,
    *,
    rule_root: Path | None = None,
    generated_root: Path | None = None,
) -> dict[str, Any]:
    workspace_root = Path(root).resolve()
    policy_path = workspace_root / "config/service_model/directories.yaml"
    policy = _load_yaml(policy_path)
    errors: list[str] = []

    if policy.get("schema") != "rule_distribution_policy_v2":
        errors.append("unsupported rule distribution policy schema")

    layout = policy.get("layout") or {}
    expected_templates = {
        "human_aggregate": "rule/{provider}/{provider}.yaml",
        "human_service": "rule/{provider}/{service}/{service}.yaml",
        "human_china": "rule/china/china.yaml",
        "human_category": "rule/category/{category}/{category}.yaml",
        "human_group": "rule/group/{group}/{group}.yaml",
        "human_aggregate_entity": "rule/aggregate/{aggregate}/{aggregate}.yaml",
        "human_unmapped_service": "rule/unmapped/{service}/{service}.yaml",
    }
    for key, expected in expected_templates.items():
        if str(layout.get(key) or "").strip() != expected:
            errors.append(
                f"directory policy layout mismatch: {key} must be {expected}"
            )

    alternate = workspace_root / "rules"
    if alternate.exists():
        errors.append("obsolete third rule tree exists: rules/")

    rule_root = (
        Path(rule_root).resolve()
        if rule_root is not None
        else workspace_root / "rule"
    )
    generated_root = (
        Path(generated_root).resolve()
        if generated_root is not None
        else workspace_root / "generated"
    )

    if not rule_root.is_dir():
        errors.append(f"human rule distribution root does not exist: {rule_root}")
    else:
        for required in ("README.md", "_index.yaml", "manifest.json"):
            if not (rule_root / required).is_file():
                errors.append(
                    f"missing human distribution metadata: {rule_root / required}"
                )

        all_payload_files = [
            p for p in _all_files(rule_root) if p.name not in _METADATA_FILES
        ]
        for path in all_payload_files:
            if not _valid_rule_path(rule_root, path):
                errors.append(f"invalid human rule path: {path}")

        manifest: dict[str, Any] = {}
        index: dict[str, Any] = {}
        try:
            manifest = json.loads(
                (rule_root / "manifest.json").read_text(encoding="utf-8")
            )
            index = _load_yaml(rule_root / "_index.yaml")

            if manifest.get("schema") != "human_rule_distribution_manifest_v1":
                errors.append("invalid human distribution manifest schema")
            if index.get("schema") != "human_rule_distribution_index_v1":
                errors.append("invalid human distribution index schema")

            if manifest.get("status") == "ready":
                if (
                    manifest.get("run_id") != index.get("run_id")
                    or manifest.get("ir_digest") != index.get("ir_digest")
                ):
                    errors.append(
                        "human distribution manifest/index identity mismatch"
                    )

                actual_paths = sorted(
                    p.relative_to(rule_root).as_posix()
                    for p in _rule_files(rule_root)
                )
                manifest_paths = sorted(
                    str(x) for x in (manifest.get("files") or [])
                )
                if manifest_paths != actual_paths:
                    errors.append(
                        "human distribution manifest file list does not match tree"
                    )

                index_paths = sorted(
                    str(entry.get("path"))
                    for entry in (index.get("entries") or [])
                    if isinstance(entry, dict) and entry.get("path")
                )
                if index_paths != actual_paths:
                    errors.append(
                        "human distribution index file list does not match tree"
                    )

            expected_run_id = (
                str(manifest.get("run_id") or "").strip()
                if manifest.get("status") == "ready"
                else None
            )
            for path in _rule_files(rule_root):
                errors.extend(
                    _validate_rule_payload(rule_root, path, expected_run_id)
                )
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
            yaml.YAMLError,
        ) as exc:
            errors.append(f"invalid human distribution metadata: {exc}")

    return {
        "schema": "rule_distribution_gate_v3",
        "pass": not errors,
        "errors": errors,
        "human_rule_files": len(_rule_files(rule_root)),
        "canonical_rule_files": len(_rule_files(rule_root)),
        "generated_rule_files": len(_rule_files(generated_root)),
        "alternate_rule_tree_exists": alternate.exists(),
        "china_excluded_independent_providers": [
            str(x).strip().lower()
            for x in (
                (policy.get("china") or {}).get(
                    "exclude_independent_providers"
                )
                or []
            )
        ],
        "policy": str(policy_path.relative_to(workspace_root)),
        "rule_root": str(rule_root),
    }
