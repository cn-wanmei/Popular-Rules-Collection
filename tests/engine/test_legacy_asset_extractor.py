from pathlib import Path
from time import perf_counter

from src.engine.ingest.legacy_asset_extractor import extract_legacy_asset_ir, iter_service_assets, write_asset_jsonl
from src.engine.ingest.rule_parser import iter_rule_records_with_line


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
    assert openai.domain_suffixes == 1
    assert openai.cidrs == 1
    assert openai.urls == 1
    assert openai.records == 3
    assert ir.relation_drift[0]["aggregate"] == "ai"
    assert ir.relation_drift[0]["missing_from_index"] == ["mistral"]


def test_line_provenance_and_duplicate_evidence_are_exact(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    _write_service(
        root,
        "AI",
        "OpenAI",
        "id: openai\nname: OpenAI\nservice_type: service\n",
        {"openai.list": "openai.com\nopenai.com\nhttps://api.openai.com/v1\n"},
    )
    records = list(iter_service_assets(root))
    domain = next(item for item in records if item.asset.asset_type == "domain_suffix")
    url = next(item for item in records if item.asset.asset_type == "url")
    assert domain.asset.line == 1
    assert domain.occurrences == 2
    assert {item["line"] for item in domain.evidence} == {1, 2}
    assert url.asset.line == 3
    assert url.occurrences == 1


def test_parser_line_api_is_single_pass_provenance(tmp_path: Path) -> None:
    path = tmp_path / "rules.list"
    path.write_text("DOMAIN-SUFFIX,example.com\nhttps://api.example.com/v1\n10.0.0.0/8\n", encoding="utf-8")
    records = list(iter_rule_records_with_line(path))
    assert [(line, typ, value) for _path, line, typ, value, _fmt in records] == [
        (1, "domain_suffix", "example.com"),
        (2, "url", "https://api.example.com/v1"),
        (3, "ip_cidr", "10.0.0.0/8"),
    ]


def test_v2fly_include_preserves_source_provenance(tmp_path: Path) -> None:
    root = tmp_path / "v2fly"
    root.mkdir()
    included = root / "included.list"
    included.write_text("full: example.com\n", encoding="utf-8")
    source = root / "v2fly_main.list"
    source.write_text("include: included.list\n", encoding="utf-8")
    records = list(iter_rule_records_with_line(source))
    assert records == [(included, 1, "domain", "example.com", "v2fly")]


def test_jsonl_output_preserves_final_occurrence_metadata(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    _write_service(
        root,
        "AI",
        "OpenAI",
        "id: openai\nname: OpenAI\nservice_type: service\n",
        {"openai.list": "openai.com\nopenai.com\n"},
    )
    output = tmp_path / "out" / "assets.jsonl"
    result = write_asset_jsonl(root, output)
    assert result["records"] == 1
    text = output.read_text(encoding="utf-8")
    assert '"occurrences": 2' in text
    assert '"line": 1' in text
    assert '"line": 2' in text


def test_large_sample_does_not_reintroduce_quadratic_line_rescan(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    payload = "".join(f"host{i}.example.com\n" for i in range(10000))
    _write_service(
        root,
        "AI",
        "OpenAI",
        "id: openai\nname: OpenAI\nservice_type: service\n",
        {"openai.list": payload},
    )
    started = perf_counter()
    records = list(iter_service_assets(root))
    elapsed = perf_counter() - started
    assert len(records) == 10000
    assert elapsed < 5.0, f"10k single-pass records took {elapsed:.3f}s"


def test_phase8_legacy_equivalence_manifest_is_ingested(tmp_path: Path) -> None:
    root = tmp_path / "rule"
    root.mkdir()
    (root / "_legacy_asset_equivalence.yaml").write_text(
        """version: 1
schema: v1_legacy_asset_equivalence_v1
assets:
  - service: example
    type: domain_suffix
    value: example.com
""",
        encoding="utf-8",
    )
    records = list(iter_service_assets(root))
    assert len(records) == 1
    assert records[0].asset.service == "example"
    assert records[0].asset.asset_type == "domain_suffix"
    assert records[0].asset.value == "example.com"
