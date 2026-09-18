"""Phase 3.2–3.4 tests: Graph Engine, Closure Engine, Canonical Dedup.

Covers:
    - Dependency / Hierarchy / Aggregate graph construction
    - Unified cycle detector with path-formatted error
    - Full transitive dependency_closure / aggregate_closure
    - AssetKey types + normalize + dedup
"""
from __future__ import annotations

import textwrap
from pathlib import Path

import pytest
import yaml

from src.engine.ingest.v1_index import load_v1_index
from src.engine.v1.errors import CycleDetectedError
from src.engine.v1.graph import build_graphs
from src.engine.v1.closure import aggregate_closure, dependency_closure
from src.engine.v1.dedup import (
    CIDRAssetKey,
    DomainAssetKey,
    URLAssetKey,
    asset_key_for,
    dedup_records,
    normalize_record,
)


# ---------------------------------------------------------------------------
# Synthetic fixtures
# ---------------------------------------------------------------------------

def _make_index_repo(tmp_path: Path) -> Path:
    """A → B → C → D chain + one shared aggregate, no cycles."""
    rule_dir = tmp_path / "rule"
    rule_dir.mkdir(parents=True)

    index = {
        "categories": {
            "tech": {
                "display_name": "Tech",
                "order": 1,
                "rules": [
                    {"id": "A", "name": "A", "path": "rule/Tech/A",
                     "service_type": "service", "domains": 1, "ips": 0},
                    {"id": "B", "name": "B", "path": "rule/Tech/B",
                     "service_type": "service", "domains": 1, "ips": 0},
                    {"id": "C", "name": "C", "path": "rule/Tech/C",
                     "service_type": "service", "domains": 1, "ips": 0},
                    {"id": "D", "name": "D", "path": "rule/Tech/D",
                     "service_type": "service", "domains": 1, "ips": 0},
                    {"id": "root", "name": "Root", "path": "rule/Tech/Root",
                     "service_type": "aggregate", "domains": 0, "ips": 0},
                ],
            }
        }
    }
    (rule_dir / "_index.yaml").write_text(yaml.dump(index), encoding="utf-8")

    # Chain: A.parent=B, B.parent=C, C.parent=D, D.parent=root
    # root.children = [D]
    chain = [
        ("A", "B", False, []),
        ("B", "C", False, []),
        ("C", "D", False, []),
        ("D", "root", False, []),
        ("root", None, True, ["D"]),
    ]
    for sid, parent, is_agg, children in chain:
        d = rule_dir / "Tech" / sid
        d.mkdir(parents=True)
        meta = {
            "id": sid,
            "name": sid,
            "service_type": "aggregate" if is_agg else "service",
            "parent": parent,
            "children": children,
            "sources": [],
            "clients": ["Mihomo"],
            "rule": {"has_domain": True, "has_ip": False},
            "auto_generated": True,
        }
        (d / "metadata.yaml").write_text(yaml.dump(meta), encoding="utf-8")
        (d / f"{sid}.list").write_text(
            f"DOMAIN-SUFFIX,{sid.lower()}.example.com\n", encoding="utf-8"
        )

    return rule_dir


def _make_cycle_repo(tmp_path: Path) -> Path:
    """google/core ↔ shared/network cycle via parent fields."""
    rule_dir = tmp_path / "rule"
    rule_dir.mkdir(parents=True)

    index = {
        "categories": {
            "google": {
                "display_name": "Google",
                "order": 1,
                "rules": [
                    {"id": "google/core", "name": "Google Core",
                     "path": "rule/Google/Core", "service_type": "service",
                     "domains": 1, "ips": 0},
                    {"id": "shared/network", "name": "Shared Network",
                     "path": "rule/Shared/Network", "service_type": "service",
                     "domains": 1, "ips": 0},
                ],
            }
        }
    }
    (rule_dir / "_index.yaml").write_text(yaml.dump(index), encoding="utf-8")

    # google/core.parent = shared/network
    # shared/network.parent = google/core  → cycle
    for sid, parent, path_parts in [
        ("google/core", "shared/network", ("Google", "Core")),
        ("shared/network", "google/core", ("Shared", "Network")),
    ]:
        d = rule_dir.joinpath(*path_parts)
        d.mkdir(parents=True)
        meta = {
            "id": sid,
            "name": sid,
            "service_type": "service",
            "parent": parent,
            "children": [],
            "sources": [],
            "clients": ["Mihomo"],
            "rule": {"has_domain": True, "has_ip": False},
            "auto_generated": True,
        }
        (d / "metadata.yaml").write_text(yaml.dump(meta), encoding="utf-8")
        (d / f"{path_parts[-1]}.list").write_text(
            f"DOMAIN-SUFFIX,{sid.replace('/', '.')}.com\n", encoding="utf-8"
        )

    return rule_dir


