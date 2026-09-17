from src.engine.ingest.rule_parser import parse_line


def test_parse_host_rule():
    assert parse_line("HOST,apps.apple.com") == [("host", "apps.apple.com")]


def test_parse_host_keyword_rule():
    assert parse_line("HOST-KEYWORD,testflight") == [("host_keyword", "testflight")]


def test_parse_host_rule_with_trailing_dot():
    assert parse_line("HOST,apps.apple.com.") == [("host", "apps.apple.com")]
