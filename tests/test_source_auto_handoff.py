from __future__ import annotations

import copy

import pytest

from scripts.source_auto_handoff import (
    LINEAGE_SERVICES,
    _validate_source_seal_report,
)


SOURCE_REF = "a" * 40
VERIFIED_INPUT = "b" * 40


def _service_record(service_id: str, *, schema: str) -> dict:
    item = {
        "status": "PERSISTED",
        "snapshot_id": f"snap-{service_id}-test",
        "content_digest": "c" * 64,
        "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64,
        "generator_digest": "f" * 64,
        "release_digest": "0" * 64,
        "release_identity_version": "2",
        "release_path": f"releases/{service_id}/snap-{service_id}-test/release.json",
        "expected_sha256": "1" * 64,
    }
    if schema == "popular_rules_source_durable_bridge_v3":
        item["source_ref"] = SOURCE_REF
    return item


def _report(schema: str = "popular_rules_source_durable_bridge_v3") -> dict:
    services = {
        service_id: _service_record(service_id, schema=schema)
        for service_id in LINEAGE_SERVICES
    }
    report = {
        "schema": schema,
        "persistence_commit": SOURCE_REF,
        "verified_input_commit": VERIFIED_INPUT,
        "services": services,
    }
    if schema == "popular_rules_source_durable_bridge_v3":
        report.update({
            "seal_completeness": "COMPLETE",
            "batch_completeness": "COMPLETE",
            "run_completeness": "COMPLETE",
            "persisted_count": len(services),
            "missing_from_execution": [],
            "incomplete": [],
        })
    return report


def test_source_handoff_accepts_complete_durable_bridge_v2() -> None:
    report = _report("popular_rules_source_durable_bridge_v2")
    assert _validate_source_seal_report(report) is report


def test_source_handoff_accepts_complete_durable_bridge_v3() -> None:
    report = _report()
    assert _validate_source_seal_report(report) is report


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seal_completeness", "PARTIAL"),
        ("batch_completeness", "PARTIAL"),
        ("run_completeness", "PARTIAL"),
    ],
)
def test_source_handoff_rejects_incomplete_v3_report(field: str, value: str) -> None:
    report = _report()
    report[field] = value
    with pytest.raises(RuntimeError, match="not complete"):
        _validate_source_seal_report(report)


def test_source_handoff_rejects_missing_v3_execution_services() -> None:
    report = _report()
    report["missing_from_execution"] = ["new-service"]
    with pytest.raises(RuntimeError, match="missing or incomplete"):
        _validate_source_seal_report(report)


def test_source_handoff_rejects_v3_persisted_count_drift() -> None:
    report = _report()
    report["persisted_count"] -= 1
    with pytest.raises(RuntimeError, match="persisted_count"):
        _validate_source_seal_report(report)


def test_source_handoff_rejects_service_source_ref_drift() -> None:
    report = _report()
    report["services"]["qqmail"]["source_ref"] = "9" * 40
    with pytest.raises(RuntimeError, match="source_ref"):
        _validate_source_seal_report(report)


def test_source_handoff_rejects_unknown_report_schema() -> None:
    report = _report()
    report["schema"] = "popular_rules_source_durable_bridge_v4"
    with pytest.raises(RuntimeError, match="unsupported Source durable report schema"):
        _validate_source_seal_report(report)
