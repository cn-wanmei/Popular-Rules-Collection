"""V3 human rule and generated distribution directory validation."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import yaml
ROOT = Path(__file__).resolve().parents[3]

def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping: {path}")
    return data

def _all_files(root: Path) -> list[Path]:
    if not root.exists(): return []
    return [p for p in root.rglob("*") if p.is_file()]

def _rule_files(root: Path) -> list[Path]:
    return [p for p in _all_files(root) if p.name == "rules.yaml"]

def _valid_rule_path(root: Path, path: Path) -> bool:
    parts = path.relative_to(root).parts
    if parts in (("_index.yaml",), ("manifest.json",), ("README.md",)): return True
    if len(parts) == 3 and parts[2] == "rules.yaml" and parts[1] == "all":
        return parts[0] == "china" or parts[0] not in {"category", "group", "aggregate", "unmapped"}
    if len(parts) == 3 and parts[2] == "rules.yaml":
        return parts[0] not in {"category", "group", "aggregate", "unmapped", "china"}
    if len(parts) == 4 and parts[0] == "category" and parts[2] == "all" and parts[3] == "rules.yaml":
        return True
    return False

def validate(root: Path = ROOT) -> dict[str, Any]:
    root = Path(root).resolve()
    policy_path = root / "config/service_model/directories.yaml"
    policy = _load_yaml(policy_path)
    errors: list[str] = []
    if policy.get("schema") != "rule_distribution_policy_v2":
        errors.append("unsupported rule distribution policy schema")
    alternate = root / "rules"
    if alternate.exists():
        errors.append("obsolete third rule tree exists: rules/")
    rule_root = root / "rule"
    generated_root = root / "generated"
    if not rule_root.is_dir():
        errors.append("human rule distribution root does not exist: rule/")
    else:
        for required in ("README.md", "_index.yaml", "manifest.json"):
            if not (rule_root / required).is_file():
                errors.append(f"missing human distribution metadata: rule/{required}")
        for path in _all_files(rule_root):
            if not _valid_rule_path(rule_root, path):
                errors.append(f"invalid human rule path: {path.relative_to(root)}")
        try:
            manifest = json.loads((rule_root / "manifest.json").read_text(encoding="utf-8"))
            index = _load_yaml(rule_root / "_index.yaml")
            if manifest.get("schema") != "human_rule_distribution_manifest_v1":
                errors.append("invalid human distribution manifest schema")
            if index.get("schema") != "human_rule_distribution_index_v1":
                errors.append("invalid human distribution index schema")
            if manifest.get("status") == "ready" and (manifest.get("run_id") != index.get("run_id") or manifest.get("ir_digest") != index.get("ir_digest")):
                errors.append("human distribution manifest/index identity mismatch")
        except (OSError, json.JSONDecodeError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"invalid human distribution metadata: {exc}")
    return {
        "schema": "rule_distribution_gate_v3",
        "pass": not errors,
        "errors": errors,
        "human_rule_files": len(_rule_files(rule_root)),
        "canonical_rule_files": len(_rule_files(rule_root)),
        "generated_rule_files": len(_rule_files(generated_root)),
        "alternate_rule_tree_exists": alternate.exists(),
        "china_excluded_independent_providers": [str(x).strip().lower() for x in ((policy.get("china") or {}).get("exclude_independent_providers") or [])],
        "policy": str(policy_path.relative_to(root)),
    }