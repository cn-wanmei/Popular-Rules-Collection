from __future__ import annotations

import json
from pathlib import Path

from src.engine.cli.__main__ import main
from src.engine.ingest.formats.v2fly import parse_line as parse_v2fly_line
from src.engine.ingest.normalizer import normalize_record
from src.engine.ingest.rule_parser import parse_line
from src.engine.pipeline.run import run_pipeline
from src.engine.promote.artifact import promote_run, rollback_to_run


def test_domain_rules_with_qualifiers_parse_without_truncation() -> None:
    assert parse_line("DOMAIN-SUFFIX,example.com,no-resolve") == [("domain_suffix", "example.com")]
    assert parse_line("DOMAIN,mail.example.com") == [("domain", "mail.example.com")]


def test_v2fly_adapter_and_v3_normalizer_are_independent() -> None:
    assert parse_v2fly_line("full:example.com") == [("domain", "example.com")]
    assert parse_v2fly_line("domain:example.com") == [("domain_suffix", "example.com")]
    assert normalize_record("Demo", "DOMAIN-SUFFIX", "example.com")["service"] == "demo"


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
    result = run_pipeline(source, tmp_path / "data")
    assert result["status"] == "ok"
    run_dir = tmp_path / "data" / "runs" / result["run_id"]
    rules = (run_dir / "canonical" / "rules.jsonl").read_text(encoding="utf-8")
    assert "example.com" in rules and "mail.example.com" in rules
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
    result = run_pipeline(source, tmp_path / "data", skip_large=True)
    assert result["status"] == "ok"
    assert result["skip_large"] is True
    text = (tmp_path / "data" / "runs" / result["run_id"] / "canonical" / "rules.jsonl").read_text(encoding="utf-8")
    assert "demo.example.com" in text and "baidu.com" not in text


def test_cli_publish_is_release_gated_and_advances_baseline(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "services"
    source.mkdir(parents=True)
    (source / "demo.yaml").write_text(
        "id: demo\ncategory: service\nrules:\n  - type: DOMAIN-SUFFIX\n    value: demo.example.com\n",
        encoding="utf-8",
    )
    generated = tmp_path / "generated"
    baseline = tmp_path / "data" / "baseline" / "canonical.json"
    rc = main(["publish", "--sources", str(tmp_path / "sources"), "--data", str(tmp_path / "data"), "--generated", str(generated), "--baseline", str(baseline)])
    assert rc == 0
    latest = json.loads((generated / "_promotion" / "latest.json").read_text(encoding="utf-8"))
    canonical = tmp_path / "data" / "runs" / latest["run_id"] / "canonical" / "rules.jsonl"
    assert baseline.read_bytes() == canonical.read_bytes()
    assert latest["release_state"] == "RC_READY"


def test_invalid_release_manifest_blocks_rollback(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "services"
    source.mkdir(parents=True)
    (source / "demo.yaml").write_text(
        "id: demo\ncategory: service\nrules:\n  - type: DOMAIN-SUFFIX\n    value: demo.example.com\n",
        encoding="utf-8",
    )
    data = tmp_path / "data"
    result = run_pipeline(source, data)
    run_dir = data / "runs" / result["run_id"]
    manifest = run_dir / "release" / "manifest.json"
    doc = json.loads(manifest.read_text(encoding="utf-8"))
    doc["canonical_digest"] = "tampered"
    manifest.write_text(json.dumps(doc), encoding="utf-8")
    try:
        rollback_to_run(result["run_id"], data / "runs", tmp_path / "generated")
    except RuntimeError as exc:
        assert "digest" in str(exc)
    else:
        raise AssertionError("tampered release manifest must block rollback")
