"""Diff Engine — unified path + safe baseline promotion (P0-5).

- Single output path: reports/diff/latest.json
- Baseline is promoted ONLY after release PASS (not immediately after diff).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DIFF_PATH = "reports/diff/latest.json"          # single canonical path
BASELINE_PATH = "reports/diff/baseline.json"


def run_diff(
    current_canonical: Path,
    baseline_path: Path | None,
    out_dir: Path,
) -> dict[str, Any]:
    """
    Compare current canonical rules vs baseline.
    Does NOT overwrite baseline. Caller must call promote_baseline() after release.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def _load_rules(d: Path) -> dict[str, dict]:
        p = d / "rules.jsonl"
        out = {}
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    out[r["id"]] = r
        return out

    current = _load_rules(current_canonical)
    baseline = {}
    if baseline_path and baseline_path.exists():
        # baseline may be a full canonical dir or a saved rules dump
        if (baseline_path / "rules.jsonl").exists():
            baseline = _load_rules(baseline_path)
        else:
            try:
                baseline = {r["id"]: r for r in json.loads(baseline_path.read_text(encoding="utf-8"))}
            except Exception:
                baseline = {}

    cur_ids = set(current)
    base_ids = set(baseline)
    added = sorted(cur_ids - base_ids)
    removed = sorted(base_ids - cur_ids)
    changed = []
    for rid in sorted(cur_ids & base_ids):
        # simple value / classification / provenance check
        c, b = current[rid], baseline[rid]
        if (c.get("value") != b.get("value")
            or c.get("classification") != b.get("classification")
            or c.get("provenance") != b.get("provenance")):
            changed.append(rid)

    report = {
        "schema": "engine_diff_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "added": len(added),
        "removed": len(removed),
        "changed": len(changed),
        "added_ids": added[:100],
        "removed_ids": removed[:100],
        "changed_ids": changed[:100],
        "v2_runtime_dependency": 0,
    }

    # unified path
    target = out_dir / "latest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # also keep a copy under the classic name for compatibility during transition
    (out_dir / "differential.json").write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
    return report


def promote_baseline(current_canonical: Path, baseline_path: Path) -> None:
    """Call ONLY after Release Gate PASS."""
    baseline_path = Path(baseline_path)
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    rules = []
    p = current_canonical / "rules.jsonl"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rules.append(json.loads(line))
    baseline_path.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
