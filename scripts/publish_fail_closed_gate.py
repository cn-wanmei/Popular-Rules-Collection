#!/usr/bin/env python3
"""Fail-closed static gate for the production Publish workflow."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FORBIDDEN_PATTERNS = {
    "ignore_failure": re.compile(r"\|\|\s*true"),
    "continue_on_error": re.compile(r"continue-on-error\s*:\s*true"),
}

REQUIRED_SNIPPETS = (
    "scripts/evidence_consistency_gate.py",
    "--require-latest",
    "scripts/immutable_source_lineage_gate.py",
    "scripts/partial_production_invariant_gate.py",
    "scripts/icon_system_v5.py",
    "assets/icons/v5/registry.json",
    "assets/icons/v5/release-pointer.json",
)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", type=Path, default=Path(".github/workflows/publish.yml"))
    parser.add_argument("--status-workflow", type=Path, default=Path(".github/workflows/status.yml"))
    args = parser.parse_args()

    errors: list[str] = []
    workflow = args.workflow.read_text(encoding="utf-8")
    status = args.status_workflow.read_text(encoding="utf-8")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(workflow):
            errors.append(f"publish.yml contains forbidden fail-open construct: {label}")
        if pattern.search(status):
            errors.append(f"status.yml contains forbidden fail-open construct: {label}")

    for snippet in REQUIRED_SNIPPETS:
        if snippet not in workflow:
            errors.append(f"publish.yml is missing required fail-closed gate: {snippet}")

    if "evidence_consistency_gate.py --run-id" in workflow and "--require-latest" not in workflow:
        errors.append("evidence consistency gate is present without --require-latest")

    print("Publish Fail-Closed Gate:", "PASS" if not errors else "FAIL")
    for error in errors:
        print(f" - {error}")
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
