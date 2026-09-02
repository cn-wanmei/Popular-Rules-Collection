#!/usr/bin/env python3
"""Static architecture gate for the V3 production supply chain."""
from __future__ import annotations

import ast
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_REFS = (
    "scripts/pipeline.py",
    "scripts/build_",
    ".github/workflows/normalize.yml",
    "workflows: [\"Normalize\"]",
)
WORKFLOWS = ROOT / ".github" / "workflows"


def _python_imports_scripts(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue
        if any(name == "scripts" or name.startswith("scripts.") for name in names):
            return True
    return False


def main() -> int:
    failures: list[str] = []

    for forbidden in (".github/workflows/normalize.yml", "scripts/pipeline.py"):
        if (ROOT / forbidden).exists():
            failures.append(f"obsolete production file exists: {forbidden}")

    for path in ROOT.joinpath("src", "engine").rglob("*.py"):
        if _python_imports_scripts(path):
            failures.append(f"V3 engine imports legacy scripts: {path.relative_to(ROOT)}")

    for path in WORKFLOWS.glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_REFS:
            if token in text:
                failures.append(f"forbidden legacy reference in {path.relative_to(ROOT)}: {token}")
        try:
            doc = yaml.safe_load(text) or {}
        except yaml.YAMLError as exc:
            failures.append(f"invalid workflow YAML {path.name}: {exc}")
            continue
        if "permissions" in doc:
            failures.append(f"workflow-level permissions must be removed: {path.name}")
        for job_name, job in (doc.get("jobs") or {}).items():
            if not isinstance(job, dict):
                failures.append(f"invalid job definition: {path.name}:{job_name}")
                continue
            perms = job.get("permissions")
            if not isinstance(perms, dict) or "contents" not in perms:
                failures.append(f"job-level contents permission missing: {path.name}:{job_name}")

    build = WORKFLOWS / "build.yml"
    publish = WORKFLOWS / "publish.yml"
    if not build.exists():
        failures.append("missing build.yml")
    else:
        build_doc = yaml.safe_load(build.read_text(encoding="utf-8")) or {}
        if "permissions" in build_doc:
            failures.append("build.yml has workflow-level permissions")
        for job_name, job in (build_doc.get("jobs") or {}).items():
            if (job.get("permissions") or {}).get("contents") != "read":
                failures.append(f"build job must be contents: read: {job_name}")
        if "git push" in build.read_text(encoding="utf-8"):
            failures.append("build.yml must never push to main")

    if not publish.exists():
        failures.append("missing publish.yml")
    else:
        pub_doc = yaml.safe_load(publish.read_text(encoding="utf-8")) or {}
        for job_name, job in (pub_doc.get("jobs") or {}).items():
            if (job.get("permissions") or {}).get("contents") != "write":
                failures.append(f"publish job must be contents: write: {job_name}")

    print(yaml.safe_dump({"schema": "architecture_gate_v1", "pass": not failures, "violations": failures}, sort_keys=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
