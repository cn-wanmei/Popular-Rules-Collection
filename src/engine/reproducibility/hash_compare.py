"""Reproducibility — stable semantic output digests across repeated runs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

VOLATILE_KEYS = {"generated_at", "started_at", "finished_at", "promoted_at", "run_dir", "ingested_at"}
SEMANTIC_ARTIFACT_SUFFIXES = {".yaml", ".list", ".json"}
METADATA_JSON_NAMES = {"build_report.json"}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _stable_json_bytes(path: Path) -> bytes:
    data = json.loads(path.read_text(encoding="utf-8"))

    def strip(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: strip(v) for k, v in sorted(value.items()) if k not in VOLATILE_KEYS}
        if isinstance(value, list):
            return [strip(v) for v in value]
        return value

    return json.dumps(strip(data), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(path: Path) -> str:
    if path.suffix == ".json":
        try:
            return hashlib.sha256(_stable_json_bytes(path)).hexdigest()
        except (OSError, json.JSONDecodeError):
            pass
    return _sha256_file(path)


def compute_run_digest(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    digests: dict[str, str] = {}
    important = [
        "canonical/rules.jsonl",
        "canonical/memberships.jsonl",
        "hierarchy/graph.json",
        "ir/ir.json",
        "ir/decisions.jsonl",
    ]
    for rel in important:
        p = run_dir / rel
        if p.exists():
            digests[rel] = _digest(p)

    art = run_dir / "artifacts"
    if art.exists():
        for f in sorted(art.rglob("*")):
            if f.is_file() and f.suffix in SEMANTIC_ARTIFACT_SUFFIXES and f.name not in METADATA_JSON_NAMES:
                digests[str(f.relative_to(run_dir))] = _digest(f)

    overall = hashlib.sha256(json.dumps(digests, sort_keys=True).encode("utf-8")).hexdigest()
    report = {
        "schema": "reproducibility_digest_v3",
        "run_dir": str(run_dir),
        "file_digests": digests,
        "overall_digest": overall,
        "file_count": len(digests),
        "volatile_metadata_excluded": sorted(VOLATILE_KEYS),
        "metadata_files_excluded": sorted(METADATA_JSON_NAMES),
        "v2_runtime_dependency": 0,
    }
    out = run_dir / "reproducibility" / "digest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def compare_runs(run_a: Path, run_b: Path) -> dict[str, Any]:
    da = compute_run_digest(run_a)
    db = compute_run_digest(run_b)
    keys_a = set(da["file_digests"])
    keys_b = set(db["file_digests"])
    only_a = sorted(keys_a - keys_b)
    only_b = sorted(keys_b - keys_a)
    differ = sorted(k for k in (keys_a & keys_b) if da["file_digests"][k] != db["file_digests"][k])
    return {
        "match": da["overall_digest"] == db["overall_digest"] and not only_a and not only_b and not differ,
        "overall_a": da["overall_digest"],
        "overall_b": db["overall_digest"],
        "only_in_a": only_a,
        "only_in_b": only_b,
        "differ": differ,
        "v2_runtime_dependency": 0,
    }
