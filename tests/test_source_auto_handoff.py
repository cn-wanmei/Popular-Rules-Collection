from __future__ import annotations

import pytest

from scripts.source_auto_handoff import (
    LINEAGE_SERVICES,
    _validate_source_seal_report,
    _lifecycle_eligible,
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


def test_handoff_workflow_propagates_python_pipeline_failures() -> None:
    from pathlib import Path

    import yaml

    root = Path(__file__).resolve().parents[1]
    workflow = yaml.safe_load(
        (root / ".github" / "workflows" / "source-auto-handoff.yml").read_text(encoding="utf-8")
    )
    triggers = workflow.get("on", workflow.get(True, {}))
    push = triggers.get("push", {})
    assert push.get("branches") == ["main"]
    assert {
        "scripts/source_auto_handoff.py",
        ".github/workflows/source-auto-handoff.yml",
    } <= set(push.get("paths", []))

    jobs = workflow["jobs"]
    steps = jobs["handoff"]["steps"]
    step = next(item for item in steps if item.get("name") == "Materialize and verify current Source durable seal")
    assert step.get("shell") == "bash"
    assert "set -euo pipefail" in step.get("run", "")



def test_lifecycle_handoff_allows_only_enabled_verified_or_production() -> None:
    assert _lifecycle_eligible({"state": "production", "enabled": True})
    assert _lifecycle_eligible({"state": "verified", "enabled": True})
    assert not _lifecycle_eligible({"state": "canary", "enabled": True})
    assert not _lifecycle_eligible({"state": "review", "enabled": True})
    assert not _lifecycle_eligible({"state": "production", "enabled": False})
    assert not _lifecycle_eligible({})
