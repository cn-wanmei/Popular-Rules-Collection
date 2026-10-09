#!/usr/bin/env python3
"""Phase F: validate the seven-client build contract from immutable build evidence."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-report", type=Path, default=None)
    args = ap.parse_args()
    path = args.build_report
    if path is None:
        latest = json.loads((ROOT / "reports/latest_release.json").read_text(encoding="utf-8"))
        path = ROOT / "data" / "runs" / latest["run_id"] / "artifacts" / "build_report.json"

    errors = []
    clients = {}
    if not path.is_file():
        errors.append(f"missing build report: {path}")
    else:
        report = json.loads(path.read_text(encoding="utf-8"))
        clients = report.get("clients") or {}
        missing = sorted(set(REQUIRED) - set(clients))
        if missing:
            errors.append("missing required clients: " + ", ".join(missing))
        for name in REQUIRED:
            item = clients.get(name) or {}
            if int(item.get("files", 0)) <= 0:
                errors.append(f"{name}: no generated files")
            if "input_rules" not in item or "emitted_rules" not in item:
                errors.append(f"{name}: missing input/emitted rule counts")
            unsupported = item.get("skipped_unsupported_rule_types")
            if not isinstance(unsupported, dict):
                errors.append(f"{name}: unsupported rule types are not explicitly recorded")

    payload = {
        "schema": "phase_f_client_consistency_v1",
        "build_report": str(path),
        "required_clients": list(REQUIRED),
        "pass": not errors,
        "errors": errors,
        "clients": clients,
        "semantics": "output-count equality is not required; client capability differences must be explicit",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
