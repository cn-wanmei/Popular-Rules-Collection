#!/usr/bin/env python3
"""Run two full V3 replays against the same immutable Snapshot and compare all digests."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from src.engine.pipeline.run import run_pipeline
from src.engine.v1.deterministic import compare_builds

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--data", type=Path, default=ROOT / "data")
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args()

    production = args.data / "runs" / args.run_id
    manifest = json.loads((production / "run_manifest.json").read_text(encoding="utf-8"))
    snapshot_id = (production / "snapshot_id.txt").read_text(encoding="utf-8").strip()
    collection_manifest = manifest.get("collection_manifest")
    if not collection_manifest:
        raise SystemExit("production run has no collection_manifest")
    source_root = ROOT / Path(collection_manifest).parent.parent
    if not source_root.exists():
        raise SystemExit(f"collection source root missing: {source_root}")

    replay_ids = [f"{args.run_id}-repro-b", f"{args.run_id}-repro-c"]
    run_dirs = [production]
    labels = ["production", "replay_b", "replay_c"]

    try:
        for rid in replay_ids:
            run_dir = args.data / "runs" / rid
            shutil.rmtree(run_dir, ignore_errors=True)
            result = run_pipeline(
                source_root,
                args.data,
                run_id=rid,
                snapshot_id=snapshot_id,
                skip_large=bool(manifest.get("skip_large", False)),
            )
            if result.get("status") != "ok":
                report = {
                    "schema": "v3_reproducibility_gate_v1",
                    "source_run_id": args.run_id,
                    "snapshot_id": snapshot_id,
                    "match": False,
                    "all_pass": False,
                    "builds": [],
                    "errors": [f"{rid}: {result.get('failure_stages') or result.get('status')}"],
                }
                args.report.parent.mkdir(parents=True, exist_ok=True)
                args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                return 1
            run_dirs.append(run_dir)

        result = compare_builds(run_dirs, labels=labels)
        report = result.to_dict()
        report.update({
            "schema": "v3_reproducibility_gate_v1",
            "source_run_id": args.run_id,
            "snapshot_id": snapshot_id,
        })
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if (result.match and not result.errors) else 1
    finally:
        for rid in replay_ids:
            shutil.rmtree(args.data / "runs" / rid, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
