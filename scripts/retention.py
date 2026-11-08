#!/usr/bin/env python3
"""Conservative, auditable retention planner.

Unknown metadata, unresolved references and non-date layouts are protected.
Dry-run is the default. --apply only removes candidates produced by this planner.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
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
    """Collect run IDs, snapshot IDs and explicit repository paths from pointer/evidence JSON."""
    run_ids: set[str] = set()
    snapshot_ids: set[str] = set()
    paths: set[str] = set()
    scan_roots = [root / "baseline", root / "data" / "baseline",
                  root / "reports", root / "generated"]
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for file in scan_root.rglob("*.json"):
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
                    for v in obj.values():
                        walk(v)
                elif isinstance(obj, list):
                    for v in obj:
                        walk(v)
                elif isinstance(obj, str):
                    normalized = obj.replace("\\", "/").lstrip("./")
                    if normalized and (normalized.startswith(("data/", "backup/", "reports/", "generated/"))):
                        paths.add(normalized)
            walk(doc)
    return run_ids, snapshot_ids, paths


def backup_status(path: Path) -> tuple[str, str | None]:
    manifest = read_json(path / "manifests" / "_collection.json")
    if not manifest:
        return "unknown", "missing_or_invalid_collection_manifest"
    if manifest.get("status") == "ok" and not manifest.get("critical_failures"):
        return "success", None
    if manifest.get("status") in {"failed", "error"} or manifest.get("critical_failures"):
        return "failed", None
    return "unknown", "ambiguous_collection_status"


def run_status(path: Path) -> tuple[str, str | None, str | None]:
    manifest = read_json(path / "run_manifest.json")
    quality = read_json(path / "quality.json")
    if not manifest or not isinstance(manifest.get("stages"), dict):
        return "unknown", None, "missing_or_invalid_run_manifest"
    run_id = manifest.get("run_id")
    if run_id and run_id != path.name:
        return "unknown", None, "run_id_mismatch"
    stages = manifest["stages"]
    statuses = [stage.get("status") for stage in stages.values() if isinstance(stage, dict)]
    if not statuses or any(status not in {"ok", "success"} for status in statuses):
        if any(status in {"failed", "error", "failure"} for status in statuses):
            return "failed", None, None
        return "unknown", None, "ambiguous_stage_status"
    if not quality or quality.get("decision") not in {"PASS", "pass"} or quality.get("all_hard_pass") is False:
        if quality and quality.get("decision") in {"FAIL", "fail"}:
            return "failed", None, None
        return "unknown", None, "missing_or_nonpassing_quality_report"
    snapshot_id = None
    snapshot = stages.get("snapshot")
    if isinstance(snapshot, dict):
        snapshot_id = snapshot.get("snapshot_id")
    return "success", snapshot_id, None


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

    # Backups: retain the newest N successful snapshots, not merely newest dates.
    backup_root = root / "backup"
    backup_cfg = policy.get("backup", {})
    keep_days = int(backup_cfg.get("keep_days", 30))
    min_success = int(backup_cfg.get("keep_min_successful", 7))
    successes: list[tuple[Path, dt.datetime]] = []
    if backup_root.exists():
        for path in sorted(backup_root.iterdir()):
            date = parse_date(path.name)
            if not path.is_dir() or date is None:
                skipped.append(_entry(path, "not_a_dated_backup_directory"))
                continue
            status, why = backup_status(path)
            if status == "success":
                successes.append((path, date))
            else:
                protected.append(_entry(path, why or "backup_not_confirmed_successful"))
        successes.sort(key=lambda pair: pair[1], reverse=True)
        newest_success = {path for path, _ in successes[:min_success]}
        for path, date in successes:
            age = age_days(date, now)
            if path in newest_success:
                protected.append(_entry(path, "minimum_successful_backup_retention"))
            elif age <= keep_days:
                protected.append(_entry(path, "within_backup_retention_window", age))
            elif any(ref == path.relative_to(root).as_posix()
                     or ref.startswith(path.relative_to(root).as_posix() + "/")
                     for ref in path_refs):
                protected.append(_entry(path, "explicitly_referenced_backup", age))
            else:
                candidates.append(_entry(path, "expired_successful_backup", age))

    # Runs: require both a complete successful run manifest and PASS quality report.
    runs_root = root / "data" / "runs"
    runs_cfg = policy.get("runs", {})
    run_keep_days = int(runs_cfg.get("keep_days", 30))
    failed_keep_days = int(policy.get("failed_runs", {}).get("keep_days", 14))
    run_min_success = int(runs_cfg.get("keep_min_successful", 10))
    run_successes: list[tuple[Path, dt.datetime, str | None]] = []
    run_records: list[tuple[Path, dt.datetime, str, str | None]] = []
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
            run_records.append((path, date, status, snapshot_id))
            if status == "success":
                run_successes.append((path, date, snapshot_id))
            elif why:
                protected.append(_entry(path, why, age_days(date, now)))
            elif status == "failed":
                age = age_days(date, now)
                if age <= failed_keep_days:
                    protected.append(_entry(path, "failed_run_within_retention_window", age))
                else:
                    candidates.append(_entry(path, "expired_failed_run", age))
    run_successes.sort(key=lambda item: item[1], reverse=True)
    newest_runs = {path for path, _, _ in run_successes[:run_min_success]}
    for path, date, status, snapshot_id in run_records:
        age = age_days(date, now)
        if status != "success":
            continue
        if path.name in run_refs or (snapshot_id and snapshot_id in snapshot_refs):
            protected.append(_entry(path, "referenced_by_baseline_or_release_pointer", age))
        elif path in newest_runs:
            protected.append(_entry(path, "minimum_successful_run_retention", age))
        elif age <= run_keep_days:
            protected.append(_entry(path, "within_run_retention_window", age))
        else:
            candidates.append(_entry(path, "expired_successful_run", age))

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
            evidence_names = {"audit", "evidence", "release_evidence", "health_history"}
            contains_evidence = any(child.name.lower() in evidence_names for child in path.rglob("*"))
            if contains_evidence:
                protected.append(_entry(path, "contains_audit_or_release_evidence", age))
            elif any(ref == rel or ref.startswith(rel + "/") for ref in path_refs):
                protected.append(_entry(path, "explicitly_referenced_report", age))
            elif age > reports_keep_days:
                candidates.append(_entry(path, "expired_date_partition_report", age))
            else:
                protected.append(_entry(path, "within_report_retention_window", age))

    # These policy classes have no independently verified root/layout in this repo.
    for key, label in (("release_evidence", "release_evidence_layout_not_independently_identified"),
                       ("health_history", "health_history_layout_not_independently_identified"),
                       ("generated", "generated_artifacts_preserved_without_consumer_inventory")):
        if policy.get(key):
            skipped.append({"path": key, "reason": label})

    # Any unresolved baseline run reference is surfaced; it is not silently discarded.
    missing_run_refs = sorted(ref for ref in run_refs if not (runs_root / ref).exists())
    for ref in missing_run_refs:
        protected.append({"path": f"data/runs/{ref}", "reason": "dangling_reference_target_missing"})
    return {
        "schema": "retention_plan_v2",
        "generated_at": now.isoformat(),
        "mode": "dry-run",
        "summary": {"candidate_count": len(candidates), "protected_count": len(protected),
                    "skipped_count": len(skipped), "dangling_run_reference_count": len(missing_run_refs)},
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
