from src.engine.audit.matcher import rule_matches


def test_host_exact_is_boundary_safe():
    rule = {"type": "host", "value": "apps.apple.com"}
    assert rule_matches(rule, "apps.apple.com")
    assert not rule_matches(rule, "apps.apple.com.evil.example")


def test_domain_suffix_matches_root_and_subdomain_only():
    rule = {"type": "domain_suffix", "value": "developer.apple.com"}
    assert rule_matches(rule, "developer.apple.com")
    assert rule_matches(rule, "api.developer.apple.com")
    assert not rule_matches(rule, "developer.apple.com.evil.example")


def test_keyword_is_explicit_broad_match():
    rule = {"type": "host-keyword", "value": "testflight"}
    assert rule_matches(rule, "api.testflight.apple.com")
    assert rule_matches(rule, "not-testflight.example.com")
