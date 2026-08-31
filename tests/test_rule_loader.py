"""Canonical contract tests for rule_loader (V3: src.adapters._common.rule_loader)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.adapters._common import rule_loader  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def _patch_paths(monkeypatch, fixture_name: str) -> Path:
    base = FIXTURES / fixture_name
    # Patch the module that owns load_service_rules globals (not scripts/ shim)
    monkeypatch.setattr(rule_loader, "ROOT", base)
    monkeypatch.setattr(rule_loader, "SERVICES", base / "database" / "services")
    monkeypatch.setattr(rule_loader, "DOMAINS", base / "database" / "domains")
    monkeypatch.setattr(rule_loader, "IPS", base / "database" / "ips")
    return base


def test_yaml_domain_only(monkeypatch):
    _patch_paths(monkeypatch, "svc_domain")
    buckets = rule_loader.load_service_rules("demo")
    assert len(buckets) == 1
    b = buckets[0]
    assert b["domain"] == ["example.com"]
    assert b["domain_suffix"] == []


def test_domains_txt_as_suffix_and_casefold_dedup(monkeypatch):
    _patch_paths(monkeypatch, "svc_domains_txt")
    buckets = rule_loader.load_service_rules("demo")
    assert len(buckets) == 1
    b = buckets[0]
    assert len(b["domain_suffix"]) == 1
    assert b["domain_suffix"][0].lower() == "example.com"
    assert sum(len(b[k]) for k in rule_loader.TYPED_KEYS) > 0


def test_domain_and_domain_suffix_are_distinct(monkeypatch):
    _patch_paths(monkeypatch, "svc_mixed")
    buckets = rule_loader.load_service_rules("demo")
    b = buckets[0]
    assert "example.com" in b["domain"]
    assert "example.com" in b["domain_suffix"]
    assert len(b["domain"]) >= 1
    assert len(b["domain_suffix"]) >= 1


def test_ipv4_and_ipv6_buckets(monkeypatch):
    _patch_paths(monkeypatch, "svc_mixed")
    b = rule_loader.load_service_rules("demo")[0]
    assert "1.2.3.4/32" in b["ip_cidr"]
    assert "2001:db8::/32" in b["ip_cidr6"]


def test_empty_yaml_plus_domains_txt_not_omitted(monkeypatch):
    """Regression: adblock-class services with domains.txt only must load."""
    _patch_paths(monkeypatch, "svc_domains_txt")
    buckets = rule_loader.load_service_rules("demo")
    assert len(buckets) == 1
    total = sum(len(buckets[0][k]) for k in rule_loader.TYPED_KEYS)
    assert total > 0


def test_fully_empty_service_omitted(monkeypatch):
    _patch_paths(monkeypatch, "svc_empty")
    buckets = rule_loader.load_service_rules("empty")
    assert buckets == []


def test_keyword_only_service_kept(monkeypatch):
    _patch_paths(monkeypatch, "svc_keyword")
    buckets = rule_loader.load_service_rules("kw")
    assert len(buckets) == 1
    assert buckets[0]["domain_keyword"] == ["stripe"]
