#!/usr/bin/env python3
"""Validate the V3 human-rule and generated distribution directory contract."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from src.engine.validation.directory_contract import validate
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json-out", type=Path, default=None)
    args = parser.parse_args()
    report = validate(args.root)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
