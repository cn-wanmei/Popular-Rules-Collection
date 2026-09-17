from pathlib import Path

import yaml

from src.engine.ingest.legacy_asset_reconciliation import reconcile_legacy_assets


def _service(root: Path, category: str, name: str, metadata: str, filename: str, content: str) -> None:
    directory = root / category / name
    directory.mkdir(parents=True)
    (directory / "metadata.yaml").write_text(metadata, encoding="utf-8")
    (directory / filename).write_text(content, encoding="utf-8")


def test_reconciliation_reports_exact_duplicate_relation_and_candidates(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    (root / "_index.yaml").write_text(
        """categories:\n  ai:\n    rules:\n      - id: openai\n        name: OpenAI\n        path: rule/AI/OpenAI\n        service_type: service\n        domains: 1\n        ips: 1\n      - id: ai\n        name: AI\n        path: rule/AI/AI\n        service_type: aggregate\n        domains: 1\n        ips: 0\n""",
        encoding="utf-8",
    )
    _service(root, "AI", "OpenAI", "id: openai\nname: OpenAI\nservice_type: service\nparent: ai\n", "openai.list", "openai.com\nopenai.com\n10.0.0.0/8\n")
    _service(root, "AI", "AI", "id: ai\nname: AI\nservice_type: aggregate\nchildren: [openai, mistral]\n", "ai.list", "ai.example\n")

    report = reconcile_legacy_assets(root, jsonl_output=tmp_path / "assets.jsonl", report_path=tmp_path / "report.yaml")
    openai = next(item for item in report["services"] if item["id"] == "openai")
    assert openai["domain"]["status"] == "exact-match"
    assert openai["ip_cidr"]["status"] == "exact-match"
    assert report["relation_drift"][0]["missing_from_index"] == ["mistral"]
    aggregate = report["aggregate_own_assets"][0]
    assert aggregate["own_assets_not_in_child_union"] == 1
    candidate = next(item for item in report["promotion_candidates"] if item["id"] == "openai")
    assert candidate["candidate"] is True
    assert candidate["promotion_status"] == "blocked-until-canonical-review"
    assert yaml.safe_load((tmp_path / "report.yaml").read_text(encoding="utf-8"))["promotion"]["blocked"] is True
