from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.engine.adapters.singbox import render


def test_singbox_preserves_supported_rule_types(tmp_path: Path) -> None:
    output = tmp_path / "rules.json"
    render(
        [
            {"type": "DOMAIN", "value": "example.com"},
            {"type": "DOMAIN-SUFFIX", "value": "example.org"},
            {"type": "DOMAIN-KEYWORD", "value": "openai"},
            {"type": "DOMAIN-REGEX", "value": r"^api\\.example\\.com$"},
            {"type": "IP-CIDR", "value": "192.0.2.0/24"},
            {"type": "IP-CIDR6", "value": "2001:db8::/32"},
        ],
        output,
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["version"] == 2
    assert len(payload["rules"]) == 1
    rule = payload["rules"][0]
    assert rule["domain"] == ["example.com"]
    assert rule["domain_suffix"] == ["example.org"]
    assert rule["domain_keyword"] == ["openai"]
    assert rule["domain_regex"] == [r"^api\\.example\\.com$"]
    assert rule["ip_cidr"] == ["192.0.2.0/24", "2001:db8::/32"]


def test_singbox_rejects_unknown_rule_type(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported sing-box rule type"):
        render([{"type": "UNKNOWN", "value": "example.com"}], tmp_path / "rules.json")
