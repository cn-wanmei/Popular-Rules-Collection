from pathlib import Path

import yaml

from src.engine.adapters.egern import render


def test_egern_renders_native_rule_set_schema(tmp_path: Path):
    out = render(
        [
            {"type": "DOMAIN", "value": "example.com"},
            {"type": "DOMAIN-SUFFIX", "value": "google.com"},
            {"type": "DOMAIN-KEYWORD", "value": "youtube"},
            {"type": "DOMAIN-REGEX", "value": r"^ads?\\."},
            {"type": "IP-CIDR", "value": "192.168.0.0/16"},
            {"type": "IP-CIDR6", "value": "2001:db8::/32"},
        ],
        tmp_path / "12306.yaml",
    )

    payload = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert payload == {
        "domain_set": ["example.com"],
        "domain_suffix_set": ["google.com"],
        "domain_keyword_set": ["youtube"],
        "domain_regex_set": [r"^ads?\\."],
        "ip_cidr_set": ["192.168.0.0/16"],
        "ip_cidr6_set": ["2001:db8::/32"],
    }
    assert "payload" not in payload


def test_egern_rejects_clash_only_or_unknown_rule_types(tmp_path: Path):
    import pytest

    with pytest.raises(ValueError, match="Unsupported Egern rule type"):
        render(
            [{"type": "MATCH", "value": "DIRECT"}],
            tmp_path / "bad.yaml",
        )
