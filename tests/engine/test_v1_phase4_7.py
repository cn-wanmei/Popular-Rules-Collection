"""Phase 4–7 tests: Golden / Client Regression / Deterministic / Legacy Regression."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from src.engine.v1.golden import GOLDEN_SERVICE_IDS, run_v1_golden
from src.engine.v1.client_regression import CLIENTS, run_client_regression
from src.engine.v1.deterministic import compare_builds, digest_run, run_deterministic_builds
from src.engine.v1.legacy_regression import (
    compare_legacy_to_v1,
    load_assets_from_records,
    run_legacy_regression,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_golden_repo(tmp_path: Path) -> Path:
    """Synthetic rule/ covering Parent/Child/Aggregate/Domain/Shared."""
    rule_dir = tmp_path / "rule"
    rule_dir.mkdir(parents=True)

    index = {
        "categories": {
            "tech": {
                "display_name": "Tech",
                "order": 1,
                "rules": [
                    {"id": "Google", "name": "Google", "path": "rule/Tech/Google",
                     "service_type": "aggregate", "domains": 0, "ips": 0},
                    {"id": "YouTube", "name": "YouTube", "path": "rule/Tech/YouTube",
                     "service_type": "service", "domains": 2, "ips": 0},
                    {"id": "GitHub", "name": "GitHub", "path": "rule/Tech/GitHub",
                     "service_type": "service", "domains": 1, "ips": 0},
                ],
            },
            "media": {
                "display_name": "Media",
                "order": 2,
                "rules": [
                    # YouTube also here → Shared / Multi-category
                    {"id": "YouTube", "name": "YouTube", "path": "rule/Tech/YouTube",
                     "service_type": "service", "domains": 2, "ips": 0},
                    {"id": "Netflix", "name": "Netflix", "path": "rule/Media/Netflix",
                     "service_type": "service", "domains": 1, "ips": 0},
                ],
            },
        }
    }
    (rule_dir / "_index.yaml").write_text(yaml.dump(index), encoding="utf-8")

    services = [
        ("Google", None, True, ["YouTube"], "Tech/Google"),
        ("YouTube", "Google", False, [], "Tech/YouTube"),
        ("GitHub", None, False, [], "Tech/GitHub"),
        ("Netflix", None, False, [], "Media/Netflix"),
    ]
    for sid, parent, is_agg, children, rel in services:
        d = rule_dir / Path(rel)
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


def _make_run_dir(tmp_path: Path) -> Path:
    """Minimal fake V3 run dir with 7 client artifact stubs."""
    run = tmp_path / "run"
    art = run / "artifacts"
    for client, ext in [
        ("mihomo", ".yaml"),
        ("singbox", ".json"),
        ("surge", ".list"),
        ("shadowrocket", ".list"),
        ("quantumultx", ".list"),
        ("egern", ".yaml"),
        ("loon", ".list"),
    ]:
        d = art / client / "Google"
        d.mkdir(parents=True)
        body = (
            "DOMAIN-SUFFIX,google.com\n"
            "DOMAIN-KEYWORD,gmail\n"
            "IP-CIDR,8.8.8.0/24\n"
            "URL-REGEX,^https://youtube\n"
            "# aggregate Google\n"
        )
        if ext == ".json":
            body = json.dumps(
                {
                    "rules": [
                        {"domain_suffix": ["google.com"]},
                        {"domain_keyword": ["gmail"]},
                        {"ip_cidr": ["8.8.8.0/24"]},
                    ]
                }
            )
        elif ext == ".yaml":
            body = (
                "payload:\n"
                "  - DOMAIN-SUFFIX,google.com\n"
                "  - DOMAIN-KEYWORD,gmail\n"
                "  - IP-CIDR,8.8.8.0/24\n"
                "  - URL-REGEX,^https://youtube\n"
                "# aggregate Google\n"
            )
        (d / f"rules{ext}").write_text(body, encoding="utf-8")

    (run / "canonical").mkdir(parents=True)
    (run / "canonical" / "rules.jsonl").write_text(
        json.dumps({"id": "r1", "type": "domain_suffix", "value": "google.com"}) + "\n",
        encoding="utf-8",
    )
    (run / "canonical" / "memberships.jsonl").write_text(
        json.dumps({"service": "Google", "rule_ids": ["r1"]}) + "\n",
        encoding="utf-8",
    )
    (run / "ir").mkdir(parents=True)
    (run / "ir" / "ir.json").write_text(
        json.dumps({"schema": "semantic_ir_v2", "entities": {"services": ["Google"]}, "decisions": [1]}),
        encoding="utf-8",
    )
    (run / "hierarchy").mkdir(parents=True)
    (run / "hierarchy" / "graph.json").write_text(
        json.dumps({"services": {"Google": {"rule_count": 1}}}),
        encoding="utf-8",
    )
    return run


# ===========================================================================
# Phase 4 — Golden
# ===========================================================================

class TestPhase4Golden:
    def test_golden_ids_defined(self):
        assert "Google" in GOLDEN_SERVICE_IDS
        assert "YouTube" in GOLDEN_SERVICE_IDS
        assert len(GOLDEN_SERVICE_IDS) >= 10

    def test_golden_matches_synthetic(self, tmp_path):
        rule_dir = _make_golden_repo(tmp_path)
        report = run_v1_golden(rule_dir)
        d = report.to_dict()
        assert d["schema"] == "v1_golden_v1"
        matched_stems = {m["golden_id"] for m in d["matched"] if m["matched_entry_ids"]}
        assert "Google" in matched_stems
        assert "YouTube" in matched_stems
        assert report.graph_ok is True
        assert d["coverage"]["Parent"] is True
        assert d["coverage"]["Child"] is True
        assert d["coverage"]["Aggregate"] is True
        assert d["coverage"]["Shared"] is True
        assert report.coverage_pass is True

    def test_golden_unmatched_reported(self, tmp_path):
        rule_dir = _make_golden_repo(tmp_path)
        report = run_v1_golden(rule_dir, golden_ids=["Google", "NonExistentXYZ"])
        assert "NonExistentXYZ" in report.unmatched


# ===========================================================================
# Phase 5 — Client Regression
# ===========================================================================

class TestPhase5ClientRegression:
    def test_all_seven_clients_listed(self):
        assert len(CLIENTS) == 7
        assert "mihomo" in CLIENTS
        assert "loon" in CLIENTS

    def test_client_artifacts_detected(self, tmp_path):
        run = _make_run_dir(tmp_path)
        report = run_client_regression(run)
        d = report.to_dict()
        assert d["schema"] == "v1_client_regression_v1"
        for client in CLIENTS:
            assert report.client_artifacts_ok[client] is True
        assert d["all_pass"] is True

    def test_missing_artifacts_fail(self, tmp_path):
        run = tmp_path / "empty_run"
        run.mkdir()
        report = run_client_regression(run)
        assert report.to_dict()["all_pass"] is False
        assert report.errors


# ===========================================================================
# Phase 6 — Deterministic Build
# ===========================================================================

class TestPhase6Deterministic:
    def test_identical_builds_match(self, tmp_path):
        def build_fn(out: Path) -> None:
            (out / "canonical").mkdir(parents=True, exist_ok=True)
            (out / "canonical" / "rules.jsonl").write_text(
                json.dumps({"id": "a", "value": "x.com", "type": "domain"}) + "\n"
                + json.dumps({"id": "b", "value": "y.com", "type": "domain"}) + "\n",
                encoding="utf-8",
            )
            (out / "ir").mkdir(parents=True, exist_ok=True)
            (out / "ir" / "ir.json").write_text(
                json.dumps({"schema": "semantic_ir_v2", "entities": {}, "decisions": []}),
                encoding="utf-8",
            )
            (out / "hierarchy").mkdir(parents=True, exist_ok=True)
            (out / "hierarchy" / "graph.json").write_text("{}", encoding="utf-8")
            art = out / "artifacts" / "mihomo"
            art.mkdir(parents=True, exist_ok=True)
            (art / "rules.yaml").write_text("DOMAIN-SUFFIX,x.com\n", encoding="utf-8")

        report = run_deterministic_builds(build_fn, tmp_path / "work", n=3)
        assert report.match is True
        assert report.to_dict()["all_pass"] is True
        assert len(report.builds) == 3

    def test_divergent_builds_detected(self, tmp_path):
        counter = {"n": 0}

        def build_fn(out: Path) -> None:
            counter["n"] += 1
            (out / "canonical").mkdir(parents=True, exist_ok=True)
            # Deliberately different content per build
            (out / "canonical" / "rules.jsonl").write_text(
                json.dumps({"id": f"r{counter['n']}", "value": f"v{counter['n']}.com"}) + "\n",
                encoding="utf-8",
            )
            (out / "ir").mkdir(parents=True, exist_ok=True)
            (out / "ir" / "ir.json").write_text("{}", encoding="utf-8")

        report = run_deterministic_builds(build_fn, tmp_path / "work2", n=2)
        assert report.match is False
        assert report.mismatches

    def test_jsonl_order_independent(self, tmp_path):
        a = tmp_path / "a"
        b = tmp_path / "b"
        for d, lines in [
            (a, ['{"id":"1"}', '{"id":"2"}']),
            (b, ['{"id":"2"}', '{"id":"1"}']),
        ]:
            (d / "canonical").mkdir(parents=True)
            (d / "canonical" / "rules.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
            (d / "ir").mkdir(parents=True)
            (d / "ir" / "ir.json").write_text("{}", encoding="utf-8")
        report = compare_builds([a, b], labels=["A", "B"])
        assert report.match is True


# ===========================================================================
# Phase 7 — Legacy Regression
# ===========================================================================

class TestPhase7LegacyRegression:
    def test_added_removed_changed_moved(self):
        legacy = load_assets_from_records(
            [
                {"type": "domain_suffix", "value": "old.com", "service": "A"},
                {"type": "domain_suffix", "value": "keep.com", "service": "A"},
                {"type": "domain_suffix", "value": "move.com", "service": "A"},
            ],
            "legacy",
        )
        v1 = load_assets_from_records(
            [
                {"type": "domain_suffix", "value": "keep.com", "service": "A"},
                {"type": "domain_suffix", "value": "new.com", "service": "B"},
                {"type": "domain_suffix", "value": "move.com", "service": "B"},
            ],
            "v1",
        )
        report = compare_legacy_to_v1(
            legacy,
            v1,
            explanations={"domain_suffix:old.com": "intentional retirement"},
        )
        kinds = {i.kind for i in report.items}
        assert "Added" in kinds
        assert "Removed" in kinds
        assert "Moved" in kinds
        assert report.unexplained_removed == []
        assert report.to_dict()["all_pass"] is True

    def test_unexplained_removed_fails(self):
        legacy = load_assets_from_records(
            [{"type": "domain", "value": "gone.com", "service": "X"}],
            "legacy",
        )
        v1 = load_assets_from_records([], "v1")
        report = compare_legacy_to_v1(legacy, v1)
        assert "domain:gone.com" in report.unexplained_removed
        assert report.to_dict()["all_pass"] is False

    def test_file_based_entry(self, tmp_path):
        leg = tmp_path / "legacy.jsonl"
        v1 = tmp_path / "v1.jsonl"
        leg.write_text(
            json.dumps({"type": "domain", "value": "a.com", "service": "S"}) + "\n",
            encoding="utf-8",
        )
        v1.write_text(
            json.dumps({"type": "domain", "value": "a.com", "service": "S"}) + "\n"
            + json.dumps({"type": "domain", "value": "b.com", "service": "S"}) + "\n",
            encoding="utf-8",
        )
        report = run_legacy_regression(leg, v1)
        assert report.counts.get("Added", 0) == 1
        assert report.counts.get("Removed", 0) == 0
