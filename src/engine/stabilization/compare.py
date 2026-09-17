"""Deterministic semantic comparison for two immutable Engine runs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


_VOLATILE_KEYS = {
    "generated_at", "started_at", "finished_at", "created_at", "updated_at", "timestamp",
    "run_id", "release_id", "promoted_at", "collection_run_id",
}
_PUBLISHABLE_SUFFIXES = {".yaml", ".json", ".list", ".jsonl"}


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
        payload = json.dumps(_canonical_json(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    else:
        try:
            payload = path.read_bytes()
        except OSError:
            return None
    return hashlib.sha256(payload).hexdigest()


def _tree_digest(root: Path, *, suffixes: set[str] | None = None) -> str | None:
    if not root.is_dir():
        return None
    allowed = suffixes or _PUBLISHABLE_SUFFIXES
    entries: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in allowed:
            continue
        digest = _file_digest(path)
        if digest is not None:
            entries.append((path.relative_to(root).as_posix(), digest))
    if not entries:
        return None
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def compare_runs(run_a: Path, run_b: Path) -> dict[str, Any]:
    """Compare semantic stage outputs while ignoring run-local metadata."""
    run_a, run_b = Path(run_a), Path(run_b)
    specs = (
        ("snapshot_id.txt", None),
        ("canonical", _PUBLISHABLE_SUFFIXES),
        ("hierarchy", _PUBLISHABLE_SUFFIXES),
        ("ir", _PUBLISHABLE_SUFFIXES),
        ("artifacts", {".yaml", ".json", ".list"}),
        ("reports/diff", {".json"}),
        ("golden", {".json"}),
    )
    comparisons: dict[str, dict[str, Any]] = {}
    for rel, suffixes in specs:
        a, b = run_a / rel, run_b / rel
        if a.is_dir() or b.is_dir():
            da, db = _tree_digest(a, suffixes=suffixes), _tree_digest(b, suffixes=suffixes)
        else:
            da, db = _file_digest(a), _file_digest(b)
        comparisons[rel] = {"match": da is not None and da == db, "a": da, "b": db}

    match = all(item["match"] for item in comparisons.values())
    return {"schema": "stabilization_compare_v2", "match": match, "comparisons": comparisons}
