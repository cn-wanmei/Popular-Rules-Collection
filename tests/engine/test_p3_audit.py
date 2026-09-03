from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.engine.audit.core import (
    adapter_capability_matrix,
    build_provenance_graph,
    dependency_lock_report,
    semantic_rule_diff,
    source_health_score,
    verify_action_shas,
    write_checksum_manifest,
)


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def test_semantic_rule_diff_ignores_volatile_metadata(tmp_path: Path):
    current = tmp_path / "current.jsonl"
    baseline = tmp_path / "baseline.jsonl"
    _write_jsonl(baseline, [{"id": "a", "value": "x", "updated_at": "1"}, {"id": "b", "value": "y"}])
    _write_jsonl(current, [{"id": "a", "value": "x", "updated_at": "2"}, {"id": "b", "value": "z"}, {"id": "c", "value": "n"}])
    result = semantic_rule_diff(current, baseline)
    assert result["counts"] == {"added": 1, "removed": 0, "changed": 1}
    assert result["changed_ids"] == ["b"]


def test_capability_matrix_and_health():
    matrix = adapter_capability_matrix({"alpha": {"capabilities": ["domain", "cidr"]}}, ["domain", "cidr", "geosite"])
    assert matrix["adapters"]["alpha"]["ready"] is False
    health = source_health_score({"http_status": 200, "latency_ms": 100, "error_count": 0})
    assert health["score"] == 100.0


def test_provenance_graph():
    result = build_provenance_graph([{"source": "feed-a", "artifact": "rules.jsonl", "stage": "normalize"}])
    assert len(result["nodes"]) == 2
    assert result["edges"][0]["stage"] == "normalize"


def test_lock_and_sha_verification(tmp_path: Path):
    lock = tmp_path / "requirements.lock"
    lock.write_text("demo==1.0\n", encoding="utf-8")
    assert dependency_lock_report(lock)["locked"] is True
    workflows = tmp_path / "workflows"
    workflows.mkdir()
    (workflows / "ok.yml").write_text("- uses: actions/checkout@0123456789abcdef0123456789abcdef01234567\n", encoding="utf-8")
    assert verify_action_shas(workflows)["pass"] is True
    (workflows / "bad.yml").write_text("- uses: actions/checkout@main\n", encoding="utf-8")
    assert verify_action_shas(workflows)["pass"] is False


def test_checksum_manifest(tmp_path: Path):
    artifact = tmp_path / "a.txt"
    artifact.write_text("hello", encoding="utf-8")
    result = write_checksum_manifest(tmp_path, tmp_path / "reports" / "checksums.json")
    assert result["algorithm"] == "sha256"
    assert result["files"][0]["path"] == "a.txt"
