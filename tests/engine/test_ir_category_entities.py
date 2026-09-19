import json
from pathlib import Path

from src.engine.ir.builder import build_ir


def test_build_ir_includes_category_aggregates_in_entity_universe(tmp_path: Path) -> None:
    canonical = tmp_path / "canonical"
    hierarchy = tmp_path / "hierarchy"
    out = tmp_path / "ir"
    canonical.mkdir()
    hierarchy.mkdir()

    (canonical / "rules.jsonl").write_text(
        json.dumps(
            {
                "id": "r1",
                "type": "DOMAIN-SUFFIX",
                "value": "example.com",
                "identity_key": "DOMAIN-SUFFIX:example.com",
                "classification": {"category": "other"},
                "provenance": {},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (canonical / "memberships.jsonl").write_text(
        json.dumps({"rule_id": "r1", "entity": "developer", "relation": "member"}) + "\n",
        encoding="utf-8",
    )
    (hierarchy / "graph.json").write_text(
        json.dumps(
            {
                "services": {},
                "groups": {},
                "aggregates": {"provider": {"id": "provider"}},
                "categories": {"developer": {"id": "developer", "type": "category_aggregate"}},
            }
        ),
        encoding="utf-8",
    )

    manifest = build_ir(canonical, hierarchy, out)
    assert manifest["stats"]["aggregates"] == 2

    ir = json.loads((out / "ir.json").read_text(encoding="utf-8"))
    assert "developer" in ir["entities"]["aggregates"]
    assert "developer" in ir["views"]["aggregates"]
    assert ir["decisions"][0]["entities"] == ["developer"]
