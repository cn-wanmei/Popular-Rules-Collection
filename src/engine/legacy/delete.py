"""Phase 8 — explicit, fail-closed Legacy deletion.

Nothing in the production build invokes this module automatically. Deletion
requires a PASS final migration gate, V1 Canonical SoT, current-HEAD binding,
the exact configured Legacy target, and an explicit operator approval.
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any
LEGACY_DELETE_SCHEMA = "v1_legacy_delete_v1"
EXPECTED_TARGET = Path("database/services")
class LegacyDeleteError(RuntimeError):
    pass
def _load_gate(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LegacyDeleteError(f"invalid final migration gate: {path}") from exc
    if not isinstance(data, dict):
        raise LegacyDeleteError("final migration gate must be an object")
    return data
def validate_delete_authorization(gate_path: Path, target: Path, *, explicit_approval: bool, current_head: str | None = None) -> dict[str, Any]:
    gate = _load_gate(gate_path)
    if gate.get("status") != "PASS": raise LegacyDeleteError("final migration gate is not PASS")
    phase8 = gate.get("phase8") or {}
    if phase8.get("sot") != "v1_canonical": raise LegacyDeleteError("V1 Canonical is not the active Source of Truth")
    head_evidence = gate.get("current_head") or {}
    if head_evidence.get("pass") is not True:
        raise LegacyDeleteError("final evidence is not bound to current HEAD")
    if current_head is not None and current_head != head_evidence.get("actual"):
        raise LegacyDeleteError("final evidence HEAD does not match current checkout")
    boundary = gate.get("deletion_boundary") or {}
    if boundary.get("automatic_delete") is not False: raise LegacyDeleteError("automatic deletion is not explicitly disabled")
    target = Path(target)
    if target.as_posix() != EXPECTED_TARGET.as_posix(): raise LegacyDeleteError(f"refusing unexpected target: {target}")
    if target.is_symlink(): raise LegacyDeleteError("refusing symlink deletion target")
    if not explicit_approval: raise LegacyDeleteError("explicit operator approval is required")
    if not target.exists(): raise LegacyDeleteError("Legacy target does not exist")
    if not target.is_dir(): raise LegacyDeleteError("Legacy target is not a directory")
    return {
        "schema": LEGACY_DELETE_SCHEMA,
        "authorized": True,
        "target": target.as_posix(),
        "run_id": gate.get("run_id"),
        "current_head": current_head.get("actual"),
    }
def delete_legacy(
    gate_path: Path,
    target: Path,
    *,
    explicit_approval: bool = False,
    current_head: str | None = None,
) -> dict[str, Any]:
    authorization = validate_delete_authorization(
        gate_path,
        target,
        explicit_approval=explicit_approval,
        current_head=current_head,
    )
    target = Path(target)
    shutil.rmtree(target)
    authorization["deleted"] = True
    return authorization
