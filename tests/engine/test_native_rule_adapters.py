from pathlib import Path
import json

import pytest
import yaml

from src.engine.adapters import egern, mihomo, loon, quantumultx, shadowrocket, singbox, surge

RULES = [
    {"type": "DOMAIN", "value": "example.com"},
    {"type": "DOMAIN-SUFFIX", "value": "google.com"},
    {"type": "DOMAIN-KEYWORD", "value": "youtube"},
    {"type": "IP-CIDR", "value": "192.168.0.0/16"},
    {"type": "IP-CIDR6", "value": "2001:db8::/32"},
]


@pytest.mark.parametrize("adapter", [mihomo, surge, shadowrocket, loon])
def test_classical_adapters_normalize_rule_types(adapter, tmp_path: Path):
    out = adapter.render(RULES, tmp_path / "rules.list")
    lines = out.read_text(encoding="utf-8").splitlines()
    assert lines == [
        "DOMAIN,example.com",
        "DOMAIN-SUFFIX,google.com",
        "DOMAIN-KEYWORD,youtube",
        "IP-CIDR,192.168.0.0/16",
        "IP-CIDR6,2001:db8::/32",
    ]
    assert all("_" not in line.split(",", 1)[0] for line in lines)


def test_quantumultx_uses_native_filter_names(tmp_path: Path):
    out = quantumultx.render(RULES, tmp_path / "rules.list")
    assert out.read_text(encoding="utf-8").splitlines() == [
        "host,example.com",
        "host-suffix,google.com",
        "host-keyword,youtube",
        "ip-cidr,192.168.0.0/16",
        "ip6-cidr,2001:db8::/32",
    ]


def test_singbox_uses_native_headless_rule_set(tmp_path: Path):
    out = singbox.render(RULES, tmp_path / "rules.json")
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["version"] == 5
    assert payload["rules"] == [{
        "domain": ["example.com"],
        "domain_suffix": ["google.com"],
        "domain_keyword": ["youtube"],
        "ip_cidr": ["192.168.0.0/16", "2001:db8::/32"],
    }]


def test_egern_uses_native_rule_set_fields(tmp_path: Path):
    out = egern.render(RULES, tmp_path / "rules.yaml")
    payload = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert payload == {
        "domain_set": ["example.com"],
        "domain_suffix_set": ["google.com"],
        "domain_keyword_set": ["youtube"],
        "ip_cidr_set": ["192.168.0.0/16"],
        "ip_cidr6_set": ["2001:db8::/32"],
    }
    assert "payload" not in payload


def test_adapters_reject_unsupported_rule_types(tmp_path: Path):
    for adapter, filename in [
        (singbox, "rules.json"),
        (quantumultx, "rules.list"),
        (egern, "rules.yaml"),
    ]:
        with pytest.raises(ValueError):
            adapter.render([{"type": "MATCH", "value": "DIRECT"}], tmp_path / filename)
