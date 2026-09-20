from __future__ import annotations

from scripts.phase_j_p0_service_evidence import canonicalize, parse_rules, positive_and_negative, service_token_match


def test_service_token_match_accepts_exact_service_filename() -> None:
    assert service_token_match("geosite_deepseek.list", "deepseek")
    assert service_token_match("Clash_TestFlight.yaml", "testflight")
    assert not service_token_match("Clash_Apple.yaml", "appledev")


def test_parse_rules_and_canonical_identity_are_deterministic() -> None:
    rules = parse_rules("+.example.com\napi.example.com\nIP-CIDR,192.0.2.0/24\n")
    canonical = canonicalize(rules)
    assert [r["type"] for r in canonical] == ["DOMAIN-SUFFIX", "DOMAIN-SUFFIX", "IP-CIDR"]
    assert canonical[0]["identity_key"] == "domain-suffix|example.com"
    assert len(canonical[0]["rule_id"]) == 64


def test_keyword_rule_requires_explicit_review() -> None:
    semantic = __import__("scripts.phase_j_p0_service_evidence", fromlist=["semantic_audit"]).semantic_audit(
        canonicalize([{ "type": "HOST-KEYWORD", "value": "testflight" }])
    )
    assert semantic["status"] == "blocked"
    assert "keyword_rule_requires_explicit_acceptance" in semantic["reasons"]


def test_cidr_probe_has_inside_and_outside_examples() -> None:
    positive, negative = positive_and_negative({"type": "IP-CIDR", "value": "192.0.2.0/24"})
    assert positive == "192.0.2.1"
    assert negative == "192.0.3.0"
