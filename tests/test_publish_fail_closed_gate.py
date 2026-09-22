from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "publish_fail_closed_gate.py"


def test_repository_publish_fail_closed_gate_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(GATE)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_publish_fail_closed_gate_rejects_ignored_status_failure(tmp_path: Path) -> None:
    status = tmp_path / "status.yml"
    status.write_text("git fetch --prune origin main || true\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(GATE),
            "--status-workflow",
            str(status),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "status.yml contains ignored command failure" in result.stdout
