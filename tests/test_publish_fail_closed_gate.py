from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REQUIRED_SNIPPETS = (
    "scripts/evidence_consistency_gate.py",
    "--require-latest",
    "scripts/immutable_source_lineage_gate.py",
    "scripts/partial_production_invariant_gate.py",
    "scripts/icon_v3_gate.py",
    "assets/icons/v3/releases/latest/manifest.json",
)


def _run_gate(tmp_path: Path, status: str) -> subprocess.CompletedProcess[str]:
    publish = tmp_path / "publish.yml"
    publish.write_text("\n".join(REQUIRED_SNIPPETS), encoding="utf-8")
    status_file = tmp_path / "status.yml"
    status_file.write_text(status, encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            "scripts/publish_fail_closed_gate.py",
            "--workflow",
            str(publish),
            "--status-workflow",
            str(status_file),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_publish_fail_closed_gate_accepts_clean_status_workflow(tmp_path: Path) -> None:
    result = _run_gate(tmp_path, "git rebase --abort\n")
    assert result.returncode == 0, result.stdout + result.stderr


def test_publish_fail_closed_gate_rejects_ignored_status_failure(tmp_path: Path) -> None:
    result = _run_gate(tmp_path, "git fetch --prune origin main || true\n")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "status.yml contains ignored command failure" in result.stdout
