from __future__ import annotations

import json
from pathlib import Path

from scripts.production_collection_gate import validate_collection_root


def _write_collection(
    root: Path,
    *,
    skip_large: bool,
    service_status: str = "ok",
    required_failures: int = 0,
) -> None:
    manifests = root / "manifests"
    manifests.mkdir(parents=True)
    collection = {
        "schema": "collection_manifest_v1",
        "collection_id": "2026-09-25-demo",
        "date": "2026-09-25",
        "root": "backup/2026-09-25",
        "status": "ok",
        "skip_large": skip_large,
        "nodes": {"service_rules": {"status": service_status, "critical": True}},
    }
    (manifests / "_collection.json").write_text(
        json.dumps(collection), encoding="utf-8"
    )

    day = {
        "schema": "collection_manifest_v2",
        "date": "2026-09-25",
        "sources": [
            {"source": "popular-rules-source", "required_failures": required_failures}
        ],
    }
    (manifests / "_day.json").write_text(json.dumps(day), encoding="utf-8")


def test_production_gate_rejects_partial_snapshot(tmp_path: Path) -> None:
    root = tmp_path / "backup" / "2026-09-25"
    _write_collection(root, skip_large=True)
    report = validate_collection_root(root)
    assert report["pass"] is False
    assert any("skip_large" in error for error in report["errors"])


def test_production_gate_accepts_complete_snapshot(tmp_path: Path) -> None:
    root = tmp_path / "backup" / "2026-09-25"
    _write_collection(root, skip_large=False)
    report = validate_collection_root(root)
    assert report["pass"] is True


def test_production_gate_rejects_required_source_failure(tmp_path: Path) -> None:
    root = tmp_path / "backup" / "2026-09-25"
    _write_collection(root, skip_large=False, required_failures=1)
    report = validate_collection_root(root)
    assert report["pass"] is False
    assert report["required_failures"]
