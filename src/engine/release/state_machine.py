"""Release State Machine — HARD gates before any publish (P0-4 / P0-10)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class ReleaseState(str, Enum):
    BUILDING = "BUILDING"
    VALIDATING = "VALIDATING"
    GOLDEN = "GOLDEN"
    RC_READY = "RC_READY"
    RELEASE_ARTIFACT = "RELEASE_ARTIFACT"
    PUBLISH = "PUBLISH"
    PRODUCTION = "PRODUCTION"
    BLOCKED = "BLOCKED"


def evaluate_release(run_dir: Path) -> dict[str, Any]:
    """
    Compute release state from actual artifacts + golden report.
    Never set production_cutover = True by hand.
    """
    run_dir = Path(run_dir)
    gates = {}

    # Gate: V2 dependency must be 0
    run_manifest = run_dir / "run_manifest.json"
    v2_ok = False
    if run_manifest.exists():
        m = json.loads(run_manifest.read_text(encoding="utf-8"))
        v2_ok = m.get("v2_runtime_dependency") == 0
    gates["v2_runtime_dependency_zero"] = v2_ok

    # Gate: Golden all_pass
    golden_path = run_dir / "golden" / "report.json"
    golden_ok = False
    if golden_path.exists():
        g = json.loads(golden_path.read_text(encoding="utf-8"))
        golden_ok = g.get("all_pass") is True
    gates["golden_all_pass"] = golden_ok

    # Gate: Canonical + IR + Artifacts exist
    gates["canonical_present"] = (run_dir / "canonical" / "manifest.json").exists()
    gates["ir_present"] = (run_dir / "ir" / "manifest.json").exists()
    gates["artifacts_present"] = (run_dir / "artifacts").exists()

    # Gate: Diff baseline not auto-promoted yet (we just check diff exists)
    gates["diff_present"] = (run_dir / "reports" / "diff" / "latest.json").exists()

    all_hard = all(gates.values())

    if not all_hard:
        state = ReleaseState.BLOCKED
    elif golden_ok and v2_ok:
        state = ReleaseState.RC_READY
    else:
        state = ReleaseState.VALIDATING

    report = {
        "schema": "release_state_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "state": state.value,
        "gates": gates,
        "all_hard_pass": all_hard,
        "v2_runtime_dependency": 0,
        "can_publish": state == ReleaseState.RC_READY,
    }
    out = run_dir / "release" / "state.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
