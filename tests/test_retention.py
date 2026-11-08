from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

from scripts.retention import build_plan


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _backup(root: Path, day: str, status: str = "ok") -> Path:
    path = root / "backup" / day
    _write(path / "manifests" / "_collection.json",
           {"schema": "collection_manifest_v1", "date": day,
            "root": f"backup/{day}", "status": status,
            "critical_failures": [] if status == "ok" else ["failed"]})
    return path



def _legacy_backup(root: Path, day: str, *, failed: int = 0,
                   corrupt_hash: bool = False) -> Path:
    path = root / "backup" / day
    payload = b"legacy snapshot test payload"
    local = path / "sources" / "test.yaml"
    local.parent.mkdir(parents=True, exist_ok=True)
    local.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    if corrupt_hash:
        digest = "0" * 64
    _write(path / "manifests" / "_day.json", {
        "date": day, "registry_version": 3,
        "sources": [{
            "source": "legacy", "files_ok": 1, "files_failed": failed,
            "empty_blocked": 0,
            "files": [{"status": "ok", "local": "sources/test.yaml",
                       "size": len(payload), "sha256": digest}]
        }]})
    return path

def _run(root: Path, run_id: str, day: str, *, quality: str = "PASS",
         snapshot_id: str = "snap-20260101T000000000000Z") -> Path:
    path = root / "data" / "runs" / run_id
    _write(path / "run_manifest.json", {
        "schema": "engine_run_v1", "run_id": run_id,
        "started_at": day + "T00:00:00+00:00",
        "collection_manifest": f"backup/{day}/manifests/_collection.json",
        "stages": {"snapshot": {"status": "ok", "snapshot_id": snapshot_id},
                   "ingest": {"status": "ok"}}})
    _write(path / "quality.json", {"decision": quality, "all_hard_pass": quality == "PASS"})
    return path



def _release_evidence(root: Path, run_id: str, snapshot_id: str, day: str) -> None:
    release = root / "data" / "runs" / run_id / "release"
    _write(release / "manifest.json", {
        "schema": "release_manifest_v3", "run_id": run_id,
        "snapshot_id": snapshot_id, "generated_at": day + "T00:00:00+00:00"})
    _write(release / "state.json", {
        "schema": "release_state_v4", "snapshot_id": snapshot_id,
        "all_hard_pass": True, "state": "RC_READY"})
    _write(release / "sbom.json", {
        "schema": "engine_sbom_v1", "run_id": run_id,
        "files": [{"path": "artifacts/client.yaml", "sha256": "abc", "size": 1}]})

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
    assert any(x["path"] == "backup/2026-01-02" and
               x["reason"] == "expired_failed_backup" for x in plan["candidates"])


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


def test_baseline_run_reference_transitively_protects_collection_backup(tmp_path: Path) -> None:
    run_id = "20260101T000000000000Z-run"
    backup = _backup(tmp_path, "2026-01-01")
    _backup(tmp_path, "2026-01-02")
    _run(tmp_path, run_id, "2026-01-01")
    _write(tmp_path / "baseline" / "latest.json", {"source_run_id": run_id})
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "backup/2026-01-01" and
               x["reason"] == "explicitly_referenced_backup" for x in plan["protected"])
    assert not any(x["path"] == "backup/2026-01-01" for x in plan["candidates"])


def test_dangling_run_and_snapshot_references_block_apply(tmp_path: Path) -> None:
    _write(tmp_path / "baseline" / "latest.json", {
        "source_run_id": "20260101T000000000000Z-run",
        "source_snapshot_id": "snap-20260101T000000000001Z"})
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert plan["apply_blocked"] is True
    assert plan["summary"]["dangling_run_reference_count"] == 1
    assert plan["summary"]["dangling_snapshot_reference_count"] == 1


def test_backup_manifest_identity_mismatch_is_protected(tmp_path: Path) -> None:
    path = _backup(tmp_path, "2026-01-01")
    manifest_path = path / "manifests" / "_collection.json"
    doc = json.loads(manifest_path.read_text(encoding="utf-8"))
    doc["date"] = "2025-12-31"
    manifest_path.write_text(json.dumps(doc), encoding="utf-8")
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert not any(x["path"] == "backup/2026-01-01" for x in plan["candidates"])
    assert any(x["path"] == "backup/2026-01-01" and
               x["reason"] == "collection_manifest_identity_mismatch" for x in plan["protected"])


