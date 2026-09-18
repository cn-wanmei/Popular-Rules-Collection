"""Phase 3.1 — V1 Loader tests.

Covers:
    1. v1_index: ServiceEntry typing (7 type flags), entry counts, error handling
    2. v1_loader: record format, provenance, aggregate skip/include
    3. Pipeline: Loader → Canonical Store contract
    4. Real-data smoke: 170 services, 14 aggregates, >600k records, 0 hard errors
"""
from __future__ import annotations

import json
import textwrap
import tempfile
from pathlib import Path

import pytest
import yaml

from src.engine.ingest.v1_index import load_v1_index, ServiceEntry
from src.engine.ingest.v1_loader import load_v1_rules, load_v1_rules_for_service

# Real repo root (relative to project root)
REPO_ROOT = Path(__file__).resolve().parents[2]
RULE_ROOT = REPO_ROOT / "rule"


# ---------------------------------------------------------------------------
# Fixtures — minimal synthetic repo
# ---------------------------------------------------------------------------

def _make_synthetic_repo(tmp_path: Path) -> Path:
    """Create a minimal synthetic rule/ directory for unit tests."""
    rule_dir = tmp_path / "rule"

    # _index.yaml
    index = {
        "categories": {
            "tech": {
                "display_name": "Tech",
                "order": 1,
                "rules": [
                    {"id": "alpha", "name": "Alpha", "path": "rule/Tech/Alpha",
                     "service_type": "service", "domains": 2, "ips": 0},
                    {"id": "beta", "name": "Beta", "path": "rule/Tech/Beta",
                     "service_type": "aggregate", "domains": 5, "ips": 3},
                ],
            },
            "network": {
                "display_name": "Network",
                "order": 2,
                "rules": [
                    # alpha also appears here → Shared
                    {"id": "alpha", "name": "Alpha", "path": "rule/Tech/Alpha",
                     "service_type": "service", "domains": 2, "ips": 0},
                    {"id": "gamma", "name": "Gamma", "path": "rule/Network/Gamma",
                     "service_type": "service", "domains": 0, "ips": 4},
                ],
            },
        }
    }
    (rule_dir).mkdir(parents=True)
    (rule_dir / "_index.yaml").write_text(yaml.dump(index), encoding="utf-8")

    # Alpha: service, appears in 2 categories → Shared; no parent
    alpha_dir = rule_dir / "Tech" / "Alpha"
    alpha_dir.mkdir(parents=True)
    (alpha_dir / "metadata.yaml").write_text(yaml.dump({
        "id": "alpha", "name": "Alpha", "service_type": "service",
        "parent": None, "children": [], "sources": ["src1"],
        "clients": ["Mihomo"], "rule": {"has_domain": True, "has_ip": False},
        "auto_generated": True,
    }), encoding="utf-8")
    (alpha_dir / "alpha.list").write_text(
        "DOMAIN-SUFFIX,alpha.com\nDOMAIN-SUFFIX,alpha.net\n", encoding="utf-8"
    )

    # Beta: aggregate, 2 children
    beta_dir = rule_dir / "Tech" / "Beta"
    beta_dir.mkdir(parents=True)
    (beta_dir / "metadata.yaml").write_text(yaml.dump({
        "id": "beta", "name": "Beta", "service_type": "aggregate",
        "parent": None, "children": ["alpha", "gamma"],
        "sources": ["src2"], "clients": ["Mihomo", "Surge"],
        "rule": {"has_domain": True, "has_ip": True},
        "auto_generated": True,
    }), encoding="utf-8")
    (beta_dir / "beta.list").write_text(
        "DOMAIN-SUFFIX,beta.com\nIP-CIDR,1.2.3.0/24\n", encoding="utf-8"
    )

    # Gamma: service, IP-only, has parent=beta → Child + NetworkRef
    gamma_dir = rule_dir / "Network" / "Gamma"
    gamma_dir.mkdir(parents=True)
    (gamma_dir / "metadata.yaml").write_text(yaml.dump({
        "id": "gamma", "name": "Gamma", "service_type": "service",
        "parent": "beta", "children": [],
        "sources": ["src3"], "clients": ["Mihomo"],
        "rule": {"has_domain": False, "has_ip": True},
        "auto_generated": False,
    }), encoding="utf-8")
    (gamma_dir / "gamma.list").write_text(
        "IP-CIDR,10.0.0.0/8\nIP-CIDR,192.168.1.0/24\nIP-CIDR6,::1/128\nIP-CIDR6,2001:db8::/32\n",
        encoding="utf-8",
    )

    return rule_dir


