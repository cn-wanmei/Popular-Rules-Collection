from __future__ import annotations

import json
from pathlib import Path

from src.engine.cli.__main__ import main
from src.engine.ingest.rule_parser import parse_line
from src.engine.pipeline.run import run_pipeline
from src.engine.promote.artifact import promote_run


# P0-P1 regression suite: publish, collected-input ingest, fail-closed CLI,
# parser correctness, skip-large, and released baseline promotion.


def test_domain_rules_with_qualifiers_parse_without_truncation() -> None:
    assert parse_line("DOMAIN-SUFFIX,example.com,no-resolve") == [("domain_suffix", "example.com")]
    assert parse_line("DOMAIN,mail.example.com") == [("domain", "mail.example.com")]


def test_collected_snapshot_ingest_replaces_normalize(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    manifests = source / "manifests"
    raw = source / "sources" / "demo"
    manifests.mkdir()
    raw.mkdir(parents=True)
    (raw / "example.list").write_text(
        "DOMAIN-SUFFIX,example.com\nDOMAIN,mail.example.com\n", encoding="utf-8"
    )
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


def test_skip_large_is_carried_into_engine_manifest(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "services"
    source.mkdir(parents=True)
    (source / "demo.yaml").write_text(
        "id: demo\ncategory: service\nrules:\n  - type: DOMAIN-SUFFIX\n    value: demo.example.com\n",
        encoding="utf-8",
    )
    (source / "china.yaml").write_text(
        "id: china\ncategory: network\nrules:\n  - type: DOMAIN-SUFFIX\n    value: baidu.com\n",
        encoding="utf-8",
    )
    data = tmp_path / "data"
    result = run_pipeline(source, data, skip_large=True)
    assert result["status"] == "ok"
    assert result["skip_large"] is True
    run_dir = data / "runs" / result["run_id"]
    text = (run_dir / "canonical" / "rules.jsonl").read_text(encoding="utf-8")
    assert "demo.example.com" in text
    assert "baidu.com" not in text


def test_cli_publish_performs_real_promotion_and_baseline(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "services"
    source.mkdir(parents=True)
    (source / "demo.yaml").write_text(
        "id: demo\ncategory: service\nrules:\n  - type: DOMAIN-SUFFIX\n    value: demo.example.com\n",
        encoding="utf-8",
    )
    generated = tmp_path / "generated"
    baseline = tmp_path / "data" / "baseline" / "canonical.json"
    rc = main([
        "publish",
        "--sources", str(tmp_path / "sources"),
        "--data", str(tmp_path / "data"),
        "--generated", str(generated),
        "--baseline", str(baseline),
    ])
    assert rc == 0
    assert (generated / "mihomo").exists()
    assert (generated / "_promotion" / "latest.json").exists()
    assert baseline.exists()
    run_id = json.loads((generated / "_promotion" / "latest.json").read_text(encoding="utf-8"))["run_id"]
    canonical = tmp_path / "data" / "runs" / run_id / "canonical" / "rules.jsonl"
    assert baseline.read_bytes() == canonical.read_bytes()


def test_cli_promote_advances_baseline_only_after_valid_release(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "services"
    source.mkdir(parents=True)
    (source / "demo.yaml").write_text(
        "id: demo\ncategory: service\nrules:\n  - type: DOMAIN-SUFFIX\n    value: demo.example.com\n",
        encoding="utf-8",
    )
    data = tmp_path / "data"
    result = run_pipeline(source, data)
    baseline = data / "baseline" / "canonical.json"
    generated = tmp_path / "generated"
    record = promote_run(
        data / "runs" / result["run_id"],
        generated,
        baseline_path=baseline,
    )
    assert record["release_state"] == "RC_READY"
    assert baseline.exists()


def test_cli_release_missing_sources_returns_failure(tmp_path: Path) -> None:
    rc = main([
        "release",
        "--sources", str(tmp_path / "missing"),
        "--data", str(tmp_path / "data"),
    ])
    assert rc != 0
