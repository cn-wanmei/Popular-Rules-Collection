#!/usr/bin/env python3
"""Promote a validated run's stable metrics to the production baseline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.engine.observability.baseline import build_baseline


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote a validated run to baseline")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--baseline", type=Path, default=Path("data/baseline/latest.json"))
    args = parser.parse_args()

    metrics_path = args.run_dir / "metrics" / "metrics.json"
    quality_path = args.run_dir / "quality.json"
    if not metrics_path.is_file() or not quality_path.is_file():
        raise SystemExit("baseline promotion requires metrics.json and quality.json")
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    quality = json.loads(quality_path.read_text(encoding="utf-8"))
    if quality.get("decision") != "PASS":
        raise SystemExit("refusing to promote a non-PASS run")
    baseline = build_baseline(metrics)
    args.baseline.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.baseline.with_name(f".{args.baseline.name}.tmp")
    tmp.write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(args.baseline)
    print(f"promoted baseline: {args.baseline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
