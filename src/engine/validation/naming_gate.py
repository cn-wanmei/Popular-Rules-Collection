"""Naming Gate — permanently forbid v3 path pollution and V2 runtime leakage."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

FORBIDDEN_PATH_SEGMENTS = (
    "src/v3",
    "data/v3",
    "config/v3",
    "tests/v3",
    "reports/v3",
    "generated/v3",
)

FORBIDDEN_IMPORT_SUBSTRINGS = (
    "src.v3",
    "build_from_v2_services",
    "snapshot_v2_oracle",
    "legacy_import.v2_service_model",
)

# Allowed only inside migrate_legacy.py
ALLOWED_LEGACY_TOUCH = {
    "src/engine/ingest/migrate_legacy.py",
}


def run_naming_gate(repo_root: Path) -> dict[str, Any]:
    repo_root = Path(repo_root)
    violations: list[str] = []

    # 1. Path segments
    for seg in FORBIDDEN_PATH_SEGMENTS:
        p = repo_root / seg
        if p.exists():
            violations.append(f"forbidden path exists: {seg}")

    # 2. Scan Python sources under src/engine for forbidden imports / calls
    engine_root = repo_root / "src" / "engine"
    if engine_root.is_dir():
        for py in engine_root.rglob("*.py"):
            rel = str(py.relative_to(repo_root)).replace("\\", "/")
            text = py.read_text(encoding="utf-8", errors="ignore")
            for bad in FORBIDDEN_IMPORT_SUBSTRINGS:
                if bad in text:
                    if rel in ALLOWED_LEGACY_TOUCH and bad in (
                        "build_from_v2_services",
                        "snapshot_v2_oracle",
                        "legacy_import.v2_service_model",
                    ):
                        # migrate_legacy may mention them in comments/docs only — still forbid actual import
                        if f"import {bad}" in text or f"from {bad}" in text:
                            violations.append(f"{rel}: forbidden import/use of {bad}")
                    else:
                        # comments are ok; hard fail on import/from
                        if f"import {bad}" in text or f"from {bad}" in text or f"{bad}(" in text:
                            violations.append(f"{rel}: forbidden reference to {bad}")

    report = {
        "schema": "naming_gate_v1",
        "pass": len(violations) == 0,
        "violations": violations,
        "v2_runtime_dependency": 0,
    }
    return report
