#!/usr/bin/env python3
"""Conservative, auditable retention planner.

Unknown metadata, unresolved references and non-date layouts are protected.
Dry-run is the default. --apply only removes candidates produced by this planner.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "retention.yaml"
RUN_ID_RE = re.compile(r"\b\d{8}T\d{12}Z-run\b")
SNAPSHOT_RE = re.compile(r"\bsnap-\d{8}T\d{12}Z\b")


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_date(value: str) -> dt.datetime | None:
    try:
        return dt.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def age_days(value: dt.datetime, now: dt.datetime) -> int:
    return max(0, (now - value).days)


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def collect_references(root: Path) -> tuple[set[str], set[str], set[str]]:
    """Collect authoritative references and follow run -> snapshot -> backup links."""
    run_ids: set[str] = set()
    snapshot_ids: set[str] = set()
    paths: set[str] = set()
    scan_files = [
        root / "reports" / "latest_release.json",
        root / "generated" / "_promotion" / "latest.json",
    ]
    scan_roots = [root / "baseline", root / "data" / "baseline"]
    for scan_root in scan_roots:
        if scan_root.exists():
            scan_files.extend(scan_root.rglob("*.json"))
    for file in sorted(set(scan_files)):
        if not file.is_file():
            continue
        try:
            raw = file.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        run_ids.update(RUN_ID_RE.findall(raw))
        snapshot_ids.update(SNAPSHOT_RE.findall(raw))
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            continue

        def walk(obj: Any) -> None:
            if isinstance(obj, dict):
                for value in obj.values():
                    walk(value)
            elif isinstance(obj, list):
                for value in obj:
                    walk(value)
            elif isinstance(obj, str):
                normalized = obj.replace("\\", "/")
                while normalized.startswith("./"):
                    normalized = normalized[2:]
                if (normalized and not normalized.startswith("/")
                        and ".." not in Path(normalized).parts
                        and normalized.startswith(("data/", "backup/", "reports/", "generated/"))):
                    paths.add(normalized)
        walk(doc)

    # A baseline/release pointer to a run also pins that run's snapshot and
    # collection manifest. This transitive edge is essential: protecting only
    # data/runs/<id> while deleting its backup manifest breaks provenance.
    runs_root = root / "data" / "runs"
    if runs_root.exists():
        for run_dir in runs_root.iterdir():
            if not run_dir.is_dir():
                continue
            manifest = read_json(run_dir / "run_manifest.json")
            if not manifest:
                continue
            run_id = manifest.get("run_id") or run_dir.name
            stages = manifest.get("stages", {})
            snapshot_stage = stages.get("snapshot", {}) if isinstance(stages, dict) else {}
            snapshot_id = manifest.get("snapshot_id") or (
                snapshot_stage.get("snapshot_id") if isinstance(snapshot_stage, dict) else None
            )
            if run_id in run_ids or (snapshot_id and snapshot_id in snapshot_ids):
                run_ids.add(run_id)
                if snapshot_id:
                    snapshot_ids.add(snapshot_id)
                collection_manifest = manifest.get("collection_manifest")
                if isinstance(collection_manifest, str):
                    normalized = collection_manifest.replace("\\", "/")
                    while normalized.startswith("./"):
                        normalized = normalized[2:]
                    if (normalized and not normalized.startswith("/")
                            and ".." not in Path(normalized).parts
                            and normalized.startswith(("backup/", "data/", "reports/", "generated/"))):
                        paths.add(normalized)
    return run_ids, snapshot_ids, paths

def backup_status(path: Path) -> tuple[str, str | None]:
    manifest = read_json(path / "manifests" / "_collection.json")
    if manifest:
        if (manifest.get("schema") != "collection_manifest_v1"
                or manifest.get("date") != path.name
                or manifest.get("root") != path.relative_to(path.parents[1]).as_posix()):
            return "unknown", "collection_manifest_identity_mismatch"
        if manifest.get("status") == "ok" and not manifest.get("critical_failures"):
            return "success", None
        if manifest.get("status") in {"failed", "error"} or manifest.get("critical_failures"):
            return "failed", "collection_manifest_reports_failure"
        return "unknown", "ambiguous_collection_status"

    # Legacy registry-v3 daily snapshots use _day.json rather than the newer
    # collection manifest. Validate every declared file before treating them as
    # successful; a partial legacy day is a failed backup, not an unknown success.
    legacy = read_json(path / "manifests" / "_day.json")
    if not legacy:
        return "unknown", "missing_or_invalid_collection_manifest"
    if legacy.get("registry_version") != 3 or legacy.get("date") != path.name:
        return "unknown", "legacy_day_manifest_identity_mismatch"
    sources = legacy.get("sources")
    if not isinstance(sources, list) or not sources:
        return "unknown", "legacy_day_manifest_has_no_sources"
    declared_failures = sum(
        int(source.get("files_failed", 0) or 0) + int(source.get("empty_blocked", 0) or 0)
        for source in sources if isinstance(source, dict)
    )
    if declared_failures:
        return "failed", "legacy_day_manifest_partial_failure"
    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("files"), list):
            return "unknown", "legacy_day_source_manifest_invalid"
        files = source["files"]
        if int(source.get("files_ok", 0) or 0) != len(files):
            return "unknown", "legacy_day_file_count_mismatch"
        for item in files:
            if not isinstance(item, dict) or item.get("status") != "ok":
                return "unknown", "legacy_day_file_status_unknown"
            local = item.get("local")
            expected_size = item.get("size")
            expected_hash = item.get("sha256")
            if (not isinstance(local, str) or not local
                    or Path(local).is_absolute() or ".." in Path(local).parts
                    or not isinstance(expected_size, int)
                    or not isinstance(expected_hash, str)
                    or not re.fullmatch(r"[0-9a-f]{64}", expected_hash)):
                return "unknown", "legacy_day_file_identity_invalid"
            if local in seen:
                return "unknown", "legacy_day_duplicate_local_path"
            seen.add(local)
            file_path = path / local
            try:
                resolved = file_path.resolve()
                resolved.relative_to(path.resolve())
                if not resolved.is_file() or resolved.stat().st_size != expected_size:
                    return "unknown", "legacy_day_file_missing_or_size_mismatch"
                digest = hashlib.sha256()
                with resolved.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        digest.update(chunk)
                if digest.hexdigest() != expected_hash:
                    return "unknown", "legacy_day_file_hash_mismatch"
            except (OSError, ValueError):
                return "unknown", "legacy_day_file_unreadable_or_outside_snapshot"
    if not seen:
        return "unknown", "legacy_day_manifest_has_no_files"
    return "success", None

def run_status(path: Path) -> tuple[str, str | None, str | None]:
    manifest = read_json(path / "run_manifest.json")
    quality = read_json(path / "quality.json")
    if (not manifest or not str(manifest.get("schema", "")).startswith("engine_run_")
            or not isinstance(manifest.get("stages"), dict)):
        return "unknown", None, "missing_or_invalid_run_manifest"
    if manifest.get("run_id") != path.name:
        return "unknown", None, "run_id_mismatch"
    collection_manifest = manifest.get("collection_manifest")
    if (not isinstance(collection_manifest, str)
            or not collection_manifest.replace("\\", "/").startswith("backup/")
            or ".." in Path(collection_manifest.replace("\\", "/")).parts):
        return "unknown", None, "missing_or_invalid_collection_manifest_reference"
    stages = manifest["stages"]
    snapshot = stages.get("snapshot")
    if not isinstance(snapshot, dict) or not snapshot.get("snapshot_id"):
        return "unknown", None, "missing_snapshot_stage_identity"
    statuses = [stage.get("status") for stage in stages.values() if isinstance(stage, dict)]
    if len(statuses) != len(stages) or not statuses or any(status not in {"ok", "success"} for status in statuses):
        if any(status in {"failed", "error", "failure"} for status in statuses):
            return "failed", None, None
        return "unknown", None, "ambiguous_stage_status"
    if not quality or quality.get("decision") not in {"PASS", "pass"} or quality.get("all_hard_pass") is not True:
        if quality and quality.get("decision") in {"FAIL", "fail"}:
            return "failed", None, None
        return "unknown", None, "missing_or_nonpassing_quality_report"
    return "success", snapshot.get("snapshot_id"), None



def parse_iso_datetime(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def release_evidence_status(path: Path) -> tuple[str, dt.datetime | None, str | None]:
    """Validate the embedded immutable release evidence for a run directory."""
    release_dir = path / "release"
    if not release_dir.exists():
        return "none", None, None
    manifest = read_json(release_dir / "manifest.json")
    state = read_json(release_dir / "state.json")
    sbom = read_json(release_dir / "sbom.json")
    run_manifest = read_json(path / "run_manifest.json")
    if not all((manifest, state, sbom, run_manifest)):
        return "unknown", None, "incomplete_release_evidence"
    if (manifest.get("schema") != "release_manifest_v3"
            or manifest.get("run_id") != path.name
            or state.get("schema") != "release_state_v4"
            or sbom.get("schema") != "engine_sbom_v1"
            or sbom.get("run_id") != path.name):
        return "unknown", None, "release_evidence_identity_mismatch"
    stages = run_manifest.get("stages", {})
    snapshot = stages.get("snapshot", {}) if isinstance(stages, dict) else {}
    run_snapshot = snapshot.get("snapshot_id") if isinstance(snapshot, dict) else None
    release_snapshot = manifest.get("snapshot_id")
    if (run_manifest.get("run_id") != path.name or not run_snapshot
            or release_snapshot != run_snapshot
            or state.get("snapshot_id") != release_snapshot):
        return "unknown", None, "release_evidence_snapshot_mismatch"
    if not isinstance(sbom.get("files"), list) or not sbom.get("files"):
        return "unknown", None, "release_evidence_sbom_incomplete"
    generated_at = parse_iso_datetime(manifest.get("generated_at"))
    if generated_at is None:
        return "unknown", None, "release_evidence_timestamp_missing"
    return "valid", generated_at, None

def _entry(path: Path, reason: str, age: int | None = None) -> dict[str, Any]:
    try:
        relative = path.relative_to(ROOT).as_posix()
    except ValueError:
        # Keep planner tests hermetic when they operate on a temporary repository.
        markers = {"backup", "reports", "generated", "data", "baseline"}
        parts = path.parts
        index = next((i for i, part in enumerate(parts) if part in markers), None)
        relative = Path(*parts[index:]).as_posix() if index is not None else path.name
    item: dict[str, Any] = {"path": relative, "reason": reason}
    if age is not None:
        item["age_days"] = age
    return item


def build_plan(root: Path = ROOT, policy: dict[str, Any] | None = None,
               now: dt.datetime | None = None) -> dict[str, Any]:
    if policy is None:
        import yaml
        policy = yaml.safe_load((root / "config" / "retention.yaml").read_text(encoding="utf-8")) or {}
    now = now or now_utc()
    run_refs, snapshot_refs, path_refs = collect_references(root)
    protected: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    # Runs: keep run payloads 30d, but preserve embedded release evidence for 180d.
    # Until an external artifact store is authoritative, release evidence lives inside
    # each run directory; deleting that directory would silently violate the 180d policy.
    runs_root = root / "data" / "runs"
    runs_cfg = policy.get("runs", {})
    run_keep_days = int(runs_cfg.get("keep_days", 30))
    failed_keep_days = int(policy.get("failed_runs", {}).get("keep_days", 14))
    run_min_success = int(runs_cfg.get("keep_min_successful", 10))
    release_keep_days = int(policy.get("release_evidence", {}).get("keep_days", 180))
    run_successes: list[tuple[Path, dt.datetime, str | None]] = []
    run_records: list[tuple[Path, dt.datetime, str, str | None, str, dt.datetime | None, str | None]] = []
    if runs_root.exists():
        for path in sorted(runs_root.iterdir()):
            match = re.fullmatch(r"(\d{8})T(\d{12})Z-run", path.name)
            if not path.is_dir() or not match:
                skipped.append(_entry(path, "unrecognized_run_directory_name"))
                continue
            try:
                date = dt.datetime.strptime(match.group(1) + match.group(2)[:6], "%Y%m%d%H%M%S").replace(tzinfo=dt.timezone.utc)
            except ValueError:
                protected.append(_entry(path, "invalid_run_timestamp"))
                continue
            status, snapshot_id, why = run_status(path)
            evidence_status, evidence_at, evidence_why = release_evidence_status(path)
            run_records.append((path, date, status, snapshot_id, evidence_status, evidence_at, evidence_why))
            if status == "success":
                run_successes.append((path, date, snapshot_id))
    run_successes.sort(key=lambda item: item[1], reverse=True)
    newest_runs = {path for path, _, _ in run_successes[:run_min_success]}
    for path, date, status, snapshot_id, evidence_status, evidence_at, evidence_why in run_records:
        age = age_days(date, now)
        evidence_age = age_days(evidence_at, now) if evidence_at else None
        if path.name in run_refs or (snapshot_id and snapshot_id in snapshot_refs):
            protected.append(_entry(path, "referenced_by_baseline_or_release_pointer", age))
        elif path in newest_runs:
            protected.append(_entry(path, "minimum_successful_run_retention", age))
        elif evidence_status == "unknown":
            protected.append(_entry(path, evidence_why or "release_evidence_unverifiable", age))
        elif evidence_status == "valid" and evidence_age is not None and evidence_age <= release_keep_days:
            protected.append(_entry(path, "release_evidence_retention_window", evidence_age))
        elif status == "failed":
            if age <= failed_keep_days:
                protected.append(_entry(path, "failed_run_within_retention_window", age))
            else:
                candidates.append(_entry(path, "expired_failed_run", age))
        elif status == "success":
            if age <= run_keep_days:
                protected.append(_entry(path, "within_run_retention_window", age))
            else:
                candidates.append(_entry(path, "expired_successful_run", age))
        else:
            protected.append(_entry(path, "run_status_unknown", age))


    # Any run whose collection provenance cannot be resolved blocks destructive cleanup.
    unresolved_run_provenance: list[str] = []
    for path, _, _, _, _, _, _ in run_records:
        manifest = read_json(path / "run_manifest.json")
        collection_manifest = manifest.get("collection_manifest") if manifest else None
        if (not isinstance(collection_manifest, str)
                or not collection_manifest.replace("\\", "/").startswith("backup/")
                or ".." in Path(collection_manifest.replace("\\", "/")).parts):
            unresolved_run_provenance.append(path.relative_to(root).as_posix())

    # Every retained run pins the collection manifest it was built from, not only
    # runs named by the latest baseline/release pointers.
    for item in protected:
        relative = item.get("path", "")
        if not relative.startswith("data/runs/") or relative.count("/") != 2:
            continue
        run_manifest = read_json(root / relative / "run_manifest.json")
        if not run_manifest:
            continue
        collection_manifest = run_manifest.get("collection_manifest")
        if not isinstance(collection_manifest, str):
            continue
        normalized = collection_manifest.replace("\\", "/")
        while normalized.startswith("./"):
            normalized = normalized[2:]
        if (normalized.startswith("backup/")
                and ".." not in Path(normalized).parts):
            path_refs.add(normalized)

    # Backups: retain the newest N successful snapshots, not merely newest dates.
    backup_root = root / "backup"
    backup_cfg = policy.get("backup", {})
    keep_days = int(backup_cfg.get("keep_days", 30))
    min_success = int(backup_cfg.get("keep_min_successful", 7))
    successes: list[tuple[Path, dt.datetime]] = []
    backup_records: list[tuple[Path, dt.datetime, str, str | None]] = []
    if backup_root.exists():
        for path in sorted(backup_root.iterdir()):
            date = parse_date(path.name)
            if not path.is_dir() or date is None:
                skipped.append(_entry(path, "not_a_dated_backup_directory"))
                continue
            status, why = backup_status(path)
            backup_records.append((path, date, status, why))
            if status == "success":
                successes.append((path, date))
    successes.sort(key=lambda pair: pair[1], reverse=True)
    newest_success = {path for path, _ in successes[:min_success]}
    failed_backup_keep_days = int(backup_cfg.get("failed_keep_days", 14))
    for path, date, status, why in backup_records:
        age = age_days(date, now)
        if status == "unknown":
            protected.append(_entry(path, why or "backup_status_unknown", age))
        elif status == "failed":
            if age <= failed_backup_keep_days:
                protected.append(_entry(path, "failed_backup_within_retention_window", age))
            else:
                candidates.append(_entry(path, "expired_failed_backup", age))
        elif path in newest_success:
            protected.append(_entry(path, "minimum_successful_backup_retention", age))
        elif age <= keep_days:
            protected.append(_entry(path, "within_backup_retention_window", age))
        elif any(ref == path.relative_to(root).as_posix()
                 or ref.startswith(path.relative_to(root).as_posix() + "/")
                 for ref in path_refs):
            protected.append(_entry(path, "explicitly_referenced_backup", age))
        else:
            candidates.append(_entry(path, "expired_successful_backup", age))

    # Reports: only direct date-partition directories are eligible. Audit and archive
    # subtrees, unknown layouts and explicitly referenced paths are never traversed.
    reports_root = root / "reports"
    reports_cfg = policy.get("reports", {})
    reports_keep_days = int(reports_cfg.get("keep_days", 90))
    if reports_root.exists():
        for path in sorted(reports_root.iterdir()):
            date = parse_date(path.name)
            if not path.is_dir() or date is None:
                skipped.append(_entry(path, "non_date_report_area_preserved"))
                continue
            age = age_days(date, now)
            rel = path.relative_to(root).as_posix()
            evidence_names = {"audit", "evidence", "release", "release_evidence", "health_history"}
            contains_evidence = any(child.name.lower() in evidence_names for child in path.rglob("*"))
            has_health_history = any(
                file.is_file() and file.name.lower().startswith(("source-health", "health-history"))
                for file in path.rglob("*")
            )
            health_keep_days = int(policy.get("health_history", {}).get("keep_days", 180))
            audit_keep_days = int(policy.get("lifecycle", {}).get("audit_days", 180))
            if contains_evidence and age <= max(reports_keep_days, audit_keep_days, release_keep_days):
                protected.append(_entry(path, "contains_retained_audit_or_release_evidence", age))
            elif has_health_history and age <= health_keep_days:
                protected.append(_entry(path, "health_history_retention_window", age))
            elif any(ref == rel or ref.startswith(rel + "/") for ref in path_refs):
                protected.append(_entry(path, "explicitly_referenced_report", age))
            elif age > reports_keep_days:
                candidates.append(_entry(path, "expired_date_partition_report", age))
            else:
                protected.append(_entry(path, "within_report_retention_window", age))

    # Generated client directories are the current distribution, not history.
    generated_root = root / "generated"
    if generated_root.exists():
        skipped.append({"path": "generated", "reason": "current_generated_distribution_preserved"})
    promotion_root = generated_root / "_promotion"
    if promotion_root.exists():
        for path in sorted(promotion_root.iterdir()):
            if path.name == "latest.json":
                protected.append(_entry(path, "authoritative_latest_promotion_pointer"))
                continue
            match = re.fullmatch(r"(\d{8})T(\d{12})Z-run\.json", path.name)
            if not path.is_file() or not match:
                skipped.append(_entry(path, "unrecognized_promotion_record_preserved"))
                continue
            doc = read_json(path)
            run_id = path.stem
            if not doc or doc.get("schema") != "promotion_v4" or doc.get("run_id") != run_id:
                protected.append(_entry(path, "promotion_record_identity_unknown"))
                continue
            try:
                promoted_at = dt.datetime.strptime(
                    match.group(1) + match.group(2)[:6], "%Y%m%d%H%M%S"
                ).replace(tzinfo=dt.timezone.utc)
            except ValueError:
                protected.append(_entry(path, "invalid_promotion_timestamp"))
                continue
            age = age_days(promoted_at, now)
            snapshot_id = doc.get("snapshot_id")
            rel = path.relative_to(root).as_posix()
            if run_id in run_refs or (snapshot_id and snapshot_id in snapshot_refs) or rel in path_refs:
                protected.append(_entry(path, "referenced_promotion_record", age))
            elif age <= release_keep_days:
                protected.append(_entry(path, "generated_release_evidence_retention_window", age))
            else:
                candidates.append(_entry(path, "expired_generated_promotion_record", age))

    # Any unresolved baseline run reference is surfaced; it is not silently discarded.
    missing_backup_refs = sorted(
        ref for ref in path_refs
        if ref.startswith("backup/") and not (root / ref).exists()
    )
    for ref in missing_backup_refs:
        protected.append({"path": ref, "reason": "dangling_backup_reference_target_missing"})
    existing_run_ids: set[str] = set()
    existing_snapshot_ids: set[str] = set()
    if runs_root.exists():
        for run_dir in runs_root.iterdir():
            if not run_dir.is_dir():
                continue
            manifest = read_json(run_dir / "run_manifest.json")
            if not manifest:
                continue
            existing_run_ids.add(str(manifest.get("run_id") or run_dir.name))
            stages = manifest.get("stages", {})
            snapshot = stages.get("snapshot", {}) if isinstance(stages, dict) else {}
            snapshot_id = manifest.get("snapshot_id") or (
                snapshot.get("snapshot_id") if isinstance(snapshot, dict) else None
            )
            if snapshot_id:
                existing_snapshot_ids.add(str(snapshot_id))
    missing_run_refs = sorted(ref for ref in run_refs if ref not in existing_run_ids)
    missing_snapshot_refs = sorted(ref for ref in snapshot_refs if ref not in existing_snapshot_ids)
    for ref in missing_run_refs:
        protected.append({"path": f"data/runs/{ref}", "reason": "dangling_run_reference_target_missing"})
    for ref in missing_snapshot_refs:
        protected.append({"path": f"snapshot/{ref}", "reason": "dangling_snapshot_reference_target_missing"})
    blocking_issues = []
    if missing_run_refs:
        blocking_issues.append("dangling_run_references")
    if missing_snapshot_refs:
        blocking_issues.append("dangling_snapshot_references")
    if missing_backup_refs:
        blocking_issues.append("dangling_backup_references")
    if unresolved_run_provenance:
        blocking_issues.append("unresolved_run_provenance")
    return {
        "schema": "retention_plan_v2",
        "generated_at": now.isoformat(),
        "mode": "dry-run",
        "apply_blocked": bool(blocking_issues),
        "blocking_issues": blocking_issues,
        "unresolved_run_provenance": sorted(unresolved_run_provenance),
        "summary": {"candidate_count": len(candidates), "protected_count": len(protected),
                    "skipped_count": len(skipped), "dangling_run_reference_count": len(missing_run_refs),
                    "dangling_snapshot_reference_count": len(missing_snapshot_refs),
                    "dangling_backup_reference_count": len(missing_backup_refs),
                    "unresolved_run_provenance_count": len(unresolved_run_provenance)},
        "candidates": sorted(candidates, key=lambda x: x["path"]),
        "protected": sorted(protected, key=lambda x: x["path"]),
        "skipped": sorted(skipped, key=lambda x: x["path"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="delete only planner-approved candidates")
    parser.add_argument("--dry-run", action="store_true", help="preview without changing files (default)")
    parser.add_argument("--json", dest="json_path", help="write the complete plan to this JSON path")
    args = parser.parse_args()
    if args.apply and args.dry_run:
        parser.error("--apply and --dry-run are mutually exclusive")
    import yaml
    policy = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
    plan = build_plan(ROOT, policy)
    plan["mode"] = "apply" if args.apply else "dry-run"
    output = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    print(output, end="")
    if args.json_path:
        target = Path(args.json_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
    if args.apply and plan.get("apply_blocked"):
        print("retention apply refused: unresolved authoritative run/snapshot references", file=sys.stderr)
        return 2
    if args.apply:
        for item in plan["candidates"]:
            target = ROOT / item["path"]
            # Guard against path traversal and accidental root deletion.
            resolved = target.resolve()
            if ROOT.resolve() not in resolved.parents:
                raise RuntimeError(f"refusing path outside repository: {target}")
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
