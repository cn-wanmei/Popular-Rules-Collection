from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_semantic_mod():
    spec = importlib.util.spec_from_file_location(
        "cross_client_semantic_test",
        ROOT / "scripts" / "cross_client_semantic_test.py",
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_extract_lines_reads_quantumult_x_native_syntax(tmp_path: Path) -> None:
    semantic = _load_semantic_mod()
    path = tmp_path / "github.list"
    path.write_text(
        "host, github.com, proxy\n"
        "host-suffix, github.io, proxy\n"
        "host-keyword, github, proxy\n"
        "ip-cidr, 192.0.2.0/24, proxy\n"
        "ip6-cidr, 2001:db8::/32, proxy\n",
        encoding="utf-8",
    )
    assert semantic._extract_lines(path) == {
        ("domain", "github.com"),
        ("domain_suffix", "github.io"),
        ("domain_keyword", "github"),
        ("ip_cidr", "192.0.2.0/24"),
        ("ip_cidr6", "2001:db8::/32"),
    }


def test_extract_lines_still_reads_surge_and_underscore_variants(tmp_path: Path) -> None:
    semantic = _load_semantic_mod()
    path = tmp_path / "surge.list"
    path.write_text(
        "DOMAIN,example.com\n"
        "DOMAIN_SUFFIX,example.org\n"
        "IP-CIDR,192.0.2.0/24\n"
        "IP-CIDR6,2001:db8::/32\n",
        encoding="utf-8",
    )
    assert semantic._extract_lines(path) == {
        ("domain", "example.com"),
        ("domain_suffix", "example.org"),
        ("ip_cidr", "192.0.2.0/24"),
        ("ip_cidr6", "2001:db8::/32"),
    }


def test_semantic_script_passes_native_artifacts_after_capability_projection(
    tmp_path: Path, monkeypatch
) -> None:
    from src.engine.adapters.build_all import build_all_clients

    ir_dir = tmp_path / "ir"
    artifacts = tmp_path / "artifacts"
    ir_dir.mkdir()
    ir = {
        "schema": "semantic_ir_v2",
        "v2_runtime_dependency": 0,
        "rules": [
            {"id": "d1", "type": "DOMAIN", "value": "example.com"},
            {"id": "s1", "type": "DOMAIN-SUFFIX", "value": "example.org"},
            {"id": "k1", "type": "DOMAIN-KEYWORD", "value": "example"},
            {"id": "r1", "type": "DOMAIN-REGEX", "value": r"^api\\.example\\.com$"},
            {"id": "ip4", "type": "IP-CIDR", "value": "192.0.2.0/24"},
            {"id": "ip6", "type": "IP-CIDR6", "value": "2001:db8::/32"},
        ],
        "memberships": {"demo": ["d1", "s1", "k1", "r1", "ip4", "ip6"]},
        "entities": {"services": ["demo"]},
    }
    (ir_dir / "ir.json").write_text(json.dumps(ir), encoding="utf-8")
    build_all_clients(ir_dir, artifacts)

    semantic = _load_semantic_mod()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cross_client_semantic_test.py",
            "--ir",
            str(ir_dir / "ir.json"),
            "--generated",
            str(artifacts),
            "--matrix",
            str(ROOT / "config" / "client_capability_matrix.yaml"),
        ],
    )
    assert semantic.main() == 0
