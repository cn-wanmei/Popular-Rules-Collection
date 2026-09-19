#!/usr/bin/env python3
"""Phase G: fail-closed wrapper around final determinism evidence."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path, default=ROOT / "reports/v1/V3_DETERMINISM_FINAL.json")
    args = ap.parse_args()
    errors = []
    if not args.report.is_file():
        errors.append(f"missing determinism report: {args.report}")
    report = json.loads(args.report.read_text(encoding="utf-8")) if args.report.is_file() else {}
    if report.get("all_pass") is not True:
        errors.append(f"determinism all_pass={report.get('all_pass')!r}")

    payload = {
        "schema": "phase_g_determinism_guard_v1",
        "report": str(args.report),
        "all_pass": report.get("all_pass"),
        "pass": not errors,
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
