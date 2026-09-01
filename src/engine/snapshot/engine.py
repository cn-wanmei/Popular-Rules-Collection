"""Source Snapshot Engine — V2-free, immutable input boundary with CAS refs."""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.cas.store import put_file


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

    # CAS lives beside snapshots: data/cas/objects/<sha>. The snapshot remains
    # self-contained on disk while its manifest now records reusable identities.
    cas_root = snapshots_dir.parent / "cas" / "objects"
    file_digests: dict[str, str] = {}
    cas_refs: dict[str, str] = {}
    if sources_root.is_dir():
        for src in sorted(sources_root.rglob("*")):
            if src.is_file():
                rel = src.relative_to(sources_root)
                target = dest_sources / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
                digest = _sha256_file(target)
                file_digests[str(rel)] = digest
                cas_refs[str(rel)] = put_file(target, cas_root)

    manifest = {
        "schema": "source_snapshot_v2",
        "snapshot_id": snapshot_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "engine_version": "1.0.1",
        "v2_runtime_dependency": 0,
        "file_count": len(file_digests),
        "file_digests": file_digests,
        "cas": {"root": "../cas/objects", "objects": cas_refs},
        "extra": extra_meta or {},
    }
    (snap_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def load_snapshot_manifest(snapshot_dir: Path) -> dict[str, Any]:
    path = Path(snapshot_dir) / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"No manifest.json in {snapshot_dir}")
    return json.loads(path.read_text(encoding="utf-8"))
