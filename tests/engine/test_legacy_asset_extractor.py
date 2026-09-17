from pathlib import Path

from src.engine.ingest.legacy_asset_extractor import extract_legacy_asset_ir, iter_service_assets, write_asset_jsonl


def _write_service(root: Path, category: str, name: str, metadata: str, files: dict[str, str]) -> None:
    directory = root / category / name
    directory.mkdir(parents=True)
    (directory / "metadata.yaml").write_text(metadata, encoding="utf-8")
    for filename, content in files.items():
        (directory / filename).write_text(content, encoding="utf-8")


def test_extracts_domains_cidrs_urls_and_deduplicates(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    (root / "_index.yaml").write_text(
        """categories:\n  ai:\n    rules:\n      - id: openai\n        name: OpenAI\n        path: rule/AI/OpenAI\n        service_type: service\n        domains: 2\n        ips: 1\n      - id: ai\n        name: AI\n        path: rule/AI/AI\n        service_type: aggregate\n        domains: 3\n        ips: 0\n""",
        encoding="utf-8",
    )
    _write_service(
        root,
        "AI",
        "OpenAI",
        """id: openai\nname: OpenAI\nprimary_category: ai\ncategories: [ai]\nservice_type: service\nparent: ai\nchildren: null\nsources: [blackmatrix7]\n""",
        {
            "openai.list": "DOMAIN-SUFFIX,openai.com\nhttps://api.openai.com/v1\n10.0.0.0/8\n",
            "openai_domain.list": "openai.com\n",
        },
    )
    _write_service(
        root,
        "AI",
        "AI",
        """id: ai\nname: AI\nprimary_category: ai\ncategories: [ai]\nservice_type: aggregate\nparent: null\nchildren: [openai, mistral]\nsources: [metacubex]\n""",
        {"ai.list": "ai.example\n"},
    )

    ir = extract_legacy_asset_ir(root)
    openai = next(item for item in ir.services if item.id == "openai")
    assert openai.domains == 0
    assert openai.domain_suffixes == 2
    assert openai.cidrs == 1
    assert openai.urls == 1
    assert openai.records == 4
    assert ir.relation_drift[0]["aggregate"] == "ai"
    assert ir.relation_drift[0]["missing_from_index"] == ["mistral"]


def test_streamed_asset_ir_preserves_provenance(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    _write_service(
        root,
        "Google",
        "GoogleFCM",
        """id: googlefcm\nname: GoogleFCM\nservice_type: service\nparent: google\nsources: [blackmatrix7, dler]\n""",
        {"googlefcm_ip.list": "142.250.0.1/32\n142.250.0.2/32\n"},
    )

    records = list(iter_service_assets(root))
    assert len(records) == 2
    assert records[0].asset.asset_type == "ip_cidr"
    assert records[0].asset.line == 1
    assert records[0].asset.sources == ("blackmatrix7", "dler")


def test_jsonl_output_is_streamed_and_hashed(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    _write_service(
        root,
        "AI",
        "OpenAI",
        "id: openai\nname: OpenAI\nservice_type: service\n",
        {"openai.list": "openai.com\n"},
    )
    output = tmp_path / "out" / "assets.jsonl"
    result = write_asset_jsonl(root, output)
    assert result["records"] == 1
    assert len(result["sha256"]) == 64
    assert output.read_text(encoding="utf-8").count("\n") == 1
