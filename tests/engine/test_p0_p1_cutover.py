from __future__ import annotations

import json
from pathlib import Path

from src.engine.cli.__main__ import main
from src.engine.pipeline.run import run_pipeline


# P0-P1 regression suite: publish, collected-input ingest, and fail-closed CLI.


def test_collected_snapshot_ingest_replaces_normalize(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    manifests = source / "manifests"
    raw = source / "sources" / "demo"
    manifests.mkdir()
    raw.mkdir(parents=True)
    (raw / "example.list").write_text("DOMAIN-SUFFIX,example.com\nDOMAIN,mail.example.com\n", encoding="utf-8")
    (manifests / "demo.json").write_text(
        json.dumps({
            "source": "demo",
            "files": [{
                "name": "example.list",
                "service": "example-service",
                "local": "sources/demo/example.list",
                "status": "ok",
                "url": "https://example.invalid/rules",
            }],
        }),
        encoding="utf-8",
    )
    (manifests / "_day.json").write_text("{}", encoding="utf-8")

    data = tmp_path / "data"
    result = run_pipeline(source, data)
    assert result["status"] == "ok"
    run_dir = data / "runs" / result["run_id"]
    rules = (run_dir / "canonical" / "rules.jsonl").read_text(encoding="utf-8")
    assert "example.com" in rules
    assert "mail.example.com" in rules
    assert not (tmp_path / "database" / "services").exists()


def test_cli_publish_performs_real_promotion(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "services"
    source.mkdir(parents=True)
    (source / "demo.yaml").write_text(
        "id: demo\ncategory: service\nrules:\n  - type: DOMAIN-SUFFIX\n    value: demo.example.com\n",
        encoding="utf-8",
    )
    generated = tmp_path / "generated"
    rc = main([
        "publish",
        "--sources", str(tmp_path / "sources"),
        "--data", str(tmp_path / "data"),
        "--generated", str(generated),
    ])
    assert rc == 0
    assert (generated / "mihomo").exists()
    assert (generated / "_promotion" / "latest.json").exists()


def test_cli_release_missing_sources_returns_failure(tmp_path: Path) -> None:
    rc = main([
        "release",
        "--sources", str(tmp_path / "missing"),
        "--data", str(tmp_path / "data"),
    ])
    assert rc != 0
