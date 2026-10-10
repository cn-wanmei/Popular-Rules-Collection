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
    "scripts/publish_fail_closed_gate.py",
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

    # The post-promotion lock must reconcile Icon against the newly promoted
    # index before the strict writer runs. Checking only for both snippets is
    # insufficient: the order is the consistency contract.
    lock_step = workflow.find("- name: Reconcile Icon identity then write ecosystem release lock")
    if lock_step < 0:
        errors.append("publish.yml is missing the post-promotion identity→lock transaction")
    else:
        identity_step = workflow.find("scripts/ensure_icon_identity.py", lock_step)
        writer_step = workflow.find("scripts/write_ecosystem_release_lock.py", lock_step)
        strict_gate = workflow.find("--require-icon-identity", writer_step if writer_step >= 0 else lock_step)
        if identity_step < lock_step or writer_step < identity_step:
            errors.append("post-promotion lock must reconcile Icon identity before writing the lock")
        if strict_gate < writer_step or strict_gate < 0:
            errors.append("post-promotion lock writer must require Icon identity match")
        if "scripts/verify_ecosystem_release_lock.py" not in workflow[lock_step:]:
            errors.append("post-promotion lock must run verify_ecosystem_release_lock.py")

    if re.search(r"^\\s*git\\s+(?:pull\\s+--rebase|rebase\\s+--autostash)\\b", workflow, re.M):
        errors.append("publish.yml must not rebase large generated-tree commits")

    print("Publish Fail-Closed Gate:", "PASS" if not errors else "FAIL")
    for error in errors:
        print(f" - {error}")
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