def test_release_evidence_retention_overrides_short_run_retention(tmp_path: Path) -> None:
    run_id = "20260101T000000000000Z-run"
    snapshot_id = "snap-20260101T000000000000Z"
    _run(tmp_path, run_id, "2026-01-01", snapshot_id=snapshot_id)
    _release_evidence(tmp_path, run_id, snapshot_id, "2026-01-01")
    policy = _policy()
    policy["runs"]["keep_min_successful"] = 0
    plan = build_plan(tmp_path, policy, dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == f"data/runs/{run_id}" and
               x["reason"] == "release_evidence_retention_window" for x in plan["protected"])
    assert not any(x["path"] == f"data/runs/{run_id}" for x in plan["candidates"])


def test_expired_release_evidence_allows_old_run_cleanup(tmp_path: Path) -> None:
    old_id = "20250701T000000000000Z-run"
    old_snapshot = "snap-20250701T000000000000Z"
    recent_id = "20260220T000000000000Z-run"
    _run(tmp_path, old_id, "2025-07-01", snapshot_id=old_snapshot)
    _release_evidence(tmp_path, old_id, old_snapshot, "2025-07-01")
    _run(tmp_path, recent_id, "2026-02-20")
    policy = _policy()
    policy["runs"]["keep_min_successful"] = 1
    plan = build_plan(tmp_path, policy, dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == f"data/runs/{old_id}" and
               x["reason"] == "expired_successful_run" for x in plan["candidates"])
    assert any(x["path"] == f"data/runs/{recent_id}" and
               x["reason"] == "minimum_successful_run_retention" for x in plan["protected"])


def test_health_history_outlives_shorter_report_retention(tmp_path: Path) -> None:
    health = tmp_path / "reports" / "2025-12-01" / "source-health.md"
    health.parent.mkdir(parents=True)
    health.write_text("historical health evidence", encoding="utf-8")
    policy = _policy()
    policy["reports"]["keep_days"] = 30
    policy["health_history"] = {"keep_days": 180}
    plan = build_plan(tmp_path, policy, dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "reports/2025-12-01" and
               x["reason"] == "health_history_retention_window" for x in plan["protected"])
    assert not any(x["path"] == "reports/2025-12-01" for x in plan["candidates"])


def test_generated_promotion_keeps_latest_and_180_day_release_evidence(tmp_path: Path) -> None:
    current_id = "20260220T000000000000Z-run"
    current_snapshot = "snap-20260220T000000000000Z"
    current_run = tmp_path / "data" / "runs" / current_id
    _write(current_run / "run_manifest.json", {
        "schema": "engine_run_v1", "run_id": current_id,
        "stages": {"snapshot": {"status": "ok", "snapshot_id": current_snapshot}}})
    promotion = tmp_path / "generated" / "_promotion"
    _write(promotion / "latest.json", {
        "schema": "promotion_v4", "run_id": current_id,
        "snapshot_id": current_snapshot})
    _write(promotion / f"{current_id}.json", {
        "schema": "promotion_v4", "run_id": current_id,
        "snapshot_id": current_snapshot})
    recent_id = "20251201T000000000000Z-run"
    _write(promotion / f"{recent_id}.json", {
        "schema": "promotion_v4", "run_id": recent_id,
        "snapshot_id": "snap-20251201T000000000000Z"})
    old_id = "20250701T000000000000Z-run"
    _write(promotion / f"{old_id}.json", {
        "schema": "promotion_v4", "run_id": old_id,
        "snapshot_id": "snap-20250701T000000000000Z"})
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == f"generated/_promotion/{current_id}.json" and
               x["reason"] == "referenced_promotion_record" for x in plan["protected"])
    assert any(x["path"] == f"generated/_promotion/{recent_id}.json" and
               x["reason"] == "generated_release_evidence_retention_window" for x in plan["protected"])
    assert any(x["path"] == f"generated/_promotion/{old_id}.json" and
               x["reason"] == "expired_generated_promotion_record" for x in plan["candidates"])
    assert any(x["path"] == "generated/_promotion/latest.json" for x in plan["protected"])


