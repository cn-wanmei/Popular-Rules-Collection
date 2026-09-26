from __future__ import annotations

import json
from pathlib import Path

from src.engine.distribution.rule_tree import build_rule_tree


def test_rule_distribution_is_derived_from_ir_and_deterministic(tmp_path: Path):
    ir_dir = tmp_path / "ir"
    ir_dir.mkdir()
    ir = {
        "schema": "semantic_ir_v2",
        "generated_at": "2026-01-01T00:00:00Z",
        "engine_version": "3",
        "v2_runtime_dependency": 0,
        "entities": {"services": ["mail"], "groups": [], "aggregates": ["acme", "communication"]},
        "views": {"services": {}, "groups": {}, "aggregates": {}},
        "memberships": {"mail": ["r1"], "acme": ["r1", "r2"], "communication": ["r2"]},
        "rules": [
            {"id": "r2", "type": "DOMAIN-SUFFIX", "value": "example.com", "identity_key": "domain-suffix:example.com", "classification": {"category": "communication"}, "provenance": {}},
            {"id": "r1", "type": "DOMAIN", "value": "mail.example.com", "identity_key": "domain:mail.example.com", "classification": {"category": "communication"}, "provenance": {}},
        ],
        "decisions": [],
        "stats": {},
    }
    (ir_dir / "ir.json").write_text(json.dumps(ir, ensure_ascii=False), encoding="utf-8")
    (ir_dir / "manifest.json").write_text(json.dumps({"ir_digest": "a" * 64}), encoding="utf-8")
    hierarchy = tmp_path / "hierarchy.yaml"
    hierarchy.write_text(
        "version: 1\nschema: provider_service_hierarchy_v1\nproviders:\n"
        "  acme:\n    display_name: Acme\n    aggregate: acme\n    services:\n"
        "      mail: {display_name: Mail, status: existing}\ncategories:\n"
        "  communication:\n    display_name: Communication\n    aggregate: communication\n    services:\n"
        "      mail: {display_name: Mail, status: existing}\n",
        encoding="utf-8",
    )
    a = tmp_path / "a"
    b = tmp_path / "b"
    first = build_rule_tree(ir_dir, a, hierarchy_path=hierarchy, run_id="run-1")
    second = build_rule_tree(ir_dir, b, hierarchy_path=hierarchy, run_id="run-1")
    assert first["status"] == "ready"
    assert first["rule_file_count"] == 4
    assert (a / "acme" / "mail" / "mail.yaml").exists()
    assert (a / "acme" / "acme" / "acme.yaml").exists()
    assert (a / "category" / "communication" / "communication.yaml").exists()
    assert (a / "aggregate" / "communication" / "communication.yaml").exists()
    assert first["ir_digest"] == second["ir_digest"]
    assert (a / "acme" / "mail" / "mail.yaml").read_text(encoding="utf-8") == (b / "acme" / "mail" / "mail.yaml").read_text(encoding="utf-8")
    assert (a / "_index.yaml").read_text(encoding="utf-8") == (b / "_index.yaml").read_text(encoding="utf-8")