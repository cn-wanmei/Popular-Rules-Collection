#!/usr/bin/env python3
"""Phase C: validate and classify intentional-unmaterialized registry entries."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"NO_UPSTREAM", "COVERED_BY_AGGREGATE", "MAPS_TO", "DEFERRED_PROFILE", "KEYWORD_ONLY", "SOURCE_DRIFT"}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", type=Path, default=ROOT / "config/intentional_unmaterialized.yaml")
    args = ap.parse_args()
    doc = yaml.safe_load(args.registry.read_text(encoding="utf-8")) or {}
    services = doc.get("services") or {}
    errors = []
    rows = []
    for sid, item in sorted(services.items()):
        code = str((item or {}).get("code", "")).strip()
        reason = str((item or {}).get("reason", "")).strip()
        if code not in ALLOWED:
            errors.append(f"{sid}: invalid code {code!r}")
        if not reason:
            errors.append(f"{sid}: missing reason")
        rows.append({"id": sid, "code": code, "reason": reason})

    counts = {}
    for row in rows:
        counts[row["code"]] = counts.get(row["code"], 0) + 1

    payload = {
        "schema": "phase_c_intentional_audit_v1",
        "count": len(rows),
        "expected_count": 34,
        "code_counts": counts,
        "materialization_decision": "deferred_to_evidence_review",
        "pass": not errors and len(rows) == 34,
        "errors": errors,
        "entries": rows,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
