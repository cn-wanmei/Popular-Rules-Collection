from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from scripts.retention import build_plan


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _backup(root: Path, day: str, status: str = "ok") -> Path:
    path = root / "backup" / day
    _write(path / "manifests" / "_collection.json",
           {"status": status, "critical_failures": [] if status == "ok" else ["failed"]})
    return path


def _run(root: Path, run_id: str, day: str, *, quality: str = "PASS",
         snapshot_id: str = "snap-20260101T000000000000Z") -> Path:
    path = root / "data" / "runs" / run_id
    _write(path / "run_manifest.json", {
        "run_id": run_id, "started_at": day + "T00:00:00+00:00",
        "stages": {"snapshot": {"status": "ok", "snapshot_id": snapshot_id},
                   "ingest": {"status": "ok"}}})
    _write(path / "quality.json", {"decision": quality, "all_hard_pass": quality == "PASS"})
    return path


def _policy() -> dict:
    return {"backup": {"keep_days": 30, "keep_min_successful": 1},
            "runs": {"keep_days": 30, "keep_min_successful": 1},
            "failed_runs": {"keep_days": 14}, "reports": {"keep_days": 90},
            "release_evidence": {"keep_days": 180}, "health_history": {"keep_days": 180},
            "generated": {"keep_latest_only": True}}


def test_backup_minimum_counts_successful_not_newest_directories(tmp_path: Path) -> None:
    old = _backup(tmp_path, "2026-01-01")
    _backup(tmp_path, "2026-01-02", status="failed")
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "backup/2026-01-01" and x["reason"] == "minimum_successful_backup_retention"
               for x in plan["protected"])
    assert not any(x["path"] == "backup/2026-01-02" for x in plan["candidates"])


def test_timestamp_run_id_is_parsed_and_baseline_reference_protects_run(tmp_path: Path) -> None:
    run_id = "20260101T000000000000Z-run"
    run = _run(tmp_path, run_id, "2026-01-01")
    _write(tmp_path / "baseline" / "latest.json", {"source_run_id": run_id})
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert run.exists()
    assert any(x["path"] == f"data/runs/{run_id}" and
               x["reason"] == "referenced_by_baseline_or_release_pointer" for x in plan["protected"])


def test_unknown_run_metadata_is_never_a_delete_candidate(tmp_path: Path) -> None:
    run_id = "20260101T000000000000Z-run"
    path = tmp_path / "data" / "runs" / run_id
    path.mkdir(parents=True)
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert not any(x["path"] == f"data/runs/{run_id}" for x in plan["candidates"])
    assert any(x["reason"] == "missing_or_invalid_run_manifest" for x in plan["protected"])


def test_reports_only_date_partition_directories_are_considered(tmp_path: Path) -> None:
    old = tmp_path / "reports" / "2025-01-01"
    old.mkdir(parents=True)
    audit = tmp_path / "reports" / "audit"
    audit.mkdir(parents=True)
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "reports/2025-01-01" for x in plan["candidates"])
    assert any(x["path"] == "reports/audit" and x["reason"] == "non_date_report_area_preserved"
               for x in plan["skipped"])


def test_nested_backup_reference_protects_snapshot_directory(tmp_path: Path) -> None:
    old = _backup(tmp_path, "2026-01-01")
    _backup(tmp_path, "2026-01-02")
    _write(tmp_path / "baseline" / "latest.json",
           {"backup_manifest": "backup/2026-01-01/manifests/_collection.json"})
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "backup/2026-01-01" and
               x["reason"] == "explicitly_referenced_backup" for x in plan["protected"])
    assert not any(x["path"] == "backup/2026-01-01" for x in plan["candidates"])


def test_prior_retention_plan_is_not_treated_as_authoritative_reference(tmp_path: Path) -> None:
    _backup(tmp_path, "2026-01-01")
    _backup(tmp_path, "2026-01-02")
    _write(tmp_path / "reports" / "retention_plan.json", {
        "candidates": [{"path": "backup/2026-01-01"}]})
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "backup/2026-01-01" for x in plan["candidates"])
