#!/usr/bin/env python3
"""Phase H: verify all prerequisites before any rule/ -> rules/ cutover."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def yaml_doc(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--migration", type=Path, default=ROOT / "config/canonical_root_migration.yaml")
    ap.add_argument("--p0-report", type=Path, default=None)
    ap.add_argument("--client-report", type=Path, default=None)
    ap.add_argument("--determinism-report", type=Path, default=ROOT / "reports/v1/V3_DETERMINISM_FINAL.json")
    ap.add_argument("--dual-report", type=Path, default=None)
    args = ap.parse_args()

    errors = []
    migration = yaml_doc(args.migration) if args.migration.is_file() else {}
    if migration.get("status") != "CUTOVER_READY":
        errors.append(f"migration status is {migration.get('status')!r}, expected CUTOVER_READY")
    if migration.get("current_runtime_root") != "rule" or migration.get("target_runtime_root") != "rules":
        errors.append("migration root declaration is invalid")

    if args.p0_report:
        p0 = json.loads(args.p0_report.read_text(encoding="utf-8"))
        if p0.get("production") != 50 or p0.get("pass") is not True:
            errors.append("P0 is not 50/50 production")
    else:
        errors.append("P0 report was not supplied")

    if args.client_report:
        client = json.loads(args.client_report.read_text(encoding="utf-8"))
        if client.get("pass") is not True:
            errors.append("seven-client consistency report is not PASS")
    else:
        errors.append("seven-client report was not supplied")

    if args.dual_report:
        dual = json.loads(args.dual_report.read_text(encoding="utf-8"))
        if dual.get("pass") is not True:
            errors.append("dual-track equivalence report is not PASS")
    else:
        errors.append("dual-track report was not supplied")

    if not args.determinism_report.is_file():
        errors.append("missing determinism report")
    else:
        det = json.loads(args.determinism_report.read_text(encoding="utf-8"))
        if det.get("all_pass") is not True:
            errors.append("determinism report is not PASS")

    payload = {
        "schema": "phase_h_directory_cutover_guard_v1",
        "status": "CUTOVER_ALLOWED" if not errors else "CUTOVER_BLOCKED",
        "pass": not errors,
        "errors": errors,
        "warning": "This guard never performs the directory move itself.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
