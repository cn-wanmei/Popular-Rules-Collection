from __future__ import annotations

from scripts import collect


def test_prs_source_can_be_runtime_enabled_by_single_service_entry(monkeypatch):
    source = {
        "id": "popular-rules-source",
        "enabled": False,
        "rules": [
            {"path": "generated/source/dingding/domains.txt", "enabled": True},
            {"path": "generated/source/qqmail/domains.txt", "enabled": False},
        ],
    }
    assert collect.source_runtime_enabled(source) is True


def test_prs_source_stays_disabled_when_all_service_entries_are_disabled():
    source = {
        "id": "popular-rules-source",
        "enabled": False,
        "rules": [
            {"path": "generated/source/dingding/domains.txt", "enabled": False},
        ],
    }
    assert collect.source_runtime_enabled(source) is False


def test_other_global_sources_keep_global_enable_semantics():
    source = {
        "id": "other-source",
        "enabled": False,
        "rules": [{"path": "rule/example.txt", "enabled": True}],
    }
    assert collect.source_runtime_enabled(source) is False
    source["enabled"] = True
    assert collect.source_runtime_enabled(source) is True


def test_prs_production_failures_are_required_failures(tmp_path, monkeypatch):
    source = {
        "id": "popular-rules-source",
        "enabled": False,
        "fetch": {"type": "github_raw"},
        "rules": [
            {"path": "generated/source/cainiao/domains.txt", "enabled": True},
        ],
    }

    def fake_fetch_entry(*args, **kwargs):
        return {
            "name": "domains.txt",
            "path": "generated/source/cainiao/domains.txt",
            "service": "cainiao",
            "status": "failed",
            "error": "simulated upstream failure",
        }

    monkeypatch.setattr(collect, "_fetch_entry", fake_fetch_entry)
    result = collect.collect_source(
        source,
        tmp_path / "day",
        {"sources": {}},
        collect.FetchStateStore(tmp_path / "state.json"),
        max_workers=1,
    )

    assert result["files_failed"] == 1
    assert result["required_failures"] == 1
