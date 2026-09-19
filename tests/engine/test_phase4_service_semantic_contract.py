from src.engine.service_semantics.contract import validate_service_semantics
def _valid_ir() -> dict:
    return {
        "entities": {"services": ["Example"], "groups": [], "aggregates": []},
        "rules": [{"id": "r1", "type": "DOMAIN-SUFFIX", "value": "example.com"}],
        "memberships": {"Example": ["r1"]},
        "decisions": [{"rule_id": "r1", "type": "DOMAIN-SUFFIX", "value": "example.com", "action": "PROXY", "entities": ["Example"], "category": "example"}],
    }
def test_semantic_contract_accepts_valid_ir() -> None:
    report = validate_service_semantics(_valid_ir())
    assert report.all_pass is True
    assert report.violations == []
def test_semantic_contract_rejects_invalid_action() -> None:
    ir = _valid_ir()
    ir["decisions"][0]["action"] = "MAYBE"
    report = validate_service_semantics(ir)
    assert report.all_pass is False
    assert any("invalid action" in item for item in report.violations)
def test_semantic_contract_rejects_unknown_reference() -> None:
    ir = _valid_ir()
    ir["memberships"]["Missing"] = ["r1"]
    report = validate_service_semantics(ir)
    assert report.all_pass is False
    assert any("unknown entity" in item for item in report.violations)
def test_semantic_contract_rejects_conflicting_decisions() -> None:
    ir = _valid_ir()
    ir["decisions"].append({"rule_id": "r1", "type": "DOMAIN-SUFFIX", "value": "example.com", "action": "DIRECT", "entities": ["Example"]})
    report = validate_service_semantics(ir)
    assert report.all_pass is False
    assert any("conflicting decisions" in item for item in report.violations)
