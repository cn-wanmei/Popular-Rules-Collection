"""Command line entry point for the V3 Collection DAG."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .run import run_collection


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m src.engine.collection")
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    parser.add_argument("--skip-large", action="store_true")
    args = parser.parse_args()
    result = run_collection(args.data, date=args.date, skip_large=args.skip_large)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") in {"ok", "degraded"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
