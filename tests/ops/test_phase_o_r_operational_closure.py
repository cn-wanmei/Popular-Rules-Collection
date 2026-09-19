from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

import scripts.phase_o_r_operational_closure as gate


def write_fixture(root: Path) -> tuple[Path, Path, Path]:
    config = root / "config.yaml"
    state = root / "state.json"
    evidence = root / "evidence.json"
    config.write_text(
        yaml.safe_dump(
            {
                "states": [
                    "NOT_EXECUTED",
                    "CUTOVER_EXECUTED",
                    "OBSERVING",
                    "FROZEN_OLD_ROOT",
                    "RETIRED",
                ],
                "transition_policy": {
                    "NOT_EXECUTED": {"next": ["CUTOVER_EXECUTED"]},
                },
                "observation": {
                    "minimum_runs": 3,
                    "required_checks": [
                        "seven_client",
                        "golden",
                        "determinism",
                        "artifact_equivalence",
                        "semantic_regression",
                        "source_health",
                    ],
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    state.write_text(
        json.dumps(
            {
                "current_state": "NOT_EXECUTED",
                "closure": {"cutover_executed": False},
            }
        ),
        encoding="utf-8",
    )
    evidence.write_text(
        json.dumps(
            {
                "cutover": {
                    "status": "NOT_EXECUTED",
                    "source_root": "rule",
                    "target_root": "rules",
                    "loader_root": "rule",
                    "ci_root": "rule",
                    "old_root_preserved": True,
                },
                "observation_runs": [],
                "old_root_freeze": {"status": "NOT_FROZEN"},
                "operator_approval": False,
            }
        ),
        encoding="utf-8",
    )
    return config, state, evidence


def run_gate(monkeypatch, *args: str) -> int:
    monkeypatch.setattr(sys, "argv", ["phase_o_r_operational_closure.py", *args])
    return gate.main()


def test_not_executed_is_a_honest_non_closed_state(tmp_path, monkeypatch, capsys):
    config, state, evidence = write_fixture(tmp_path)
    rc = run_gate(
        monkeypatch,
        "--config",
        str(config),
        "--state-file",
        str(state),
        "--evidence",
        str(evidence),
    )
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["persisted_state"] == "NOT_EXECUTED"
    assert payload["closure_pass"] is False
    assert "phase_n_not_executed" in payload["blockers"]


def test_enforce_fails_before_operational_closure(tmp_path, monkeypatch, capsys):
    config, state, evidence = write_fixture(tmp_path)
    rc = run_gate(
        monkeypatch,
        "--config",
        str(config),
        "--state-file",
        str(state),
        "--evidence",
        str(evidence),
        "--enforce",
    )
    assert rc == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["closure_pass"] is False


def test_manual_runs_argument_is_rejected(tmp_path, monkeypatch):
    config, state, evidence = write_fixture(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "phase_o_r_operational_closure.py",
            "--config",
            str(config),
            "--state-file",
            str(state),
            "--evidence",
            str(evidence),
            "--runs",
            "3",
        ],
    )
    try:
        gate.main()
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("manual --runs argument must be rejected")
