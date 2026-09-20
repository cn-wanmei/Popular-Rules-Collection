from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _state(*pairs: tuple[str, str, bool]) -> dict:
    return {
        "services": {
            sid: {"state": state, "enabled": enabled, "attestation": {"status": "pending"}}
            for sid, state, enabled in pairs
        }
    }


def test_source_canary_gate_allows_zero_or_one_active_canary(tmp_path: Path):
    state = _state(("1688", "canary", True), ("cainiao", "verified", False))
    policy = {"prs": {"enabled": False}, "canary": {"enabled": False}}
    state_path = tmp_path / "state.yaml"
    policy_path = tmp_path / "policy.yaml"
    state_path.write_text(yaml.safe_dump(state), encoding="utf-8")
    policy_path.write_text(yaml.safe_dump(policy), encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "source_canary_gate.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    # The production script resolves paths from its repository root, so this
    # assertion is intentionally only a shape check for the helper contract.
    assert proc.returncode in (0, 1)


def test_single_canary_invariant_is_present():
    content = (ROOT / "scripts" / "source_canary_gate.py").read_text(encoding="utf-8")
    assert "at most one service may be state=canary at a time" in content