def test_legacy_backup_manifest_with_verified_hash_is_successful_and_expires(tmp_path: Path) -> None:
    old = _legacy_backup(tmp_path, "2026-01-01")
    _backup(tmp_path, "2026-02-20")
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "backup/2026-01-01" and
               x["reason"] == "expired_successful_backup" for x in plan["candidates"])
    assert not any(x["path"] == "backup/2026-01-01" for x in plan["protected"])


def test_legacy_partial_backup_expires_after_failed_backup_window(tmp_path: Path) -> None:
    _legacy_backup(tmp_path, "2026-01-01", failed=1)
    _backup(tmp_path, "2026-02-20")
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "backup/2026-01-01" and
               x["reason"] == "expired_failed_backup" for x in plan["candidates"])


def test_legacy_backup_hash_mismatch_is_protected_as_unknown(tmp_path: Path) -> None:
    _legacy_backup(tmp_path, "2026-01-01", corrupt_hash=True)
    _backup(tmp_path, "2026-02-20")
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == "backup/2026-01-01" and
               x["reason"] == "legacy_day_file_hash_mismatch" for x in plan["protected"])
    assert not any(x["path"] == "backup/2026-01-01" for x in plan["candidates"])


def test_retained_release_run_pins_its_collection_backup(tmp_path: Path) -> None:
    run_id = "20260101T000000000000Z-run"
    snapshot_id = "snap-20260101T000000000000Z"
    backup = _backup(tmp_path, "2026-01-01")
    _backup(tmp_path, "2026-02-20")
    _run(tmp_path, run_id, "2026-01-01", snapshot_id=snapshot_id)
    _release_evidence(tmp_path, run_id, snapshot_id, "2026-01-01")
    policy = _policy()
    policy["runs"]["keep_min_successful"] = 0
    plan = build_plan(tmp_path, policy, dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert any(x["path"] == f"data/runs/{run_id}" and
               x["reason"] == "release_evidence_retention_window" for x in plan["protected"])
    assert any(x["path"] == "backup/2026-01-01" and
               x["reason"] == "explicitly_referenced_backup" for x in plan["protected"])
    assert not any(x["path"] == "backup/2026-01-01" for x in plan["candidates"])


def test_missing_backup_from_retained_run_blocks_apply(tmp_path: Path) -> None:
    run_id = "20260101T000000000000Z-run"
    snapshot_id = "snap-20260101T000000000000Z"
    _run(tmp_path, run_id, "2026-01-01", snapshot_id=snapshot_id)
    _release_evidence(tmp_path, run_id, snapshot_id, "2026-01-01")
    policy = _policy()
    policy["runs"]["keep_min_successful"] = 0
    plan = build_plan(tmp_path, policy, dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert plan["apply_blocked"] is True
    assert plan["summary"]["dangling_backup_reference_count"] == 1
    assert any(x["path"] == "backup/2026-01-01/manifests/_collection.json" and
               x["reason"] == "dangling_backup_reference_target_missing" for x in plan["protected"])


def test_run_without_collection_manifest_provenance_is_protected(tmp_path: Path) -> None:
    run_id = "20260101T000000000000Z-run"
    path = _run(tmp_path, run_id, "2026-01-01")
    manifest_path = path / "run_manifest.json"
    doc = json.loads(manifest_path.read_text(encoding="utf-8"))
    doc.pop("collection_manifest")
    manifest_path.write_text(json.dumps(doc), encoding="utf-8")
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert not any(x["path"] == f"data/runs/{run_id}" for x in plan["candidates"])
    assert any(x["path"] == f"data/runs/{run_id}" and
               x["reason"] == "missing_or_invalid_collection_manifest_reference"
               for x in plan["protected"])
    assert plan["apply_blocked"] is True
    assert plan["summary"]["unresolved_run_provenance_count"] == 1


def test_missing_authoritative_baseline_pointer_blocks_apply(tmp_path: Path) -> None:
    (tmp_path / "baseline").mkdir()
    plan = build_plan(tmp_path, _policy(), dt.datetime(2026, 3, 1, tzinfo=dt.timezone.utc))
    assert plan["apply_blocked"] is True
    assert plan["summary"]["invalid_authoritative_pointer_count"] == 1
    assert "baseline/latest.json" in plan["invalid_authoritative_pointers"]
