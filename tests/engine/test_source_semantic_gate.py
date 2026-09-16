from src.engine.validation.source_semantic import validate_records


def test_geosite_suffix_without_dot_is_allowed_when_explicit():
    report = validate_records([
        {
            "service": "alibaba",
            "type": "domain_suffix",
            "value": "alibaba",
            "provenance": {"format": "metacubex_geosite"},
        }
    ])
    assert report["pass"] is True


def test_suffix_without_dot_is_rejected_for_generic_plain_input():
    report = validate_records([
        {
            "service": "example",
            "type": "domain_suffix",
            "value": "example",
            "provenance": {"format": "plain_list"},
        }
    ])
    assert report["pass"] is False
    assert report["failures"][0]["reason"] == "suffix_without_dot_requires_explicit_suffix_format"


def test_invalid_cidr_and_regex_are_rejected():
    report = validate_records([
        {"type": "ip_cidr", "value": "999.1.1.1/24", "provenance": {"format": "native_list"}},
        {"type": "domain_regex", "value": "[", "provenance": {"format": "native_list"}},
    ])
    assert report["pass"] is False
    assert len(report["failures"]) == 2
