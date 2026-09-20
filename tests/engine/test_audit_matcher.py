from __future__ import annotations

from src.engine.audit.matcher import matching_rules, rule_matches


def test_ipv4_cidr_matches_inside_and_rejects_outside() -> None:
    rule = {"type": "IP-CIDR", "value": "1.116.116.0/22"}
    assert rule_matches(rule, "1.116.116.1")
    assert rule_matches(rule, "1.116.119.255")
    assert not rule_matches(rule, "1.116.120.1")
    assert not rule_matches(rule, "2001:df6:f400::1")


def test_ipv6_cidr_matches_inside_and_rejects_outside() -> None:
    rule = {"type": "IP6-CIDR", "value": "2001:df6:f400::/48"}
    assert rule_matches(rule, "2001:df6:f400::1")
    assert rule_matches(rule, "2001:df6:f400:ffff::1")
    assert not rule_matches(rule, "2001:df6:f401::1")
    assert not rule_matches(rule, "1.116.116.1")


def test_matching_rules_preserves_rule_order_for_mixed_types() -> None:
    rules = [
        {"type": "HOST", "value": "example.com"},
        {"type": "IP-CIDR", "value": "192.0.2.0/24"},
        {"type": "IP6-CIDR", "value": "2001:db8::/32"},
    ]
    assert matching_rules(rules, "192.0.2.10") == [rules[1]]
    assert matching_rules(rules, "2001:db8::1") == [rules[2]]
