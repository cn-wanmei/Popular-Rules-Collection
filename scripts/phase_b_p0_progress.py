#!/usr/bin/env python3
"""Phase B: audit the 50-service P0 production queue without mutating state."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
HARD = ("identity", "source", "canonical", "semantic_audit", "overlap_audit", "seven_client", "golden", "release")

def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", type=Path, default=ROOT / "config/p0_service_production.yaml")
    ap.add_argument("--queue", type=Path, default=ROOT / "config/p0_materialization.yaml")
    args = ap.parse_args()

    matrix = load_yaml(args.matrix).get("services") or {}
    queue = load_yaml(args.queue).get("services") or []
    ids = [str(x.get("id")) for x in queue if isinstance(x, dict) and x.get("id")]
    errors = []
    if len(ids) != 50 or len(set(ids)) != 50:
        errors.append(f"P0 queue must contain exactly 50 unique services; found {len(ids)}")
    if set(matrix) != set(ids):
        errors.append("production matrix keys do not exactly match P0 queue")

    rows = []
    production = 0
    blocked = 0
    partial = 0
    unknown = 0
    for sid in ids:
        row = matrix.get(sid) or {}
        failed = [k for k in HARD if row.get(k) != "pass"]
        status = row.get("status")
        coverage = row.get("coverage", "not_recorded")
        if status == "production" and not failed:
            production += 1
        else:
            blocked += 1
        partial += coverage == "partial"
        unknown += coverage == "unknown"
        rows.append({"id": sid, "status": status, "coverage": coverage, "failed_gates": failed})

    payload = {
        "schema": "phase_b_p0_progress_v1",
        "queue_size": len(ids),
        "production": production,
        "blocked": blocked,
        "coverage_partial": partial,
        "coverage_unknown": unknown,
        "target": 50,
        "pass": not errors and production == 50,
        "errors": errors,
        "services": rows,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
