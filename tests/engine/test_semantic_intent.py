from __future__ import annotations

from pathlib import Path

import pytest

from src.engine.semantic_intent import SemanticIntentError, apply_semantic_intent, validate_semantic_probes


POLICY = Path(__file__).resolve().parents[2] / "config" / "semantic_intent.yaml"


def _rule(rule_id: str, value: str, *, source: str = "blackmatrix7", rule_type: str = "DOMAIN-SUFFIX") -> dict:
    return {
        "id": rule_id,
        "type": rule_type,
        "value": value,
        "identity_key": f"{rule_type}:{value}",
        "classification": {"category": "other"},
        "provenance": {"sources": [{"id": source}], "format": "v2fly"},
    }


def test_alibaba_override_is_explicit_and_audited() -> None:
    rules = [
        _rule("r1", "alibaba"),
        _rule("r2", "alipay"),
        _rule("r3", "alibaba.com"),
    ]
    memberships = {"alibaba": ["r1", "r2", "r3"]}

    transformed, report = apply_semantic_intent(rules, memberships, policy_path=POLICY)
    by_id = {r["id"]: r for r in transformed}

    assert by_id["r1"]["type"] == "DOMAIN-KEYWORD"
    assert by_id["r2"]["type"] == "DOMAIN-KEYWORD"
    assert by_id["r3"]["type"] == "DOMAIN-SUFFIX"
    assert report["applied_count"] == 2
    marker = by_id["r1"]["provenance"]["semantic_transformations"][0]
    assert marker["from_type"] == "DOMAIN-SUFFIX"
    assert marker["to_type"] == "DOMAIN-KEYWORD"
    assert marker["policy_id"] == "blackmatrix7-alibaba-brand-aliases"


def test_unrelated_bare_suffix_is_not_globally_rewritten() -> None:
    rules = [_rule("r1", "localhost", source="other-source")]
    memberships = {"lan": ["r1"]}

    transformed, report = apply_semantic_intent(rules, memberships, policy_path=POLICY)

    assert transformed[0]["type"] == "DOMAIN-SUFFIX"
    assert report["applied_count"] == 0


def test_wrong_source_is_not_rewritten() -> None:
    rules = [_rule("r1", "alibaba", source="another-source")]
    memberships = {"alibaba": ["r1"]}

    transformed, report = apply_semantic_intent(rules, memberships, policy_path=POLICY)

    assert transformed[0]["type"] == "DOMAIN-SUFFIX"
    assert report["applied_count"] == 0


def test_semantic_probes_verify_behavior() -> None:
    rules, _ = apply_semantic_intent(
        [
            _rule("r1", "alibaba"),
            _rule("r2", "alipay"),
            _rule("r3", "taobao"),
            _rule("r4", "tmall"),
        ],
        {"alibaba": ["r1", "r2", "r3", "r4"]},
        policy_path=POLICY,
    )
    report = validate_semantic_probes(
        rules,
        {"alibaba": ["r1", "r2", "r3", "r4"]},
        policy_path=POLICY,
    )

    assert report["probe_count"] == 6
    assert all(item["expected"] == item["matched"] for item in report["probes"])


def test_semantic_probes_are_idempotent_after_ir_projection() -> None:
    rules, report = apply_semantic_intent(
        [_rule('r1', 'alibaba'), _rule('r2', 'alipay'), _rule('r3', 'taobao'), _rule('r4', 'tmall')],
        {'alibaba': ['r1', 'r2', 'r3', 'r4']},
        policy_path=POLICY,
    )
    reparsed = [{k: v for k, v in rule.items() if k != 'provenance'} for rule in rules]
    probe = validate_semantic_probes(
        reparsed,
        {'alibaba': ['r1', 'r2', 'r3', 'r4']},
        policy_path=POLICY,
        semantic_intent=report,
    )
    assert all(item['expected'] == item['matched'] for item in probe['probes'])


def test_probe_fails_when_policy_projection_is_broken() -> None:
    rules = [
        _rule("r1", "alibaba"),
        _rule("r2", "alipay"),
        _rule("r3", "taobao"),
        _rule("r4", "tmall"),
    ]
    memberships = {"alibaba": ["r1", "r2", "r3", "r4"]}

    with pytest.raises(SemanticIntentError, match="semantic probe failed"):
        validate_semantic_probes(rules, memberships, policy_path=POLICY)
