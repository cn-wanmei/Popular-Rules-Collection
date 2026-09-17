"""CLI entrypoint for the Phase 2.1.1 Legacy Asset Extractor."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from src.engine.ingest.legacy_asset_extractor import extract_legacy_asset_ir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract legacy rule assets into Legacy Asset IR")
    parser.add_argument("--rule-root", type=Path, default=Path("rule"))
    parser.add_argument("--index", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=Path("data/legacy_asset_ir.yaml"))
    parser.add_argument("--jsonl", type=Path, default=None, help="Optional full de-duplicated asset JSONL output")
    parser.add_argument("--exclude-aggregates", action="store_true")
    args = parser.parse_args(argv)

    ir = extract_legacy_asset_ir(
        args.rule_root,
        index_path=args.index,
        include_aggregates=not args.exclude_aggregates,
        jsonl_output=args.jsonl,
    )
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        yaml.safe_dump(ir.as_dict(), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    result = {"manifest": str(args.manifest), "summary": ir.as_dict()["summary"]}
    if args.jsonl:
        result["jsonl"] = ir.as_dict()["profile"].get("jsonl")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
