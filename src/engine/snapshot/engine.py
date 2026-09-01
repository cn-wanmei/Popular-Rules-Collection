"""Source Snapshot Engine — V2-free, first stage of every pipeline run.

Snapshot = the entire immutable input boundary for one build.
All subsequent stages bind to snapshot_id.
Never call snapshot_v2_oracle. Never read database/services at runtime.
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


def create_source_snapshot(
    sources_root: Path,
    snapshots_dir: Path,
    *,
    snapshot_id: str | None = None,
    extra_meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Freeze current sources into an immutable snapshot.
    sources_root: directory containing the raw/structured inputs to freeze
    snapshots_dir: data/snapshots/
    Returns manifest.
    """
    sources_root = Path(sources_root)
    snapshots_dir = Path(snapshots_dir)
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    if not snapshot_id:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        snapshot_id = f"snap-{ts}"

    snap_dir = snapshots_dir / snapshot_id
    if snap_dir.exists():
        raise FileExistsError(f"Snapshot already exists: {snap_dir}")

    dest_sources = snap_dir / "sources"
    dest_sources.mkdir(parents=True)

    file_digests: dict[str, str] = {}
    if sources_root.is_dir():
        for src in sorted(sources_root.rglob("*")):
            if src.is_file():
                rel = src.relative_to(sources_root)
                target = dest_sources / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
                file_digests[str(rel)] = _sha256_file(target)

    manifest = {
        "schema": "source_snapshot_v1",
        "snapshot_id": snapshot_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "engine_version": "1.0.1",
        "v2_runtime_dependency": 0,
        "file_count": len(file_digests),
        "file_digests": file_digests,
        "extra": extra_meta or {},
    }
    (snap_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def load_snapshot_manifest(snapshot_dir: Path) -> dict[str, Any]:
    path = Path(snapshot_dir) / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"No manifest.json in {snapshot_dir}")
    return json.loads(path.read_text(encoding="utf-8"))
