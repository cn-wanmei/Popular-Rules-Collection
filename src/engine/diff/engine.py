"""Diff Engine — immutable baseline and safe released-diff comparison."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DIFF_PATH = "reports/diff/latest.json"
BASELINE_PATH = "reports/diff/baseline.json"


def _load_rules(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    rows = [line for line in text.splitlines() if line.strip()]
    if not rows:
        return {}
    # V3 baseline is canonical JSONL. Keep compatibility with older JSON-array baselines.
    try:
        return {r["id"]: r for r in (json.loads(line) for line in rows)}
    except json.JSONDecodeError:
        data = json.loads(text)
        if isinstance(data, list):
            return {r["id"]: r for r in data if isinstance(r, dict) and "id" in r}
        return {}


def run_diff(current_canonical: Path, baseline_path: Path | None, out_dir: Path) -> dict[str, Any]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    current = _load_rules(Path(current_canonical) / "rules.jsonl")
    baseline = {}
    if baseline_path:
        candidate = Path(baseline_path)
        baseline = _load_rules(candidate / "rules.jsonl" if candidate.is_dir() else candidate)

    cur_ids, base_ids = set(current), set(baseline)
    added = sorted(cur_ids - base_ids)
    removed = sorted(base_ids - cur_ids)
    changed = sorted(
        rid for rid in cur_ids & base_ids
        if any(current[rid].get(k) != baseline[rid].get(k) for k in ("value", "classification", "provenance"))
    )
    report = {
        "schema": "engine_diff_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "added": len(added), "removed": len(removed), "changed": len(changed),
        "added_ids": added[:100], "removed_ids": removed[:100], "changed_ids": changed[:100],
        "baseline_present": bool(baseline), "v2_runtime_dependency": 0,
    }
    target = out_dir / "latest.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "differential.json").write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
    return report


def promote_baseline(current_canonical: Path, baseline_path: Path) -> str:
    """Atomically replace a released JSONL baseline and return its digest."""
    import hashlib
    import shutil
    source = Path(current_canonical) / "rules.jsonl"
    target = Path(baseline_path)
    if not source.exists() or source.stat().st_size == 0:
        raise RuntimeError("Cannot promote empty canonical baseline")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f".{target.name}.tmp")
    shutil.copy2(source, tmp)
    tmp.replace(target)
    h = hashlib.sha256(target.read_bytes()).hexdigest()
    return h
