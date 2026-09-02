"""Formal CLI for independent V3 Engine.

Usage:
  python -m src.engine.cli all
  python -m src.engine.cli naming_gate
  python -m src.engine.cli snapshot|quarantine|canonical|hierarchy|ir|adapters|diff|golden|release|publish
  python -m src.engine.cli migrate-legacy --database-services <legacy-service-dir>
  python -m src.engine.cli promote --run-id <id>
  python -m src.engine.cli rollback --run-id <id>
  python -m src.engine.cli reproducibility --run-a <path> --run-b <path>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.engine import __version__, __engine__, __v2_runtime_dependency__
from src.engine.pipeline.run import run_pipeline, STAGES
from src.engine.ingest.migrate_legacy import migrate_database_services_to_snapshot
from src.engine.promote.artifact import promote_run, rollback_to_run
from src.engine.reproducibility.hash_compare import compute_run_digest, compare_runs
from src.engine.validation.naming_gate import run_naming_gate


def _add_pipeline_args(parser: argparse.ArgumentParser, *, run_id: bool = True) -> None:
    parser.add_argument("--sources", type=Path, default=Path("sources"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--skip-large", action="store_true", help="Skip configured mega service sets")
    if run_id:
        parser.add_argument("--run-id", type=str, default=None)


def _run_to_stage(args: argparse.Namespace, stage: str) -> int:
    sources = Path(getattr(args, "sources", "sources"))
    data = Path(getattr(args, "data", "data"))
    run_id = getattr(args, "run_id", None)
    skip_large = bool(getattr(args, "skip_large", False))
    if not sources.exists():
        print(json.dumps({
            "status": "failed",
            "reason": f"sources not found: {sources}",
            "stage": stage,
            "v2_runtime_dependency": 0,
        }, ensure_ascii=False, indent=2))
        return 1
    idx = STAGES.index(stage)
    result = run_pipeline(
        sources,
        data,
        run_id=run_id,
        stages=STAGES[: idx + 1],
        skip_large=skip_large,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") == "ok" else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.engine.cli",
        description="Popular-Rules-Collection Engine v3 (independent kernel)",
    )
    parser.add_argument("--version", action="store_true", help="Show version")
    sub = parser.add_subparsers(dest="cmd")

    for name, help_txt in (("all", "Run full pipeline"), ("pipeline", "Run full pipeline (alias of all)")):
        p = sub.add_parser(name, help=help_txt)
        _add_pipeline_args(p)

    sub.add_parser("naming_gate", help="Run naming / V2-runtime gate")

    for stage in STAGES:
        p = sub.add_parser(stage, help=f"Run stage: {stage}")
        _add_pipeline_args(p)

    p_prom = sub.add_parser("promote", help="Promote RC_READY run to generated/")
    p_prom.add_argument("--run-id", type=str, required=True)
    p_prom.add_argument("--runs", type=Path, default=Path("data/runs"))
    p_prom.add_argument("--generated", type=Path, default=Path("generated"))
    p_prom.add_argument("--baseline", type=Path, default=None, help="Advance released diff baseline after successful promotion")
    p_prom.add_argument("--force", action="store_true")

    p_pub = sub.add_parser("publish", help="Run, release-gate, atomically promote, and advance baseline")
    _add_pipeline_args(p_pub)
    p_pub.add_argument("--generated", type=Path, default=Path("generated"))
    p_pub.add_argument("--baseline", type=Path, default=Path("data/baseline/canonical.json"))

    p_rb = sub.add_parser("rollback", help="Rollback generated/ to a previous run")
    p_rb.add_argument("--run-id", type=str, required=True)
    p_rb.add_argument("--runs", type=Path, default=Path("data/runs"))
    p_rb.add_argument("--generated", type=Path, default=Path("generated"))

    p_mig = sub.add_parser("migrate-legacy", help="Migrate the legacy service store into a Source Snapshot")
    p_mig.add_argument("--database-services", type=Path, required=True)
    p_mig.add_argument("--snapshots", type=Path, default=Path("data/snapshots"))
    p_mig.add_argument("--snapshot-id", type=str, default=None)

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
        result = run_pipeline(
            args.sources,
            args.data,
            run_id=args.run_id,
            skip_large=args.skip_large,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") == "ok" else 1

    if args.cmd in STAGES and args.cmd != "release":
        return _run_to_stage(args, args.cmd)

    if args.cmd == "release":
        return _run_to_stage(args, "release")

    if args.cmd == "publish":
        result = run_pipeline(
            args.sources,
            args.data,
            run_id=args.run_id,
            skip_large=args.skip_large,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if result.get("status") != "ok":
            return 1
        run_id = result.get("run_id")
        if not run_id or result.get("stages", {}).get("release", {}).get("state") != "RC_READY":
            return 1
        record = promote_run(
            args.data / "runs" / run_id,
            args.generated,
            baseline_path=args.baseline,
        )
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "migrate-legacy":
        manifest = migrate_database_services_to_snapshot(
            args.database_services, args.snapshots, snapshot_id=args.snapshot_id
        )
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "promote":
        record = promote_run(
            args.runs / args.run_id,
            args.generated,
            force=args.force,
            baseline_path=args.baseline,
        )
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
    raise SystemExit(main())
