import copy
import json

import pytest

from src.engine.ir.contract import CONTRACT_VERSION, IRContractError, ir_digest, validate_ir


def sample_ir():
    return {
        "schema": "semantic_ir_v2",
        "generated_at": "2026-09-02T00:00:00+00:00",
        "engine_version": "1.0.1",
        "v2_runtime_dependency": 0,
        "entities": {"services": ["a"], "groups": [], "aggregates": []},
        "entity": {"services": ["a"], "groups": [], "aggregates": []},
        "views": {"services": {}, "groups": {}, "aggregates": {}},
        "view": {"services": {}, "groups": {}, "aggregates": {}},
        "memberships": {},
        "rules": [{"id": "1", "type": "domain", "value": "a.com", "identity_key": "domain|a.com", "classification": {}, "provenance": {}}],
        "decisions": [],
        "stats": {"rules": 1, "services": 1, "groups": 0, "aggregates": 0, "decisions": 0},
    }


def test_contract_accepts_current_ir():
    validate_ir(sample_ir())
    assert CONTRACT_VERSION == "2.0"


@pytest.mark.parametrize("field", ["schema", "entities", "views", "memberships", "rules", "decisions", "stats"])
def test_contract_rejects_missing_required_field(field):
    ir = sample_ir()
    del ir[field]
    with pytest.raises(IRContractError):
        validate_ir(ir)


def test_contract_rejects_wrong_type_and_nonzero_v2_dependency():
    ir = sample_ir()
    ir["rules"] = {}
    with pytest.raises(IRContractError):
        validate_ir(ir)
    ir = sample_ir()
    ir["v2_runtime_dependency"] = 1
    with pytest.raises(IRContractError):
        validate_ir(ir)


def test_digest_ignores_volatile_timestamp_and_legacy_aliases():
    left = sample_ir()
    right = copy.deepcopy(left)
    right["generated_at"] = "2026-09-03T00:00:00+00:00"
    right["entity"] = {"services": ["different"]}
    right["view"] = {"services": {"different": []}, "groups": {}, "aggregates": {}}
    assert ir_digest(left) == ir_digest(right)


def test_digest_is_canonical_json_sha256():
    ir = sample_ir()
    payload = {k: v for k, v in ir.items() if k not in {"generated_at", "entity", "view"}}
    expected = __import__("hashlib").sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert ir_digest(ir) == expected
