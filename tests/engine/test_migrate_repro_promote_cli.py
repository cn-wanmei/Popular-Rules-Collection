"""Migration path + Reproducibility + Promote/Rollback + CLI smoke."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from src.engine.ingest.migrate_legacy import migrate_database_services_to_snapshot
from src.engine.pipeline.run import run_pipeline
from src.engine.reproducibility.hash_compare import compute_run_digest, compare_runs
from src.engine.promote.artifact import promote_run, rollback_to_run
from src.engine.cli.__main__ import main


def _fake_database_services(tmp: Path) -> Path:
    d = tmp / "database" / "services"
    d.mkdir(parents=True)
    (d / "google-gmail.yaml").write_text(
        "id: google-gmail\ncategory: mail\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: gmail.com\n", encoding="utf-8")
    (d / "china.yaml").write_text(
        "id: china\ncategory: china\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: baidu.com\n", encoding="utf-8")
    return d


def test_migrate_legacy_then_pipeline():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        db = _fake_database_services(tmp)
        snaps = tmp / "data" / "snapshots"
        manifest = migrate_database_services_to_snapshot(db, snaps)
        assert manifest["v2_runtime_dependency"] == 0
        assert manifest["extra"]["service_files"] == 2
        snap_id = manifest["snapshot_id"]
        # Copy snapshot sources to a clean sources dir so pipeline creates a NEW snapshot
        import shutil
        clean_sources = tmp / "clean_sources"
        shutil.copytree(snaps / snap_id / "sources", clean_sources)
        data = tmp / "data"
        result = run_pipeline(clean_sources, data)
        assert result["status"] == "ok"
        assert result["stages"]["release"]["state"] == "RC_READY"


def test_reproducibility_same_snapshot():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        src = tmp / "sources" / "services"
        src.mkdir(parents=True)
        (src / "a.yaml").write_text(
            "id: a\ncategory: mail\nrules:\n  - type: DOMAIN\n    value: a.com\n", encoding="utf-8")
        data = tmp / "data"
        r1 = run_pipeline(tmp / "sources", data, run_id="run-A")
        r2 = run_pipeline(tmp / "sources", data, run_id="run-B")
        # note: different snapshot_ids because create_source_snapshot always new
        # but same logical content → digests of canonical should match structure
        d1 = compute_run_digest(data / "runs" / "run-A")
        d2 = compute_run_digest(data / "runs" / "run-B")
        assert d1["file_count"] > 0
        assert d2["file_count"] > 0
        # overall may differ because snapshot_id embedded, but rules.jsonl content digest should be equal
        assert d1["file_digests"].get("canonical/rules.jsonl") == d2["file_digests"].get("canonical/rules.jsonl")


def test_promote_and_rollback():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        src = tmp / "sources" / "services"
        src.mkdir(parents=True)
        (src / "x.yaml").write_text(
            "id: x\ncategory: mail\nrules:\n  - type: DOMAIN\n    value: x.com\n", encoding="utf-8")
        data = tmp / "data"
        result = run_pipeline(tmp / "sources", data)
        run_id = result["run_id"]
        generated = tmp / "generated"
        rec = promote_run(data / "runs" / run_id, generated)
        assert rec["release_state"] == "RC_READY"
        assert (generated / "mihomo").exists()
        assert (generated / "_promotion" / "latest.json").exists()
        # rollback to same run (smoke)
        rec2 = rollback_to_run(run_id, data / "runs", generated)
        assert rec2["run_id"] == run_id


def test_cli_version():
    assert main(["--version"]) == 0
