import json
from pathlib import Path

from src.engine.adapters.build_all import build_all_clients


def test_build_all_projects_rules_to_client_capabilities(tmp_path: Path) -> None:
    ir_dir = tmp_path / "ir"
    artifacts = tmp_path / "artifacts"
    ir_dir.mkdir()
    ir = {
        "schema": "semantic_ir_v2",
        "v2_runtime_dependency": 0,
        "rules": [
            {"id": "domain-1", "type": "DOMAIN", "value": "example.com"},
            {"id": "regex-1", "type": "DOMAIN-REGEX", "value": r"^.*\\.example\\.com$"},
        ],
        "memberships": {"test": ["domain-1", "regex-1"]},
        "entities": {"services": ["test"]},
    }
    (ir_dir / "ir.json").write_text(json.dumps(ir), encoding="utf-8")

    report = build_all_clients(ir_dir, artifacts)

    surge = report["clients"]["surge"]
    assert surge["input_rules"] == 2
    assert surge["emitted_rules"] == 1
    assert surge["skipped_unsupported_rule_types"] == {"domain_regex": 1}
    assert (artifacts / "surge" / "aggregate.list").read_text(encoding="utf-8") == "DOMAIN,example.com\n"

    mihomo = report["clients"]["mihomo"]
    assert mihomo["emitted_rules"] == 2
    assert "domain_regex" not in mihomo["skipped_unsupported_rule_types"]
