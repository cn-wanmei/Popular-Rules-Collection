from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sources" / "immutable_registry.yaml"
SERVICES = {"1688", "cainiao", "dingding", "qqmail", "qqmusic", "taobao", "tencentcloud", "tmall"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")


def test_immutable_registry_covers_phase2_services() -> None:
    # Active bindings must carry both artifact and gate lineage.
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert data["schema"] == "popular_rules_collection_immutable_source_registry_v1"
    bindings = data["bindings"]
    assert SERVICES <= set(bindings)
    for service in SERVICES:
        binding = bindings[service]
        assert binding["source_id"] == "popular-rules-source"
        assert binding["status"] in {"pending", "active"}
        if binding["status"] == "active":
            assert SHA40.fullmatch(binding["source_ref"])
            assert SHA40.fullmatch(binding["verified_input_commit"])
            assert binding["artifact_path"]
            assert binding["release_path"]
            assert binding["snapshot_id"]
            assert SHA64.fullmatch(binding["expected_sha256"])
            assert binding["content_digest"]
