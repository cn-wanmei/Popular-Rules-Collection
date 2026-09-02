from pathlib import Path

import src.engine.pipeline.run as pipeline


def test_run_pipeline_resolves_relative_collection_root(tmp_path, monkeypatch):
    relative_root = Path("backup/2026-09-01")
    collection_manifest = {
        "schema": "collection_manifest_v1",
        "collection_id": "2026-09-01-test",
        "root": str(relative_root),
        "status": "ok",
    }

    monkeypatch.setattr(pipeline, "_load_collection_manifest", lambda root: collection_manifest)
    monkeypatch.setattr(
        pipeline,
        "create_source_snapshot",
        lambda sources_root, output_root, extra_meta: {
            "snapshot_id": "test-snapshot",
            "file_count": 0,
        },
    )

    result = pipeline.run_pipeline(
        relative_root,
        tmp_path,
        stages=["snapshot"],
        run_id="relative-path-test",
    )

    assert result["status"] == "ok"
    assert result["collection_id"] == "2026-09-01-test"
    assert result["collection_manifest"] == "backup/2026-09-01/manifests/_collection.json"
    assert (tmp_path / "runs" / "relative-path-test" / "run_manifest.json").exists()
