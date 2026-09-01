"""Retention-aware garbage collection for immutable filesystem CAS objects."""
from __future__ import annotations

import time
from pathlib import Path
from typing import Iterable


def referenced_digests(run_roots: Iterable[Path]) -> set[str]:
    """Collect digests referenced by immutable CAS manifests under run roots."""
    import json

    refs: set[str] = set()
    for root in run_roots:
        root = Path(root)
        if not root.exists():
            continue
        for manifest_path in root.rglob("cas-manifest.json"):
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            objects = manifest.get("objects")
            if isinstance(objects, dict):
                refs.update(d for d in objects.values() if isinstance(d, str) and len(d) == 64)
    return refs


def collect(
    cas_root: Path,
    *,
    referenced: Iterable[str] = (),
    pinned: Iterable[str] = (),
    min_age_seconds: float = 0,
    dry_run: bool = True,
) -> dict[str, int]:
    """Delete unreferenced, unpinned objects older than the retention threshold.

    ``dry_run=True`` is the safe default. Objects are addressed solely by their
    SHA-256 path and are never removed when referenced or pinned.
    """
    root = Path(cas_root)
    protected = {d.lower() for d in referenced} | {d.lower() for d in pinned}
    now = time.time()
    scanned = eligible = deleted = 0
    for path in root.glob("[0-9a-f][0-9a-f]/*"):
        if not path.is_file() or len(path.name) != 62 or len(path.parent.name) != 2:
            continue
        digest = path.parent.name + path.name
        scanned += 1
        if digest in protected:
            continue
        try:
            age = now - path.stat().st_mtime
        except OSError:
            continue
        if age < min_age_seconds:
            continue
        eligible += 1
        if not dry_run:
            try:
                path.unlink()
                deleted += 1
            except FileNotFoundError:
                pass
    return {"scanned": scanned, "eligible": eligible, "deleted": deleted}
