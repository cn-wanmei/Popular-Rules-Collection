"""Formal CLI for independent V3 Engine.

Usage:
  python -m src.engine.cli all
  python -m src.engine.cli naming_gate
  python -m src.engine.cli snapshot|quarantine|canonical|hierarchy|ir|adapters|diff|golden|release
  python -m src.engine.cli migrate-legacy --database-services ./database/services
  python -m src.engine.cli promote --run-id <id>
  python -m src.engine.cli rollback --run-id <id>
  python -m src.engine.cli reproducibility --run-a <path> --run-b <path>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.engine import __version__, __engine__, __v2_runtime_dependency__
from src.engine.pipeline.run import run_pipeline, STAGES
from src.engine.ingest.migrate_legacy import migrate_database_services_to_snapshot
from src.engine.promote.artifact import promote_run, rollback_to_run
from src.engine.reproducibility.hash_compare import compute_run_digest, compare_runs
from src.engine.validation.naming_gate import run_naming_gate

LEGACY_STAGE_ALIASES = {
    "snapshot": "snapshot",
    "quarantine": "quarantine",
    "canonical": "canonical",
    "hierarchy": "hierarchy",
    "ir": "ir",
    "ir_full": "ir",
    "adapters": "adapters",
    "diff": "diff",
    "golden": "golden",
    "release": "release",
    "publish": "release",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.engine.cli",
        description="Popular-Rules-Collection Engine v3 (independent kernel)",
    )
    parser.add_argument("--version", action="store_true", help="Show version")
    sub = parser.add_subparsers(dest="cmd")

    for name, help_txt in (
        ("all", "Run full pipeline"),
        ("pipeline", "Run full pipeline (alias of all)"),
    ):
        p = sub.add_parser(name, help=help_txt)
        p.add_argument("--sources", type=Path, default=Path("sources"))
        p.add_argument("--data", type=Path, default=Path("data"))

    sub.add_parser("naming_gate", help="Run naming / V2-runtime gate")

    for stage in (
        "snapshot", "quarantine", "canonical", "hierarchy", "ir", "ir_full",
        "adapters", "diff", "golden", "release", "publish",
    ):
        p = sub.add_parser(stage, help=f"Run stage: {stage}")
        p.add_argument("--sources", type=Path, default=Path("sources"))
        p.add_argument("--data", type=Path, default=Path("data"))
        p.add_argument("--run-id", type=str, default=None)

    p_mig = sub.add_parser("migrate-legacy", help="database/services → Source Snapshot")
    p_mig.add_argument("--database-services", type=Path, required=True)
    p_mig.add_argument("--snapshots", type=Path, default=Path("data/snapshots"))
    p_mig.add_argument("--snapshot-id", type=str, default=None)

    p_prom = sub.add_parser("promote", help="Promote RC_READY run to generated/")
    p_prom.add_argument("--run-id", type=str, required=True)
    p_prom.add_argument("--runs", type=Path, default=Path("data/runs"))
    p_prom.add_argument("--generated", type=Path, default=Path("generated"))
    p_prom.add_argument("--force", action="store_true")

    p_rb = sub.add_parser("rollback", help="Rollback generated/ to a previous run")
    p_rb.add_argument("--run-id", type=str, required=True)
    p_rb.add_argument("--runs", type=Path, default=Path("data/runs"))
    p_rb.add_argument("--generated", type=Path, default=Path("generated"))

    p_rep = sub.add_parser("reproducibility", help="Compare two runs")
    p_rep.add_argument("--run-a", type=Path, required=True)
    p_rep.add_argument("--run-b", type=Path, required=True)

    p_dig = sub.add_parser("digest", help="Compute run digest")
    p_dig.add_argument("--run", type=Path, required=True)

    args = parser.parse_args(argv)

    if args.version or args.cmd is None:
        print(
            f"Engine {__engine__}  product {__version__}  "
            f"v2_runtime_dependency={__v2_runtime_dependency__}"
        )
        if args.cmd is None and not args.version:
            parser.print_help()
        return 0

    if args.cmd == "naming_gate":
        report = run_naming_gate(Path("."))
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("pass") else 1

    if args.cmd in ("all", "pipeline"):
        result = run_pipeline(args.sources, args.data)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") == "ok" else 1

    if args.cmd == "migrate-legacy":
        manifest = migrate_database_services_to_snapshot(
            args.database_services, args.snapshots, snapshot_id=args.snapshot_id
        )
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0

    if args.cmd in LEGACY_STAGE_ALIASES:
        target = LEGACY_STAGE_ALIASES[args.cmd]
        if target not in STAGES:
            print(f"Unknown stage mapping: {target}", file=sys.stderr)
            return 2
        idx = STAGES.index(target)
        stages = STAGES[: idx + 1]
        sources = getattr(args, "sources", Path("sources"))
        data = getattr(args, "data", Path("data"))
        run_id = getattr(args, "run_id", None)
        if not sources.exists():
            print(json.dumps({
                "status": "skipped",
                "reason": f"sources not found: {sources}",
                "stage": target,
                "v2_runtime_dependency": 0,
            }, indent=2))
            return 0
        result = run_pipeline(sources, data, run_id=run_id, stages=stages)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") == "ok" else 1

    if args.cmd == "promote":
        run_dir = args.runs / args.run_id
        record = promote_run(run_dir, args.generated, force=args.force)
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "rollback":
        record = rollback_to_run(args.run_id, args.runs, args.generated)
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "reproducibility":
        report = compare_runs(args.run_a, args.run_b)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["match"] else 1

    if args.cmd == "digest":
        report = compute_run_digest(args.run)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
