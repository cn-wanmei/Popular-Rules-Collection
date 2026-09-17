from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.engine.hierarchy.resolver import (
    HierarchyConfigError,
    build_hierarchy,
    load_hierarchy_config,
    validate_hierarchy_config,
)


def _seed_canonical(tmp_path: Path) -> Path:
    canonical = tmp_path / "canonical"
    canonical.mkdir()
    rules = [
        {"id": "r-apple", "type": "DOMAIN", "value": "apple.com"},
        {"id": "r-music", "type": "DOMAIN", "value": "music.apple.com"},
        {"id": "r-aws", "type": "DOMAIN", "value": "aws.amazon.com"},
        {"id": "r-legacy", "type": "DOMAIN", "value": "legacy.example"},
    ]
    memberships = [
        {"rule_id": "r-apple", "entity": "apple", "relation": "member"},
        {"rule_id": "r-music", "entity": "applemusic", "relation": "member"},
        {"rule_id": "r-aws", "entity": "aws", "relation": "member"},
        {"rule_id": "r-legacy", "entity": "legacy-service-name", "relation": "member"},
    ]
    (canonical / "rules.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in rules),
        encoding="utf-8",
    )
    (canonical / "memberships.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in memberships),
        encoding="utf-8",
    )
    return canonical


def test_explicit_provider_service_relationships(tmp_path: Path):
    canonical = _seed_canonical(tmp_path)
    out = tmp_path / "hierarchy"

    manifest = build_hierarchy(canonical, out)
    graph = json.loads((out / "graph.json").read_text(encoding="utf-8"))

    assert manifest["configured_service_count"] > 0
    assert graph["services"]["applemusic"]["provider"] == "apple"
    assert graph["services"]["applemusic"]["parent"] == "apple"
    assert graph["aggregates"]["apple"]["rule_ids"] == ["r-apple", "r-music"]
    assert graph["services"]["aws"]["provider"] == "amazon"
    assert graph["services"]["aws"]["parent"] == "amazon"
    assert graph["aggregates"]["amazon"]["rule_ids"] == ["r-aws"]
    assert "aws" in graph["categories"]["developer"]["services"]
    assert graph["categories"]["developer"]["rule_ids"] == ["r-aws"]
    assert graph["services"]["legacy-service-name"]["provider"] is None
    assert "legacy-service-name" in graph["unmodeled_services"]


def test_no_name_prefix_provider_inference(tmp_path: Path):
    canonical = _seed_canonical(tmp_path)
    out = tmp_path / "hierarchy"
    build_hierarchy(canonical, out)
    graph = json.loads((out / "graph.json").read_text(encoding="utf-8"))

    assert graph["services"]["legacy-service-name"]["provider"] is None
    assert "legacy" not in graph["aggregates"]
    assert graph["groups"] == {}


def test_invalid_duplicate_service_is_rejected(tmp_path: Path):
    config = tmp_path / "bad.yaml"
    config.write_text(
        """\nversion: 1\nschema: provider_service_hierarchy_v1\nproviders:\n  a:\n    aggregate: a\n    services:\n      shared: {display_name: Shared}\n  b:\n    aggregate: b\n    services:\n      shared: {display_name: Shared}\n""",
        encoding="utf-8",
    )
    config_doc = load_hierarchy_config(config)
    with pytest.raises(HierarchyConfigError):
        validate_hierarchy_config(config_doc)