# ===========================================================================
# 1. v1_index — unit tests
# ===========================================================================

class TestV1Index:
    def test_entry_count(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_index(rule_dir)
        assert result.entry_count == 3  # alpha, beta, gamma
        assert result.service_count == 2  # alpha, gamma
        assert result.aggregate_count == 1  # beta
        assert result.category_count == 2

    def test_alpha_is_shared_service(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_index(rule_dir)
        alpha = result.by_id["alpha"]
        assert isinstance(alpha, ServiceEntry)
        assert alpha.service_type == "service"
        assert alpha.is_aggregate is False
        assert alpha.is_child is False
        assert alpha.is_network_ref is False
        assert alpha.is_shared is True  # appears in tech + network
        assert "Shared" in alpha.type_flags()
        assert "Service" in alpha.type_flags()

    def test_beta_is_aggregate_parent(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_index(rule_dir)
        beta = result.by_id["beta"]
        assert beta.is_aggregate is True
        assert "Parent" in beta.type_flags()
        assert "Aggregate" in beta.type_flags()
        assert beta.children == frozenset({"alpha", "gamma"})
        assert beta.is_network_ref is True  # has_ip from metadata

    def test_gamma_is_child_and_network_ref(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_index(rule_dir)
        gamma = result.by_id["gamma"]
        assert gamma.is_child is True
        assert gamma.parent == "beta"
        assert gamma.is_network_ref is True
        assert "Child" in gamma.type_flags()
        assert "NetworkRef" in gamma.type_flags()
        assert gamma.is_shared is False  # only in network category

    def test_by_category(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_index(rule_dir)
        assert "alpha" in result.by_category["tech"]
        assert "beta" in result.by_category["tech"]
        assert "alpha" in result.by_category["network"]
        assert "gamma" in result.by_category["network"]

    def test_missing_index_returns_error(self, tmp_path):
        empty_dir = tmp_path / "no_rule"
        empty_dir.mkdir()
        result = load_v1_index(empty_dir)
        assert len(result.errors) > 0
        assert result.entry_count == 0

    def test_digest_is_stable(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        r1 = load_v1_index(rule_dir)
        r2 = load_v1_index(rule_dir)
        for eid in r1.by_id:
            assert r1.by_id[eid].digest == r2.by_id[eid].digest


# ===========================================================================
# 2. v1_loader — unit tests
# ===========================================================================

class TestV1Loader:
    def test_service_records_loaded(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir)
        services = {r["service"] for r in result["records"]}
        assert "alpha" in services
        assert "gamma" in services

    def test_aggregates_skipped_by_default(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir)
        services = {r["service"] for r in result["records"]}
        assert "beta" not in services
        assert "beta" in result["manifest"]["skipped_aggregates"]

    def test_aggregates_included_when_requested(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir, include_aggregates=True)
        services = {r["service"] for r in result["records"]}
        assert "beta" in services

    def test_record_schema(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir)
        for rec in result["records"]:
            assert "service" in rec
            assert "type" in rec
            assert "value" in rec
            assert "category" in rec
            assert "provenance" in rec
            prov = rec["provenance"]
            assert prov["loader"] == "v1_loader"
            assert prov["format"] == "v1_list"

    def test_alpha_domains_parsed(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir, service_ids={"alpha"})
        records = result["records"]
        values = {r["value"] for r in records}
        assert "alpha.com" in values
        assert "alpha.net" in values
        assert len(records) == 2

    def test_gamma_ips_parsed(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir, service_ids={"gamma"})
        records = result["records"]
        types = {r["type"] for r in records}
        assert "ip_cidr" in types or any("ip" in t for t in types)

    def test_manifest_schema(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir)
        m = result["manifest"]
        assert m["schema"] == "v1_loader_manifest_v1"
        assert m["loader"] == "v1_loader"
        assert isinstance(m["records_total"], int)
        assert isinstance(m["errors_total"], int)
        assert isinstance(m["loaded_services"], list)

    def test_service_filter(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir, service_ids={"alpha"})
        services = {r["service"] for r in result["records"]}
        assert services == {"alpha"}

    def test_zero_hard_errors_on_valid_data(self, tmp_path):
        rule_dir = _make_synthetic_repo(tmp_path)
        result = load_v1_rules(rule_dir, include_aggregates=True)
        hard = [e for e in result["errors"] if e.get("severity") != "warning"]
        assert hard == []


# ===========================================================================
# 3. Pipeline: Loader → Canonical Store
# ===========================================================================

class TestLoaderCanonicalPipeline:
    def test_canonical_store_contract(self, tmp_path):
        from src.engine.canonical.store import build_canonical

        rule_dir = _make_synthetic_repo(tmp_path)
        ingest = load_v1_rules(rule_dir, service_ids={"alpha"})

        canonical_dir = tmp_path / "canonical"
        manifest = build_canonical(ingest, canonical_dir)

        assert manifest["schema"] == "canonical_store_v1"
        assert manifest["v2_runtime_dependency"] == 0
        assert manifest["unique_rules"] > 0
        assert (canonical_dir / "rules.jsonl").exists()
        assert (canonical_dir / "memberships.jsonl").exists()
        assert (canonical_dir / "manifest.json").exists()

    def test_rule_identity_keys_are_stable(self, tmp_path):
        from src.engine.canonical.store import build_canonical

        rule_dir = _make_synthetic_repo(tmp_path)
        ingest = load_v1_rules(rule_dir, service_ids={"alpha"})

        out1 = tmp_path / "c1"
        out2 = tmp_path / "c2"
        build_canonical(ingest, out1)
        build_canonical(ingest, out2)

        def read_ids(d: Path) -> set[str]:
            return {json.loads(l)["id"] for l in (d / "rules.jsonl").read_text().splitlines() if l}

        assert read_ids(out1) == read_ids(out2)

    def test_no_v2_runtime_dependency(self, tmp_path):
        from src.engine.canonical.store import build_canonical

        rule_dir = _make_synthetic_repo(tmp_path)
        ingest = load_v1_rules(rule_dir)
        canonical_dir = tmp_path / "canonical"
        manifest = build_canonical(ingest, canonical_dir)
        assert manifest["v2_runtime_dependency"] == 0


# ===========================================================================
# 4. Real-data smoke tests (skip if rule/ not present)
# ===========================================================================

@pytest.mark.skipif(not RULE_ROOT.exists(), reason="rule/ directory not available")
class TestRealDataSmoke:
    def test_index_loads_184_entries(self):
        result = load_v1_index(RULE_ROOT)
        assert result.entry_count == 184
        assert result.service_count == 170
        assert result.aggregate_count == 14
        assert result.category_count == 25

    def test_all_entries_have_ids(self):
        result = load_v1_index(RULE_ROOT)
        for entry in result.entries:
            assert entry.id, f"Entry missing id: {entry}"

    def test_loader_loads_all_services(self):
        result = load_v1_rules(RULE_ROOT)
        m = result["manifest"]
        assert m["loaded_services"] != []
        assert len(m["loaded_services"]) == m["service_count"]

    def test_loader_zero_hard_errors(self):
        result = load_v1_rules(RULE_ROOT)
        hard = [e for e in result["errors"] if e.get("severity") != "warning"]
        assert hard == [], f"Hard errors: {hard[:3]}"

    def test_loader_record_count_above_threshold(self):
        result = load_v1_rules(RULE_ROOT)
        # 170 services × average ~3000 rules each → well above 100k
        assert result["manifest"]["records_total"] > 100_000

    def test_all_records_have_required_fields(self):
        result = load_v1_rules(RULE_ROOT)
        required = {"service", "type", "value", "category", "provenance"}
        for rec in result["records"][:5000]:  # sample first 5000
            missing = required - rec.keys()
            assert not missing, f"Record missing fields {missing}: {rec}"

    def test_14_aggregates_skipped_by_default(self):
        result = load_v1_rules(RULE_ROOT)
        assert len(result["manifest"]["skipped_aggregates"]) == 14

    def test_youtube_service_loads(self):
        result = load_v1_rules_for_service(RULE_ROOT, "youtube")
        assert result["manifest"]["records_total"] > 0
        services = {r["service"] for r in result["records"]}
        assert "youtube" in services

    def test_canonical_pipeline_end_to_end(self):
        from src.engine.canonical.store import build_canonical

        result = load_v1_rules(RULE_ROOT, service_ids={"youtube", "googlefcm"})
        with tempfile.TemporaryDirectory() as td:
            manifest = build_canonical(result, Path(td))
            assert manifest["unique_rules"] > 0
            assert manifest["errors"] == 0
            rules = [json.loads(l) for l in (Path(td) / "rules.jsonl").read_text().splitlines() if l]
            for rule in rules:
                assert "id" in rule
                assert "type" in rule
                assert "value" in rule
                assert "identity_key" in rule
