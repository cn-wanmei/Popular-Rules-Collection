#!/usr/bin/env python3
"""Read-only execution wrapper for the Batch 01 semantic/overlap audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.p0_batch01_semantic_overlap_audit import run_overlap, run_semantic

SEMANTIC = ROOT / "config/p0_batch01_semantic_audit.yaml"
OVERLAP = ROOT / "config/p0_batch01_overlap_audit.yaml"


def main() -> int:
    semantic = yaml.safe_load(SEMANTIC.read_text(encoding="utf-8")) or {}
    overlap = yaml.safe_load(OVERLAP.read_text(encoding="utf-8")) or {}

    semantic_result, service_rules = run_semantic(semantic)
    overlap_result = run_overlap(overlap, service_rules, semantic_result)

    report = {
        "schema": "p0_batch01_semantic_overlap_execution_v1",
        "batch": "01",
        "read_only": True,
        "semantic": semantic_result,
        "overlap": overlap_result,
        "summary": {
            "semantic_status": semantic_result.get("overall_status"),
            "overlap_status": overlap_result.get("status"),
            "runtime_probe_count": overlap_result.get("runtime_probe_count"),
            "runtime_collisions": overlap_result.get("runtime_collisions"),
            "services": {
                sid: {
                    "status": (spec or {}).get("status"),
                    "executed_rule_count": (spec or {}).get("executed_rule_count"),
                    "probe_count": len((spec or {}).get("probes") or []),
                }
                for sid, spec in (semantic_result.get("services") or {}).items()
            },
        },
    }

    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    # This wrapper records audit execution. Production eligibility is enforced
    # separately by the Phase J production gate, which requires semantic and
    # overlap evidence to be explicitly PASS for every P0 service.
    if report["summary"]["semantic_status"] == "fail":
        return 1
    if report["summary"]["overlap_status"] == "fail":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
