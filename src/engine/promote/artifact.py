"""Artifact Promotion & Rollback.

Promotion is allowed only after Release State == RC_READY unless explicitly
requested through the manual --force rollback/recovery path. Artifacts are
staged in a temporary sibling directory and swapped atomically so generated/
never becomes partially updated.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
        if path.is_file() and path.suffix in {".yaml", ".json", ".list"}:
            out[str(path.relative_to(root))] = _sha256_file(path)
    return out


def promote_run(
    run_dir: Path,
    generated_root: Path,
    *,
    force: bool = False,
) -> dict[str, Any]:
    run_dir = Path(run_dir)
    generated_root = Path(generated_root)

    state_path = run_dir / "release" / "state.json"
    if not state_path.exists():
        raise RuntimeError("No release state — cannot promote")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("state") != "RC_READY" and not force:
        raise RuntimeError(f"Release state is {state.get('state')}, not RC_READY")

    src_art = run_dir / "artifacts"
    if not src_art.exists():
        raise RuntimeError("No artifacts to promote")

    expected_clients = {
        "mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon"
    }
    actual_clients = {p.name for p in src_art.iterdir() if p.is_dir()}
    missing = sorted(expected_clients - actual_clients)
    if missing:
        raise RuntimeError(f"Missing client artifacts: {', '.join(missing)}")

    generated_root.parent.mkdir(parents=True, exist_ok=True)
    staging = generated_root.parent / f".{generated_root.name}.staging-{run_dir.name}"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    try:
        for client_dir in sorted(src_art.iterdir()):
            if client_dir.is_dir():
                shutil.copytree(client_dir, staging / client_dir.name)

        digests = _artifact_digests(staging)
        if not digests:
            raise RuntimeError("Promotion refused: no publishable artifacts")

        promotion_time = datetime.now(timezone.utc).isoformat()
        record = {
            "schema": "promotion_v2",
            "promoted_at": promotion_time,
            "run_id": run_dir.name,
            "release_state": state.get("state"),
            "v2_runtime_dependency": 0,
            "artifact_count": len(digests),
            "artifact_digests": digests,
        }
        (staging / "_promotion").mkdir(parents=True, exist_ok=True)
        (staging / "_promotion" / "latest.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        backup = generated_root.parent / f".{generated_root.name}.previous-{run_dir.name}"
        if backup.exists():
            shutil.rmtree(backup)
        if generated_root.exists():
            generated_root.rename(backup)
        try:
            staging.rename(generated_root)
        except Exception:
            if backup.exists() and not generated_root.exists():
                backup.rename(generated_root)
            raise
        finally:
            if backup.exists():
                shutil.rmtree(backup)

        # Keep a history record outside the atomic client tree as well.
        history = generated_root / "_promotion"
        history.mkdir(exist_ok=True)
        (history / f"{run_dir.name}.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return record
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def rollback_to_run(
    run_id: str,
    runs_root: Path,
    generated_root: Path,
) -> dict[str, Any]:
    """Rollback to a previously generated run after validating its release state."""
    run_dir = Path(runs_root) / run_id
    if not run_dir.exists():
        raise FileNotFoundError(f"Run not found: {run_dir}")
    state_path = run_dir / "release" / "state.json"
    if not state_path.exists():
        raise RuntimeError(f"Run has no release state: {run_id}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("state") != "RC_READY":
        raise RuntimeError(f"Rollback target is not RC_READY: {run_id}")
    return promote_run(run_dir, generated_root, force=False)
