"""One-time / optional migration: legacy database/services → Source Snapshot.

This is the ONLY place that may still touch database/services.
After snapshot is created, the rest of the Engine never reads it again.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from src.engine.snapshot.engine import create_source_snapshot


def migrate_database_services_to_snapshot(
    database_services_dir: Path,
    snapshots_dir: Path,
    *,
    snapshot_id: str | None = None,
) -> dict[str, Any]:
    """
    Copy database/services/*.yaml into a fresh Source Snapshot under sources/services/.
    Returns the snapshot manifest.
    """
    database_services_dir = Path(database_services_dir)
    if not database_services_dir.is_dir():
        raise FileNotFoundError(f"database/services not found: {database_services_dir}")

    # temporary staging so create_source_snapshot can freeze it
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        staging = Path(td) / "sources"
        dest = staging / "services"
        dest.mkdir(parents=True)
        count = 0
        for p in sorted(database_services_dir.glob("*.yaml")):
            if p.name.startswith("example"):
                continue
            shutil.copy2(p, dest / p.name)
            count += 1
        if count == 0:
            raise RuntimeError("No service YAML found to migrate")
        manifest = create_source_snapshot(
            staging,
            Path(snapshots_dir),
            snapshot_id=snapshot_id,
            extra_meta={
                "migrated_from": str(database_services_dir),
                "service_files": count,
                "note": "legacy database/services → snapshot; Engine runtime no longer depends on it",
            },
        )
    return manifest
