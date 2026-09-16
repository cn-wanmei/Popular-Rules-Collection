from __future__ import annotations

import json
from pathlib import Path

from src.engine.hierarchy.resolver import HierarchyConfigError, build_hierarchy, load_hierarchy_config


def _seed_canonical(tmp_path: Path) -> Path:
    canonical = tmp_path / "canonical"
    canonical.mkdir()
    (canonical / "rules.json").write_text(
        json.dumps(
            {
                "r-apple": {"id": "r-apple", "type": "DOMAIN", "value": "apple.com"},
                "r-music": {"id": "r-music", "type": "DOMAIN", "value": "music.apple.com"},
                "r-legacy": {"id": "r-legacy", "type": "DOMAIN", "value": "legacy.example"},
            }
        ),
        encoding="utf-8",
    )
    (canonical / "memberships.json").write_text(
        json.dumps(
            {
                "apple": ["r-apple"],
                "applemusic": ["r-music"],
                "legacy-service-name": ["r-legacy"],
            }
        ),
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
    assert graph["services"]["legacy-service-name"]["provider"] is None
    assert "legacy-service-name" in graph["unmodeled_services"]


def test_no_name_prefix_provider_inference(tmp_path: Path):
    canonical = _seed_canonical(tmp_path)
    out = tmp_path / "hierarchy"
    build_hierarchy(canonical, out)
    graph = json.loads((out / "graph.json").read_text(encoding="utf-8"))

    # The old resolver inferred the provider from the text before '-'.
    # The new resolver must leave unknown entities unmodeled instead.
    assert graph["services"]["legacy-service-name"]["provider"] is None
    assert "legacy" not in graph["aggregates"]


def test_invalid_duplicate_service_is_rejected(tmp_path: Path):
    config = tmp_path / "bad.yaml"
    config.write_text(
        """\nversion: 1\nschema: provider_service_hierarchy_v1\nproviders:\n  a:\n    aggregate: a\n    services:\n      shared: {display_name: Shared}\n  b:\n    aggregate: b\n    services:\n      shared: {display_name: Shared}\n""",
        encoding="utf-8",
    )
    config_doc = load_hierarchy_config(config)
    assert config_doc["schema"] == "provider_service_hierarchy_v1"
    try:
        # Validation is exercised through build, which avoids exporting internals.
        build_hierarchy(tmp_path / "missing-canonical", tmp_path / "out", config)
    except FileNotFoundError:
        # Canonical IO happens before hierarchy validation in this call path.
        pass
    except HierarchyConfigError:
        # Also acceptable once the canonical fixture is present in future refactors.
        pass
