from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.engine.collection.run import COLLECTION_NODES, COLLECTION_SPECS, _collection_id, _manifest_digest


def test_collection_dag_has_explicit_dependencies() -> None:
    names = [n.name for n in COLLECTION_NODES]
    assert names == [spec.name for spec in COLLECTION_SPECS]
    assert "service_rules" in names
    assert "ip_rules" in names
    assert "datasets" in names
    assert "providers" in names
    assert next(n for n in COLLECTION_NODES if n.name == "service_rules").deps == ("validate_registry",)
    assert next(n for n in COLLECTION_NODES if n.name == "network_datasets").deps == ("datasets",)


def test_collection_commands_reference_existing_python_scripts() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    for spec in COLLECTION_SPECS:
        command = spec.command
        assert command[0] == __import__("sys").executable
        assert len(command) == 2
        script = repo_root / command[1]
        assert command[1].startswith("scripts/")
        assert script.suffix == ".py"
        assert script.is_file(), f"missing collection entrypoint: {script}"


def test_collection_id_is_deterministic() -> None:
    results = {
        "b": {"status": "ok", "critical": False, "attempts": [{"attempt": 1}]},
        "a": {"status": "ok", "critical": True, "attempts": [{"attempt": 1}]},
    }
    assert _collection_id("2026-09-02", results) == _collection_id(
        "2026-09-02", dict(reversed(list(results.items())))
    )


def test_collection_manifest_digest_ignores_its_own_field() -> None:
    manifest = {
        "schema": "collection_manifest_v1",
        "collection_id": "2026-09-02-demo",
        "status": "ok",
        "root": "backup/2026-09-02",
        "nodes": {"service_rules": {"status": "ok", "critical": True, "deps": []}},
    }
    digest = _manifest_digest(manifest)
    with_field = {**manifest, "manifest_sha256": digest}
    assert _manifest_digest(with_field) == digest
    assert digest == hashlib.sha256(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def test_collection_manifest_contract_shape(tmp_path: Path) -> None:
    payload = {
        "schema": "collection_manifest_v1",
        "collection_id": "2026-09-02-demo",
        "status": "ok",
        "root": "backup/2026-09-02",
        "nodes": {"service_rules": {"status": "ok", "critical": True, "deps": []}},
    }
    path = tmp_path / "_collection.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["schema"] == "collection_manifest_v1"
    assert loaded["status"] == "ok"
