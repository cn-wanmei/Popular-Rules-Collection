"""Network dataset builder format smoke tests."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "bnd", ROOT / "scripts" / "build_network_datasets.py"
)
bnd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bnd)


def test_domain_to_clash(tmp_path):
    src = tmp_path / "d.txt"
    src.write_text("Example.COM\n# c\n", encoding="utf-8")
    dest = tmp_path / "out.list"
    n = bnd.domain_to_clash(src, dest)
    assert n == 1
    text = dest.read_text(encoding="utf-8")
    assert text.startswith("DOMAIN-SUFFIX,")


def test_cidr_to_clash(tmp_path):
    src = tmp_path / "c.txt"
    src.write_text("1.2.3.0/24\n2001:db8::/32\n", encoding="utf-8")
    dest = tmp_path / "out.list"
    n = bnd.cidr_to_clash(src, dest)
    assert n == 2
    text = dest.read_text(encoding="utf-8")
    assert "IP-CIDR,1.2.3.0/24" in text
    assert "IP-CIDR6," in text
