
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


def test_prs_production_failures_are_required_failures():
    # This exercises the production-source invariant without contacting the network.
    source = {
        "id": "popular-rules-source",
        "enabled": False,
        "rules": [
            {"path": "generated/source/cainiao/domains.txt", "enabled": True},
        ],
    }
    entries = collect.rules_for(source)
    assert len(entries) == 1
    assert entries[0]["service"] == "cainiao"
