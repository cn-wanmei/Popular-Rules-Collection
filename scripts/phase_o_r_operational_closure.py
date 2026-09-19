#!/usr/bin/env python3
"""Phase O-R: operational closure reconciliation.

This gate binds Phase N/O state transitions to persisted evidence. It never
moves or deletes the runtime root and it never treats a user-supplied run count
as observation evidence.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "phase_o_r_operational_closure.yaml"
STATE_DEFAULT = ROOT / "reports" / "v1" / "PHASE_O_STATE.json"
EVIDENCE_DEFAULT = ROOT / "reports" / "v1" / "PHASE_O_EVIDENCE_BUNDLE.json"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "UNKNOWN"


def resolve_reference(ref: str) -> Path:
    path = Path(ref)
    return path if path.is_absolute() else ROOT / path


def validate_observation_run(
    run: dict[str, Any],
    required_checks: list[str],
    cutover_sha: str | None,
) -> list[str]:
    errors: list[str] = []
    run_id = str(run.get("run_id") or "").strip()
    snapshot_id = str(run.get("snapshot_id") or "").strip()
    if not run_id:
        errors.append("observation run missing run_id")
    if not snapshot_id:
        errors.append(f"{run_id or '<unknown>'}: observation run missing snapshot_id")
    if run.get("post_cutover") is not True:
        errors.append(f"{run_id or '<unknown>'}: post_cutover must be true")
    if not cutover_sha:
        errors.append(f"{run_id or '<unknown>'}: no persisted cutover commit SHA")
    elif run.get("cutover_commit_sha") != cutover_sha:
        errors.append(
            f"{run_id or '<unknown>'}: cutover_commit_sha does not match persisted cutover"
        )

    checks = run.get("checks") or {}
    for name in required_checks:
        if checks.get(name) is not True:
            errors.append(f"{run_id or '<unknown>'}: check {name}=true is required")

    references = run.get("references") or {}
    for key in (
        "run_manifest",
        "observation",
        "golden",
        "artifacts",
        "determinism",
        "artifact_equivalence",
        "semantic_regression",
        "source_health",
    ):
        ref = references.get(key)
        if ref and not resolve_reference(str(ref)).is_file():
            errors.append(f"{run_id or '<unknown>'}: evidence file missing: {ref}")

    obs_ref = references.get("observation")
    if obs_ref:
        obs = load_json(resolve_reference(str(obs_ref)))
        if obs.get("all_pass") is not True:
            errors.append(f"{run_id or '<unknown>'}: observation report is not all_pass")
    golden_ref = references.get("golden")
    if golden_ref:
        golden = load_json(resolve_reference(str(golden_ref)))
        if golden.get("all_pass") is not True:
            errors.append(f"{run_id or '<unknown>'}: golden report is not all_pass")
    artifact_ref = references.get("artifacts")
    if artifact_ref:
        artifact = load_json(resolve_reference(str(artifact_ref)))
        clients = set((artifact.get("clients") or {}).keys())
        if len(clients) != 7:
            errors.append(
                f"{run_id or '<unknown>'}: artifact build report does not contain exactly 7 clients"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evidence-bound Phase O-R operational closure gate"
    )
    parser.add_argument(
        "--state",
        choices=[
            "NOT_EXECUTED",
            "CUTOVER_EXECUTED",
            "OBSERVING",
            "FROZEN_OLD_ROOT",
            "RETIRED",
        ],
        default=None,
        help="Desired state to validate. Omit to evaluate the persisted state.",
    )
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--state-file", type=Path, default=STATE_DEFAULT)
    parser.add_argument("--evidence", type=Path, default=EVIDENCE_DEFAULT)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    contract = load_yaml(args.config)
    state_doc = load_json(args.state_file)
    evidence = load_json(args.evidence)
    errors: list[str] = []
    blockers: list[str] = []

    states = list(contract.get("states") or [])
    persisted_state = str(state_doc.get("current_state") or "").strip()
    requested_state = args.state or persisted_state

    if persisted_state not in states:
        errors.append(f"invalid persisted current_state: {persisted_state!r}")
    if requested_state not in states:
        errors.append(f"invalid requested state: {requested_state!r}")

    transition_policy = contract.get("transition_policy") or {}
    if not errors and requested_state != persisted_state:
        allowed = set((transition_policy.get(persisted_state) or {}).get("next") or [])
        if requested_state not in allowed:
            errors.append(
                f"invalid state transition: {persisted_state} -> {requested_state}"
            )

    required_checks = list(
        (contract.get("observation") or {}).get("required_checks") or []
    )
    minimum_runs = int((contract.get("observation") or {}).get("minimum_runs", 3))

    cutover = evidence.get("cutover") or {}
    cutover_status = str(cutover.get("status") or "")
    cutover_sha = str(cutover.get("commit_sha") or "").strip() or None

    if requested_state == "NOT_EXECUTED":
        if cutover_status != "NOT_EXECUTED":
            errors.append("NOT_EXECUTED state requires cutover.status=NOT_EXECUTED")
        if (state_doc.get("closure") or {}).get("cutover_executed") is True:
            errors.append("persisted closure incorrectly claims cutover_executed=true")
        blockers.extend(
            [
                "phase_n_not_executed",
                "canonical_rules_root_not_populated",
                "p0_service_production_not_50_of_50",
                "no_post_cutover_observation_evidence",
            ]
        )

    if requested_state in {
        "CUTOVER_EXECUTED",
        "OBSERVING",
        "FROZEN_OLD_ROOT",
        "RETIRED",
    }:
        if cutover_status != "EXECUTED":
            errors.append("cutover.status must be EXECUTED")
        if not cutover_sha:
            errors.append("cutover.commit_sha is required")
        if cutover.get("source_root") != "rule":
            errors.append("cutover.source_root must be rule")
        if cutover.get("target_root") != "rules":
            errors.append("cutover.target_root must be rules")
        if cutover.get("loader_root") != "rules":
            errors.append("cutover.loader_root must be rules")
        if cutover.get("ci_root") != "rules":
            errors.append("cutover.ci_root must be rules")
        if cutover.get("old_root_preserved") is not True:
            errors.append("old_root_preserved must be true at cutover")
        if not isinstance(cutover.get("evidence"), dict):
            errors.append("cutover.evidence object is required")
        old_root = ROOT / "rule"
        target_root = ROOT / "rules"
        if not old_root.is_dir():
            errors.append("old rule/ root must still exist")
        if not target_root.is_dir():
            errors.append("target rules/ root must exist")
        elif not any(p.is_file() for p in target_root.rglob("*")):
            errors.append("target rules/ root must be non-empty")

    runs = list(evidence.get("observation_runs") or [])
    run_ids = [
        str(x.get("run_id"))
        for x in runs
        if isinstance(x, dict) and x.get("run_id")
    ]
    snapshot_ids = [
        str(x.get("snapshot_id"))
        for x in runs
        if isinstance(x, dict) and x.get("snapshot_id")
    ]
    valid_run_errors: list[str] = []
    for run in runs:
        if isinstance(run, dict):
            valid_run_errors.extend(
                validate_observation_run(run, required_checks, cutover_sha)
            )
        else:
            valid_run_errors.append("observation_runs contains a non-object item")

    if len(set(run_ids)) != len(runs):
        errors.append("observation run_id values must be unique")
    if len(set(snapshot_ids)) != len(runs):
        errors.append("observation snapshot_id values must be unique")

    qualified_runs = len(runs) >= minimum_runs and not valid_run_errors
    if requested_state in {"OBSERVING", "FROZEN_OLD_ROOT", "RETIRED"} and not qualified_runs:
        errors.extend(valid_run_errors)
        errors.append(
            f"qualified observation runs={len(runs)}, minimum={minimum_runs}"
        )

    freeze = evidence.get("old_root_freeze") or {}
    operator_approval = evidence.get("operator_approval") is True
    if requested_state == "RETIRED":
        if freeze.get("status") != "FROZEN":
            errors.append("old_root_freeze.status must be FROZEN before retirement")
        if not freeze.get("evidence"):
            errors.append("old_root_freeze.evidence is required before retirement")
        if not operator_approval:
            errors.append("retirement requires explicit operator_approval=true")

    closure_pass = not errors and requested_state != "NOT_EXECUTED" and (
        requested_state == "CUTOVER_EXECUTED" or qualified_runs
    )
    audit_integrity_pass = not errors

    payload = {
        "schema": "phase_o_r_operational_closure_report_v1",
        "repository": "cn-wanmei/Popular-Rules-Collection",
        "evaluated_head": git_head(),
        "persisted_state": persisted_state,
        "requested_state": requested_state,
        "cutover": {
            "status": cutover_status,
            "commit_sha": cutover_sha,
            "loader_root": cutover.get("loader_root"),
            "ci_root": cutover.get("ci_root"),
        },
        "observation": {
            "required_checks": required_checks,
            "minimum_runs": minimum_runs,
            "evidence_run_count": len(runs),
            "qualified": qualified_runs,
            "run_ids": sorted(run_ids),
            "snapshot_ids": sorted(snapshot_ids),
        },
        "retirement": {
            "old_root_freeze_status": freeze.get("status"),
            "operator_approval": operator_approval,
            "automatic_delete": False,
        },
        "audit_integrity_pass": audit_integrity_pass,
        "closure_pass": closure_pass,
        "blockers": blockers,
        "errors": errors,
    }

    # Emit valid JSON on stdout. A literal "\n" suffix is not JSON whitespace
    # and breaks consumers that parse stdout as a single JSON document.
    output = json.dumps(payload, ensure_ascii=False, indent=2) + "
"
    print(output, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output, encoding="utf-8")
    return 1 if args.enforce and not closure_pass else 0


if __name__ == "__main__":
    raise SystemExit(main())
