#!/usr/bin/env python3
"""Static architecture and CI security gate for the V3 production supply chain."""
from __future__ import annotations

import ast
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_REFS = (
    "scripts/" + "pipeline.py",
    "scripts/" + "build_",
    ".github/workflows/" + "normalize.yml",
    'workflows: ["Normalize"]',
)
PRODUCTION_ROOTS = (
    ROOT / ".github",
    ROOT / "src",
    ROOT / "scripts",
    ROOT / "tests",
    ROOT / "config",
    ROOT / "Makefile",
)
HISTORY_PARTS = {"migration", "migrations", "history", "historical"}
WORKFLOWS = ROOT / ".github" / "workflows"
ACTION_REF_RE = re.compile(r"uses:\s*([\w.-]+/[\w.-]+)@([^\s#]+)")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


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


def _is_history_path(path: Path) -> bool:
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return False
    return bool(HISTORY_PARTS.intersection(part.lower() for part in rel.parts))


def _legacy_ref_scan() -> list[str]:
    failures: list[str] = []
    patterns = FORBIDDEN_REFS + ("database/" + "services",)
    for root in PRODUCTION_ROOTS:
        paths = [root] if root.is_file() else root.rglob("*")
        for path in paths:
            if not path.is_file() or _is_history_path(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for forbidden in patterns:
                if forbidden in text:
                    failures.append(f"forbidden legacy reference in {path.relative_to(ROOT)}: {forbidden}")
    return failures


def main() -> int:
    failures: list[str] = []
    failures.extend(_legacy_ref_scan())

    for forbidden in (".github/workflows/" + "normalize.yml", "scripts/" + "pipeline.py"):
        if (ROOT / forbidden).exists():
            failures.append(f"obsolete production file exists: {forbidden}")

    for path in ROOT.joinpath("src", "engine").rglob("*.py"):
        if _python_imports_scripts(path):
            failures.append(f"V3 engine imports legacy scripts: {path.relative_to(ROOT)}")

    for path in WORKFLOWS.glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_REFS:
            if forbidden in text:
                failures.append(f"forbidden legacy reference in {path.relative_to(ROOT)}: {forbidden}")
        for action, ref in ACTION_REF_RE.findall(text):
            if action.startswith("actions/") and not SHA_RE.fullmatch(ref):
                failures.append(f"unpinned GitHub Action in {path.name}: {action}@{ref}")
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

    print(yaml.safe_dump({"schema": "architecture_gate_v2", "pass": not failures, "violations": failures}, sort_keys=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
