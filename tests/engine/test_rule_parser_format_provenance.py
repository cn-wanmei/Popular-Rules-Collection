from pathlib import Path

from src.engine.ingest.rule_parser import detect_format, iter_rule_records, parse_line


def test_metacubex_geosite_suffix_preserves_suffix_semantics(tmp_path: Path):
    path = tmp_path / "geosite_alibaba.list"
    path.write_text("+.alibaba\n+.taobao\n", encoding="utf-8")
    assert detect_format(path) == "metacubex_geosite"
    assert list(iter_rule_records(path)) == [
        ("domain_suffix", "alibaba", "metacubex_geosite"),
        ("domain_suffix", "taobao", "metacubex_geosite"),
    ]


def test_native_process_name_is_not_silently_discarded():
    assert parse_line("PROCESS-NAME, example.exe") == [("process_name", "example.exe")]


def test_v2fly_keyword_and_full_keep_distinct_types(tmp_path: Path):
    path = tmp_path / "rules.list"
    path.write_text("keyword:google\nfull:www.google.com\n", encoding="utf-8")
    assert detect_format(path) == "v2fly"
    assert list(iter_rule_records(path)) == [
        ("domain_keyword", "google", "v2fly"),
        ("domain", "www.google.com", "v2fly"),
    ]