# ===========================================================================
# 3.2 Graph Engine
# ===========================================================================

class TestGraphEngine:
    def test_build_graphs_chain(self, tmp_path):
        rule_dir = _make_index_repo(tmp_path)
        index = load_v1_index(rule_dir)
        bundle = build_graphs(index)

        assert "A" in bundle.entry_ids
        assert "root" in bundle.entry_ids

        # Dependency: A → B → C → D → root
        assert bundle.dependency.graph.has_edge("A", "B")
        assert bundle.dependency.graph.has_edge("B", "C")
        assert bundle.dependency.graph.has_edge("C", "D")
        assert bundle.dependency.graph.has_edge("D", "root")

        # Hierarchy / Aggregate: root → D → C → B → A (parent → child)
        assert bundle.hierarchy.graph.has_edge("B", "A")
        assert bundle.hierarchy.graph.has_edge("C", "B")
        assert bundle.hierarchy.graph.has_edge("D", "C")
        assert bundle.hierarchy.graph.has_edge("root", "D")
        assert bundle.aggregate.graph.has_edge("root", "D")

    def test_cycle_error_format(self, tmp_path):
        rule_dir = _make_cycle_repo(tmp_path)
        index = load_v1_index(rule_dir)

        with pytest.raises(CycleDetectedError) as exc_info:
            build_graphs(index, raise_on_cycle=True)

        msg = str(exc_info.value)
        assert "cycle detected:" in msg
        # Must show path with arrows, not a bare "cycle detected"
        assert "→" in msg
        assert "google/core" in msg
        assert "shared/network" in msg

    def test_cycle_kind_prefix(self, tmp_path):
        rule_dir = _make_cycle_repo(tmp_path)
        index = load_v1_index(rule_dir)

        with pytest.raises(CycleDetectedError) as exc_info:
            build_graphs(index)

        # First graph checked is Dependency
        assert exc_info.value.kind == "Dependency"
        assert msg_starts_with_kind(str(exc_info.value))

    def test_no_cycle_when_disabled(self, tmp_path):
        rule_dir = _make_cycle_repo(tmp_path)
        index = load_v1_index(rule_dir)
        # Should not raise
        bundle = build_graphs(index, raise_on_cycle=False)
        assert "google/core" in bundle.entry_ids


def msg_starts_with_kind(msg: str) -> bool:
    return msg.startswith("Dependency cycle detected:") or msg.startswith(
        "Hierarchy cycle detected:"
    ) or msg.startswith("Aggregate cycle detected:")


# ===========================================================================
# 3.3 Closure Engine
# ===========================================================================

class TestClosureEngine:
    def test_dependency_closure_full_chain(self, tmp_path):
        rule_dir = _make_index_repo(tmp_path)
        index = load_v1_index(rule_dir)
        bundle = build_graphs(index)

        # A depends on B → C → D → root
        closure = dependency_closure(bundle, "A")
        assert closure == frozenset({"A", "B", "C", "D", "root"})

    def test_dependency_closure_mid_chain(self, tmp_path):
        rule_dir = _make_index_repo(tmp_path)
        index = load_v1_index(rule_dir)
        bundle = build_graphs(index)

        closure = dependency_closure(bundle, "C")
        assert closure == frozenset({"C", "D", "root"})
        assert "A" not in closure
        assert "B" not in closure

    def test_aggregate_closure_full_tree(self, tmp_path):
        rule_dir = _make_index_repo(tmp_path)
        index = load_v1_index(rule_dir)
        bundle = build_graphs(index)

        # root includes D → C → B → A (via hierarchy edges)
        closure = aggregate_closure(bundle, "root")
        assert closure == frozenset({"root", "D", "C", "B", "A"})

    def test_aggregate_closure_not_shallow(self, tmp_path):
        """Must NOT stop at one hop (A+B only)."""
        rule_dir = _make_index_repo(tmp_path)
        index = load_v1_index(rule_dir)
        bundle = build_graphs(index)

        closure = aggregate_closure(bundle, "D")
        # D → C → B → A
        assert "A" in closure
        assert "B" in closure
        assert "C" in closure
        assert "D" in closure
        assert len(closure) == 4

    def test_closure_accepts_iterable(self, tmp_path):
        rule_dir = _make_index_repo(tmp_path)
        index = load_v1_index(rule_dir)
        bundle = build_graphs(index)

        dep = dependency_closure(bundle, ["A", "C"])
        assert "root" in dep
        assert "B" in dep


