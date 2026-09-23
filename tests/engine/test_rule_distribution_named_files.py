from __future__ import annotations

import json
from pathlib import Path

import yaml

from src.engine.distribution.rule_tree import build_rule_tree
from src.engine.validation.directory_contract import validate


def _fixtures(tmp_path: Path) -> tuple[Path, Path, Path]:
    ir_dir = tmp_path / "ir"
    ir_dir.mkdir()
    ir = {
        "schema": "semantic_ir_v2",
        "v2_runtime_dependency": 0,
        "rules": [
            {"id": "r1", "type": "DOMAIN_SUFFIX", "value": "apple.com"},
        ],
        "memberships": {
            "apple": ["r1"],
            "appstore": ["r1"],
            "developer": ["r1"],
            "mystery": ["r1"],
        },
        "entities": {
            "services": ["appstore"],
            "groups": [],
            "aggregates": ["developer"],
        },
    }
    (ir_dir / "ir.json").write_text(json.dumps(ir), encoding="utf-8")
    (ir_dir / "manifest.json").write_text(
        json.dumps({"ir_digest": "0" * 64}),
        encoding="utf-8",
    )

    hierarchy = tmp_path / "hierarchy.yaml"
    hierarchy.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "schema": "provider_service_hierarchy_v1",
                "providers": {
                    "apple": {
                        "display_name": "Apple",
                        "aggregate": "apple",
                        "services": {
                            "appstore": {
                                "display_name": "App Store",
                                "status": "split",
                            }
                        },
                    }
                },
                "categories": {},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    policy = tmp_path / "directories.yaml"
    policy.write_text(
        yaml.safe_dump(
            {
                "schema": "rule_distribution_policy_v2",
                "layout": {
                    "human_aggregate": "rule/{provider}/{provider}.yaml",
                    "human_service": "rule/{provider}/{service}/{service}.yaml",
                    "human_china": "rule/china/china.yaml",
                    "human_category": "rule/category/{category}/{category}.yaml",
                    "human_group": "rule/group/{group}/{group}.yaml",
                    "human_aggregate_entity": "rule/aggregate/{aggregate}/{aggregate}.yaml",
                    "human_unmapped_service": "rule/unmapped/{service}/{service}.yaml",
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return ir_dir, hierarchy, policy


def test_rule_tree_uses_entity_named_files(tmp_path: Path) -> None:
    ir_dir, hierarchy, policy = _fixtures(tmp_path)
    out = tmp_path / "rule"
    manifest = build_rule_tree(
        ir_dir,
        out,
        hierarchy_path=hierarchy,
        policy_path=policy,
        run_id="test-run",
    )

    expected = {
        "apple/apple.yaml",
        "apple/appstore/appstore.yaml",
        "aggregate/developer/developer.yaml",
        "unmapped/mystery/mystery.yaml",
    }
    assert set(manifest["files"]) == expected
    assert (out / "apple/apple.yaml").is_file()
    assert (out / "apple/appstore/appstore.yaml").is_file()
    assert not (out / "apple/all/rules.yaml").exists()
    assert not (out / "apple/appstore/rules.yaml").exists()


def test_directory_contract_accepts_named_file_tree(tmp_path: Path) -> None:
    ir_dir, hierarchy, policy = _fixtures(tmp_path)
    out = tmp_path / "rule"
    build_rule_tree(
        ir_dir,
        out,
        hierarchy_path=hierarchy,
        policy_path=policy,
        run_id="test-run",
    )

    repo_root = Path(__file__).resolve().parents[2]
    report = validate(repo_root, rule_root=out, generated_root=tmp_path / "generated")
    assert report["pass"], report["errors"]
