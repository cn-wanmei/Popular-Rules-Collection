"""Artifact Promotion & Rollback.

Promote only after Release State == RC_READY.
Promotion copies immutable run artifacts into data/generated/ (or generated/).
Rollback restores a previous promoted run.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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

    # copy native client artifacts
    src_art = run_dir / "artifacts"
    if not src_art.exists():
        raise RuntimeError("No artifacts to promote")

    generated_root.mkdir(parents=True, exist_ok=True)
    # clear previous generated clients (safe promote)
    for client_dir in src_art.iterdir():
        if client_dir.is_dir():
            dest = generated_root / client_dir.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(client_dir, dest)

    # write promotion record
    record = {
        "schema": "promotion_v1",
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "run_id": run_dir.name,
        "release_state": state.get("state"),
        "v2_runtime_dependency": 0,
    }
    prom_dir = generated_root / "_promotion"
    prom_dir.mkdir(exist_ok=True)
    (prom_dir / "latest.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    # keep history
    (prom_dir / f"{run_dir.name}.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return record


def rollback_to_run(
    run_id: str,
    runs_root: Path,
    generated_root: Path,
) -> dict[str, Any]:
    """
    Rollback generated/ to a previous successful run.
    """
    run_dir = Path(runs_root) / run_id
    if not run_dir.exists():
        raise FileNotFoundError(f"Run not found: {run_dir}")
    # force promote the old run
    return promote_run(run_dir, generated_root, force=True)