# ===========================================================================
# 3.4 Canonical Dedup
# ===========================================================================

class TestCanonicalDedup:
    def test_domain_asset_key_normalize(self):
        k1 = DomainAssetKey("Example.COM.")
        k2 = DomainAssetKey("example.com")
        assert k1.value == "example.com"
        assert k1.identity() == k2.identity()

    def test_cidr_asset_key(self):
        k = CIDRAssetKey(" 10.0.0.0/8 ")
        assert k.value == "10.0.0.0/8"
        assert k.kind == "cidr"

    def test_url_asset_key(self):
        k = URLAssetKey(" https://example.com/path ")
        assert k.value == "https://example.com/path"
        assert k.kind == "url"

    def test_normalize_record(self):
        rec = {"type": "DOMAIN-SUFFIX", "value": "Foo.Bar.COM.", "service": "x"}
        out = normalize_record(rec)
        assert out["type"] == "domain_suffix"
        assert out["value"] == "foo.bar.com"

    def test_asset_key_for_domain(self):
        rec = normalize_record({"type": "domain_suffix", "value": "a.com"})
        key = asset_key_for(rec)
        assert isinstance(key, DomainAssetKey)
        assert "domain" in key.kind

    def test_asset_key_for_cidr(self):
        rec = normalize_record({"type": "ip_cidr", "value": "1.2.3.0/24"})
        key = asset_key_for(rec)
        assert isinstance(key, CIDRAssetKey)

    def test_dedup_removes_duplicates(self):
        records = [
            {"service": "A", "type": "domain_suffix", "value": "example.com"},
            {"service": "B", "type": "DOMAIN-SUFFIX", "value": "Example.COM."},
            {"service": "C", "type": "ip_cidr", "value": "10.0.0.0/8"},
            {"service": "D", "type": "ip_cidr", "value": "10.0.0.0/8"},
        ]
        out = dedup_records(records)
        assert len(out) == 2
        keys = {r["asset_key"] for r in out}
        assert any("example.com" in k for k in keys)
        assert any("10.0.0.0/8" in k for k in keys)

    def test_dedup_preserves_order_of_first_seen(self):
        records = [
            {"service": "A", "type": "domain", "value": "a.com"},
            {"service": "B", "type": "domain", "value": "b.com"},
            {"service": "C", "type": "domain", "value": "a.com"},
        ]
        out = dedup_records(records)
        assert len(out) == 2
        assert out[0]["value"] == "a.com"
        assert out[0]["service"] == "A"
        assert out[1]["value"] == "b.com"

    def test_dedup_prefer_service(self):
        records = [
            {"service": "A", "type": "domain", "value": "x.com"},
            {"service": "preferred", "type": "domain", "value": "x.com"},
        ]
        out = dedup_records(records, prefer_service="preferred")
        assert len(out) == 1
        assert out[0]["service"] == "preferred"

    def test_end_to_end_pipeline_shape(self, tmp_path):
        """Service → dep closure → agg closure → normalize → dedup."""
        rule_dir = _make_index_repo(tmp_path)
        index = load_v1_index(rule_dir)
        bundle = build_graphs(index)

        # Pick root aggregate closure
        members = aggregate_closure(bundle, "root")
        assert members == frozenset({"root", "D", "C", "B", "A"})

        # Simulate records from those services
        raw = [
            {"service": sid, "type": "domain_suffix", "value": f"{sid.lower()}.example.com"}
            for sid in sorted(members)
        ]
        # Inject intentional duplicate
        raw.append(
            {"service": "A", "type": "DOMAIN-SUFFIX", "value": "a.example.com."}
        )

        deduped = dedup_records(raw)
        # 5 unique domains (one per service) after dedup of the extra A duplicate
        assert len(deduped) == 5
        assert all("asset_key" in r and "asset_digest" in r for r in deduped)
