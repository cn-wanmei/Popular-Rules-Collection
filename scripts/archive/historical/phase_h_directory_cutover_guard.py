#!/usr/bin/env python3
"""Phase H: verify every prerequisite before any rule/ -> rules/ cutover."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def yaml_doc(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def json_doc(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def require_report(path: Path | None, label: str, errors: list[str]) -> dict:
    if path is None:
        errors.append(f"{label} report was not supplied")
        return {}
    if not path.is_file():
        errors.append(f"{label} report is missing: {path}")
        return {}
    try:
        return json_doc(path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label} report is invalid: {exc}")
        return {}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--migration", type=Path, default=ROOT / "config/canonical_root_migration.yaml")
    ap.add_argument("--phase-a-report", type=Path, default=None)
    ap.add_argument("--p0-report", type=Path, default=None)
    ap.add_argument("--intentional-report", type=Path, default=None)
    ap.add_argument("--client-report", type=Path, default=None)
    ap.add_argument("--determinism-report", type=Path, default=ROOT / "reports/v1/V3_DETERMINISM_FINAL.json")
    ap.add_argument("--dual-report", type=Path, default=None)
    ap.add_argument("--artifact-report", type=Path, default=None)
    ap.add_argument("--target-root", type=Path, default=ROOT / "rules")
    args = ap.parse_args()

    errors: list[str] = []
    migration = yaml_doc(args.migration) if args.migration.is_file() else {}
    if not args.migration.is_file():
        errors.append(f"migration config is missing: {args.migration}")
    if migration.get("status") != "CUTOVER_READY":
        errors.append(f"migration status is {migration.get('status')!r}, expected CUTOVER_READY")
    if migration.get("current_runtime_root") != "rule" or migration.get("target_runtime_root") != "rules":
        errors.append("migration root declaration is invalid")

    phase_a = require_report(args.phase_a_report, "Phase A", errors)
    if phase_a and phase_a.get("pass") is not True:
        errors.append("Phase A current-health report is not PASS")

    p0 = require_report(args.p0_report, "P0", errors)
    if p0 and (p0.get("production") != 50 or p0.get("pass") is not True):
        errors.append("P0 is not 50/50 production")

    intentional = require_report(args.intentional_report, "Phase C", errors)
    if intentional and (intentional.get("count") != 34 or intentional.get("pass") is not True):
        errors.append("Phase C intentional audit is not PASS")

    if not args.target_root.is_dir():
        errors.append(f"target canonical root is missing: {args.target_root}")
    else:
        supported = [
            p for p in args.target_root.rglob("*")
            if p.is_file() and p.suffix.lower() in {".yaml", ".yml", ".json", ".jsonl", ".list", ".txt", ".mmdb"}
        ]
        if not supported:
            errors.append(f"target canonical root contains no supported rule files: {args.target_root}")

    ci = ROOT / ".github" / "workflows" / "v1-loader.yml"
    ci_text = ci.read_text(encoding="utf-8") if ci.is_file() else ""
    if not ci.is_file() or "v1_loader rules/" not in ci_text or "v1_loader rule/" in ci_text:
        errors.append("V1 loader CI is not switched to target root")
    build = ROOT / ".github" / "workflows" / "build.yml"
    build_text = build.read_text(encoding="utf-8") if build.is_file() else ""
    if not build.is_file() or '"rules/**"' not in build_text:
        errors.append("main build CI does not watch target rules/**")
    if '"rule/**"' in build_text:
        errors.append("main build CI still watches legacy rule/** as a runtime source")

    dual = require_report(args.dual_report, "dual-track", errors)
    if dual and dual.get("pass") is not True:
        errors.append("dual-track equivalence report is not PASS")

    client = require_report(args.client_report, "seven-client", errors)
    if client and client.get("pass") is not True:
        errors.append("seven-client consistency report is not PASS")

    if not args.determinism_report.is_file():
        errors.append("missing determinism report")
    else:
        det = json_doc(args.determinism_report)
        if det.get("all_pass") is not True:
            errors.append("determinism report is not PASS")

    artifact = require_report(args.artifact_report, "artifact-equivalence", errors)
    if artifact and artifact.get("pass") is not True:
        errors.append("artifact equivalence report is not PASS")

    payload = {
        "schema": "phase_h_directory_cutover_guard_v2",
        "status": "CUTOVER_ALLOWED" if not errors else "CUTOVER_BLOCKED",
        "pass": not errors,
        "errors": errors,
        "warning": "This guard never performs the directory move itself.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
