"""Artifact Promotion & Rollback.

Promotion is allowed only after Release State == RC_READY. Artifacts are
staged in a sibling directory and swapped atomically; baseline advancement is
part of the same commit point and is rolled back if it cannot be completed.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_CLIENTS = {
    "mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon"
}
PUBLISHABLE_SUFFIXES = {".yaml", ".json", ".list"}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _artifact_digests(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not root.exists():
        return out
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix in PUBLISHABLE_SUFFIXES:
            out[str(path.relative_to(root))] = _sha256_file(path)
    return out


def _client_digests(root: Path) -> dict[str, str]:
    return {client: _dir_digest(root / client) for client in sorted(EXPECTED_CLIENTS)}


def _dir_digest(path: Path) -> str | None:
    if not path.exists() or not path.is_dir():
        return None
    items = []
    for p in sorted(path.rglob("*")):
        if p.is_file() and p.suffix in PUBLISHABLE_SUFFIXES:
            items.append((str(p.relative_to(path)), _sha256_file(p)))
    if not items:
        return None
    return hashlib.sha256(json.dumps(items, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _copy_baseline(canonical_rules: Path, baseline_path: Path) -> tuple[str, Path]:
    if not canonical_rules.exists() or canonical_rules.stat().st_size == 0:
        raise RuntimeError("Cannot advance baseline: canonical rules are missing or empty")
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    temp = baseline_path.with_name(f".{baseline_path.name}.tmp-{canonical_rules.stat().st_ino}")
    shutil.copy2(canonical_rules, temp)
    return _sha256_file(temp), temp


def _validate_release_artifact_set(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    release_dir = run_dir / "release"
    state_path = release_dir / "state.json"
    manifest_path = release_dir / "manifest.json"
    golden_path = run_dir / "golden" / "report.json"
    artifacts_root = run_dir / "artifacts"

    if not state_path.exists() or not manifest_path.exists():
        raise RuntimeError("Rollback/promotion requires release state and release manifest")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if state.get("state") != "RC_READY":
        raise RuntimeError(f"Release state is {state.get('state')}, not RC_READY")
    if manifest.get("run_id") != run_dir.name:
        raise RuntimeError("Release manifest run_id does not match run directory")
    if manifest.get("release_state") != "RC_READY":
        raise RuntimeError("Release manifest is not RC_READY")
    if not golden_path.exists():
        raise RuntimeError("Missing Golden report")
    golden = json.loads(golden_path.read_text(encoding="utf-8"))
    if golden.get("all_pass") is not True:
        raise RuntimeError("Rollback/promotion requires Golden all_pass=true")
    if not artifacts_root.exists():
        raise RuntimeError("Missing artifact root")

    actual_clients = {p.name for p in artifacts_root.iterdir() if p.is_dir()}
    missing = sorted(EXPECTED_CLIENTS - actual_clients)
    if missing:
        raise RuntimeError(f"Missing client artifacts: {', '.join(missing)}")
    client_digests = _client_digests(artifacts_root)
    missing_content = [c for c, d in client_digests.items() if not d]
    if missing_content:
        raise RuntimeError(f"Client artifacts are empty: {', '.join(missing_content)}")

    canonical = run_dir / "canonical" / "rules.jsonl"
    ir = run_dir / "ir" / "ir.json"
    diff = run_dir / "reports" / "diff" / "latest.json"
    if not canonical.exists() or canonical.stat().st_size == 0:
        raise RuntimeError("Missing/empty canonical rules")
    if not ir.exists() or ir.stat().st_size == 0:
        raise RuntimeError("Missing/empty IR")
    if not diff.exists():
        raise RuntimeError("Missing Diff report")

    artifact_digests = _artifact_digests(artifacts_root)
    if manifest.get("client_digests") != client_digests:
        raise RuntimeError("Release manifest client digests do not match artifacts")
    if manifest.get("canonical_digest") != _sha256_file(canonical):
        raise RuntimeError("Release manifest canonical digest mismatch")
    if manifest.get("ir_digest") != _sha256_file(ir):
        raise RuntimeError("Release manifest IR digest mismatch")
    if manifest.get("golden_digest") != _sha256_file(golden_path):
        raise RuntimeError("Release manifest Golden digest mismatch")
    if manifest.get("diff_digest") != _sha256_file(diff):
        raise RuntimeError("Release manifest Diff digest mismatch")

    return {
        "release_state": state,
        "release_manifest": manifest,
        "golden": golden,
        "artifact_digests": artifact_digests,
    }


def promote_run(
    run_dir: Path,
    generated_root: Path,
    *,
    force: bool = False,
    baseline_path: Path | None = None,
) -> dict[str, Any]:
    run_dir = Path(run_dir)
    generated_root = Path(generated_root)
    validation = _validate_release_artifact_set(run_dir)
    if force:
        # Kept as an explicit API parameter for compatibility, but never bypasses
        # release integrity validation. Recovery must be based on a valid RC_READY run.
        pass

    src_art = run_dir / "artifacts"
    generated_root.parent.mkdir(parents=True, exist_ok=True)
    staging = generated_root.parent / f".{generated_root.name}.staging-{run_dir.name}"
    backup = generated_root.parent / f".{generated_root.name}.previous-{run_dir.name}"
    if staging.exists():
        shutil.rmtree(staging)
    if backup.exists():
        shutil.rmtree(backup)

    baseline_temp: Path | None = None
    baseline_target: Path | None = Path(baseline_path) if baseline_path is not None else None
    old_baseline: Path | None = None
    old_baseline_backup: Path | None = None
    try:
        staging.mkdir(parents=True)
        for client_dir in sorted(src_art.iterdir()):
            if client_dir.is_dir():
                shutil.copytree(client_dir, staging / client_dir.name)

        digests = _artifact_digests(staging)
        if not digests:
            raise RuntimeError("Promotion refused: no publishable artifacts")

        promotion_time = datetime.now(timezone.utc).isoformat()
        record = {
            "schema": "promotion_v3",
            "promoted_at": promotion_time,
            "run_id": run_dir.name,
            "release_state": "RC_READY",
            "snapshot_id": validation["release_manifest"].get("snapshot_id"),
            "v2_runtime_dependency": 0,
            "artifact_count": len(digests),
            "artifact_digests": digests,
            "client_digests": validation["release_manifest"].get("client_digests"),
        }
        (staging / "_promotion").mkdir(parents=True, exist_ok=True)
        (staging / "_promotion" / "latest.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        if baseline_target is not None:
            baseline_digest, baseline_temp = _copy_baseline(
                run_dir / "canonical" / "rules.jsonl", baseline_target
            )
            record["baseline_path"] = str(baseline_target)
            record["baseline_digest"] = baseline_digest

        if generated_root.exists():
            generated_root.rename(backup)
        staging.rename(generated_root)

        if baseline_temp is not None and baseline_target is not None:
            old_baseline = baseline_target
            if old_baseline.exists():
                old_baseline_backup = old_baseline.with_name(f".{old_baseline.name}.previous-{run_dir.name}")
                if old_baseline_backup.exists():
                    old_baseline_backup.unlink()
                old_baseline.rename(old_baseline_backup)
            baseline_temp.rename(old_baseline)

        history = generated_root / "_promotion"
        history.mkdir(exist_ok=True)
        (history / "latest.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (history / f"{run_dir.name}.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        if backup.exists():
            shutil.rmtree(backup)
        if old_baseline_backup and old_baseline_backup.exists():
            old_baseline_backup.unlink()
        return record
    except Exception:
        if generated_root.exists() and backup.exists():
            shutil.rmtree(generated_root)
            backup.rename(generated_root)
        elif backup.exists() and not generated_root.exists():
            backup.rename(generated_root)
        if baseline_temp and baseline_temp.exists():
            baseline_temp.unlink()
        if old_baseline_backup and old_baseline_backup.exists() and old_baseline and not old_baseline.exists():
            old_baseline_backup.rename(old_baseline)
        raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
        if backup.exists():
            shutil.rmtree(backup)


def rollback_to_run(
    run_id: str,
    runs_root: Path,
    generated_root: Path,
) -> dict[str, Any]:
    """Rollback only to a fully validated RC_READY run with matching digests."""
    run_dir = Path(runs_root) / run_id
    return promote_run(run_dir, generated_root, force=False)
