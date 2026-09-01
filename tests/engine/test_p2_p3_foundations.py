from __future__ import annotations

from pathlib import Path

from src.engine.cas.store import digest_bytes, has, put_bytes, read_bytes
from src.engine.dag.executor import Node, execute, topological_layers
from src.engine.decision.confidence import score_rule


def test_cas_roundtrip(tmp_path: Path) -> None:
    root = tmp_path / "cas"
    payload = b"hello-cas"
    digest = put_bytes(payload, root)
    assert digest == digest_bytes(payload)
    assert has(digest, root)
    assert read_bytes(digest, root) == payload


def test_dag_layers_and_parallel_ready_nodes() -> None:
    nodes = [Node("snapshot"), Node("ingest", ("snapshot",)), Node("canonical", ("ingest",)), Node("diff", ("canonical",)), Node("golden", ("canonical",))]
    assert topological_layers(nodes) == [["snapshot"], ["ingest"], ["canonical"], ["diff", "golden"]]
    seen: list[str] = []
    result = execute(nodes, {"snapshot": lambda: seen.append("snapshot") or 1, "ingest": lambda: 2, "canonical": lambda: 3, "diff": lambda: 4, "golden": lambda: 5})
    assert result["golden"]["status"] == "ok"
    assert result["golden"]["value"] == 5
    assert result["golden"]["duration_ms"] >= 0
    assert seen == ["snapshot"]


def test_confidence_is_explainable() -> None:
    result = score_rule({"identity_key": "d:x", "classification": {"category": "service"}, "provenance": {"sources": [{"id": "a"}, {"id": "b"}]}})
    assert result["score"] == 0.9
    assert result["band"] == "high"
    assert result["reasons"]
