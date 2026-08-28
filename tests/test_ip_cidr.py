"""CIDR normalize / dedup contract tests."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ip_cidr import normalize_lines  # noqa: E402


def test_normalize_basic():
    out = normalize_lines(["1.2.3.0/24", "1.2.3.0/24", "# comment", ""])
    assert out.count("1.2.3.0/24") == 1


def test_normalize_strips_junk():
    out = normalize_lines(["not-a-cidr", "10.0.0.0/8"])
    assert "10.0.0.0/8" in out
    assert "not-a-cidr" not in out


def test_ipv6():
    out = normalize_lines(["2001:db8::/32"])
    assert any("2001:db8" in x.lower() for x in out)
