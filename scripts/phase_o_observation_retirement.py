#!/usr/bin/env python3
"""Evidence-bound Phase O wrapper.

Observation evidence is loaded from the persisted Phase O evidence bundle.
There is deliberately no manual run-count argument and this wrapper never
moves or deletes the old runtime root.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.phase_o_r_operational_closure import main as o_r_main


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evidence-bound Phase O observation/freeze/retirement gate"
    )
    parser.add_argument(
        "--state",
        required=True,
        choices=["CUTOVER_EXECUTED", "OBSERVING", "FROZEN_OLD_ROOT", "RETIRED"],
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        default=Path("reports/v1/PHASE_O_EVIDENCE_BUNDLE.json"),
    )
    parser.add_argument("--json-out", type=Path, default=None)
    # Kept as a rejected compatibility flag so older invocations fail closed
    # rather than silently accepting a fake approval source.
    parser.add_argument(
        "--approve-retirement",
        action="store_true",
        help="Deprecated: approval must be persisted in the evidence bundle.",
    )
    args = parser.parse_args()

    argv = [
        "phase_o_r_operational_closure.py",
        "--state",
        args.state,
        "--evidence",
        str(args.evidence),
        "--enforce",
    ]
    if args.json_out:
        argv += ["--json-out", str(args.json_out)]

    old_argv = sys.argv
    try:
        sys.argv = argv
        return o_r_main()
    finally:
        sys.argv = old_argv


if __name__ == "__main__":
    raise SystemExit(main())
