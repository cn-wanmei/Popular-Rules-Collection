"""Naming Gate — forbid V2 runtime leakage and legacy production wiring."""
from __future__ import annotations

from pathlib import Path
from typing import Any

FORBIDDEN_PATH_SEGMENTS = (
    "src/v3", "data/v3", "config/v3", "tests/v3", "reports/v3", "generated/v3",
)

FORBIDDEN_IMPORT_SUBSTRINGS = (
    "src.v3", "build_from_v2_services", "snapshot_v2_oracle", "legacy_import.v2_service_model",
)

ALLOWED_LEGACY_TOUCH = {"src/engine/ingest/migrate_legacy.py"}
LEGACY_SERVICE_DIR = Path("database") / "services"
LEGACY_PRODUCTION_REFERENCES = (
    Path("scripts") / "normalize.py",
    Path("scripts") / "deduplicate.py",
    Path("scripts") / "schema_validate.py",
    Path("scripts") / "validate.py",
    Path("scripts") / "builder_validate.py",
    LEGACY_SERVICE_DIR,
    Path("database") / "domains",
    Path("database") / "ips",
    "python scripts/normalize.py",
    "python scripts/deduplicate.py",
    "build_from_v2_services",
)


def _path_text(path: Path) -> str:
    return path.as_posix()


def _legacy_ref_texts() -> tuple[str, ...]:
    return tuple(_path_text(value) if isinstance(value, Path) else value for value in LEGACY_PRODUCTION_REFERENCES)


def run_naming_gate(repo_root: Path) -> dict[str, Any]:
    repo_root = Path(repo_root)
    violations: list[str] = []

    for seg in FORBIDDEN_PATH_SEGMENTS:
        if (repo_root / seg).exists():
            violations.append(f"forbidden path exists: {seg}")

    engine_root = repo_root / "src" / "engine"
    if engine_root.is_dir():
        for py in engine_root.rglob("*.py"):
            rel = str(py.relative_to(repo_root)).replace("\\", "/")
            text = py.read_text(encoding="utf-8", errors="ignore")
            for bad in FORBIDDEN_IMPORT_SUBSTRINGS:
                if f"import {bad}" in text or f"from {bad}" in text or f"{bad}(" in text:
                    violations.append(f"{rel}: forbidden reference to {bad}")

    production_files = [
        repo_root / ".github" / "workflows" / name
        for name in ("build.yml", "collect.yml", "engine-v3.yml")
    ]
    for workflow in production_files:
        if not workflow.exists():
            continue
        text = workflow.read_text(encoding="utf-8", errors="ignore")
        for bad in _legacy_ref_texts():
            if bad in text:
                violations.append(f"{workflow.relative_to(repo_root)}: forbidden legacy production reference {bad}")

    pipeline_cfg = repo_root / "config" / "pipeline.yaml"
    if pipeline_cfg.exists():
        text = pipeline_cfg.read_text(encoding="utf-8", errors="ignore")
        for bad in _legacy_ref_texts():
            if bad in text:
                violations.append(f"config/pipeline.yaml: forbidden legacy production reference {bad}")

    return {
        "schema": "naming_gate_v3",
        "pass": len(violations) == 0,
        "violations": violations,
        "v2_runtime_dependency": 0,
    }
