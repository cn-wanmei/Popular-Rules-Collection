"""True Reproducibility — same snapshot_id → same artifact digests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_run_digest(run_dir: Path) -> dict[str, Any]:
    """
    Compute deterministic digests of key artifacts for a finished run.
    """
    run_dir = Path(run_dir)
    digests: dict[str, str] = {}
    important = [
        "canonical/rules.jsonl",
        "canonical/memberships.jsonl",
        "canonical/manifest.json",
        "hierarchy/graph.json",
        "ir/ir.json",
        "ir/decisions.jsonl",
        "golden/report.json",
        "release/state.json",
    ]
    for rel in important:
        p = run_dir / rel
        if p.exists():
            digests[rel] = _sha256_file(p)

    # also hash all native artifacts
    art = run_dir / "artifacts"
    if art.exists():
        for f in sorted(art.rglob("*")):
            if f.is_file() and f.suffix in (".yaml", ".json", ".list"):
                digests[str(f.relative_to(run_dir))] = _sha256_file(f)

    overall = hashlib.sha256(
        json.dumps(digests, sort_keys=True).encode("utf-8")
    ).hexdigest()

    report = {
        "schema": "reproducibility_digest_v1",
        "run_dir": str(run_dir),
        "file_digests": digests,
        "overall_digest": overall,
        "file_count": len(digests),
        "v2_runtime_dependency": 0,
    }
    out = run_dir / "reproducibility" / "digest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def compare_runs(run_a: Path, run_b: Path) -> dict[str, Any]:
    """
    Compare two runs that should have been produced from the same snapshot.
    Returns match status + differing files.
    """
    da = compute_run_digest(run_a)
    db = compute_run_digest(run_b)
    keys_a = set(da["file_digests"])
    keys_b = set(db["file_digests"])
    only_a = sorted(keys_a - keys_b)
    only_b = sorted(keys_b - keys_a)
    differ = sorted(
        k for k in (keys_a & keys_b)
        if da["file_digests"][k] != db["file_digests"][k]
    )
    match = (
        da["overall_digest"] == db["overall_digest"]
        and not only_a and not only_b and not differ
    )
    return {
        "match": match,
        "overall_a": da["overall_digest"],
        "overall_b": db["overall_digest"],
        "only_in_a": only_a,
        "only_in_b": only_b,
        "differ": differ,
        "v2_runtime_dependency": 0,
    }
