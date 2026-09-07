from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.engine.adapters.egern import render as render_egern
from src.engine.adapters.loon import render as render_loon
from src.engine.adapters.mihomo import render as render_mihomo
from src.engine.adapters.quantumultx import render as render_qx
from src.engine.adapters.shadowrocket import render as render_shadowrocket
from src.engine.adapters.surge import render as render_surge

RULES = [
    {"type": "DOMAIN", "value": "example.com"},
    {"type": "DOMAIN-SUFFIX", "value": "example.org"},
    {"type": "DOMAIN-KEYWORD", "value": "example"},
    {"type": "IP-CIDR", "value": "192.0.2.0/24"},
    {"type": "IP-CIDR6", "value": "2001:db8::/32"},
]


def test_mihomo_native_yaml(tmp_path: Path) -> None:
    out = tmp_path / "rules.yaml"
    render_mihomo(RULES, out)
    assert out.read_text(encoding="utf-8") == (
        "payload:\n"
        "  - DOMAIN,example.com\n"
        "  - DOMAIN-SUFFIX,example.org\n"
        "  - DOMAIN-KEYWORD,example\n"
        "  - IP-CIDR,192.0.2.0/24\n"
        "  - IP-CIDR6,2001:db8::/32\n"
    )


def test_surge_shadowrocket_loon_native_lists(tmp_path: Path) -> None:
    expected = [
        "DOMAIN,example.com",
        "DOMAIN-SUFFIX,example.org",
        "DOMAIN-KEYWORD,example",
        "IP-CIDR,192.0.2.0/24",
        "IP-CIDR6,2001:db8::/32",
        "",
    ]
    expected_text = "\n".join(expected)
    for name, renderer in (
        ("surge", render_surge),
        ("shadowrocket", render_shadowrocket),
        ("loon", render_loon),
    ):
        out = tmp_path / f"{name}.list"
        renderer(RULES, out)
        assert out.read_text(encoding="utf-8") == expected_text


def test_quantumult_x_uses_native_lowercase_filter_syntax(tmp_path: Path) -> None:
    out = tmp_path / "rules.list"
    render_qx(RULES, out)
    assert out.read_text(encoding="utf-8") == (
        "host, example.com, proxy\n"
        "host-suffix, example.org, proxy\n"
        "host-keyword, example, proxy\n"
        "ip-cidr, 192.0.2.0/24, proxy\n"
        "ip6-cidr, 2001:db8::/32, proxy\n"
    )


def test_client_specific_adapters_reject_unsupported_semantics(tmp_path: Path) -> None:
    unsupported = [{"type": "DOMAIN-REGEX", "value": r"^api\\.example\\.com$"}]
    for name, renderer in (
        ("surge", render_surge),
        ("shadowrocket", render_shadowrocket),
        ("quantumultx", render_qx),
        ("loon", render_loon),
    ):
        with pytest.raises(ValueError, match="Unsupported"):
            renderer(unsupported, tmp_path / f"{name}.list")


def test_egern_uses_native_rule_set_fields(tmp_path: Path) -> None:
    out = tmp_path / "rules.yaml"
    render_egern(
        RULES + [{"type": "DOMAIN-REGEX", "value": r"^api\\.example\\.com$"}],
        out,
    )
    text = out.read_text(encoding="utf-8")
    assert "domain_set:" in text
    assert "domain_suffix_set:" in text
    assert "domain_keyword_set:" in text
    assert "ip_cidr_set:" in text
    assert "ip_cidr6_set:" in text
    assert "domain_regex_set:" in text
    assert json.dumps(r"^api\\.example\\.com$", ensure_ascii=False) in text
