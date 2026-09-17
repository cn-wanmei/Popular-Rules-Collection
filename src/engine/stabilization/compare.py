"""Deterministic semantic comparison for two immutable Engine runs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


_VOLATILE_KEYS = {"generated_at", "started_at", "finished_at", "created_at", "updated_at", "timestamp"}


def _canonical_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _canonical_json(v) for k, v in sorted(value.items()) if k not in _VOLATILE_KEYS}
    if isinstance(value, list):
        return [_canonical_json(v) for v in value]
    return value


def _file_digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    if path.suffix == ".json":
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return None
        payload = json.dumps(_canonical_json(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    else:
        payload = path.read_bytes()
    return hashlib.sha256(payload).hexdigest()


def _tree_digest(root: Path) -> str | None:
    if not root.is_dir():
        return None
    entries: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "run_manifest.json":
            continue
        digest = _file_digest(path)
        if digest is not None:
            entries.append((path.relative_to(root).as_posix(), digest))
    if not entries:
        return None
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def compare_runs(run_a: Path, run_b: Path) -> dict[str, Any]:
    """Compare semantic stage outputs while ignoring runtime timestamps."""
    run_a, run_b = Path(run_a), Path(run_b)
    paths = (
        "snapshot_id.txt",
        "canonical",
        "hierarchy",
        "ir",
        "artifacts",
        "reports/diff",
        "golden",
    )
    comparisons: dict[str, dict[str, Any]] = {}
    for rel in paths:
        a, b = run_a / rel, run_b / rel
        if a.is_dir() or b.is_dir():
            da, db = _tree_digest(a), _tree_digest(b)
        else:
            da, db = _file_digest(a), _file_digest(b)
        comparisons[rel] = {"match": da is not None and da == db, "a": da, "b": db}

    # run manifests are deliberately excluded because they contain run-local timestamps and IDs.
    match = all(item["match"] for item in comparisons.values())
    return {"schema": "stabilization_compare_v1", "match": match, "comparisons": comparisons}
