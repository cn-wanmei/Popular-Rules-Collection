#!/usr/bin/env python3
"""Derive per-run Service Production Evidence (NOT a second Service SSOT).

Writes:
  data/runs/<run_id>/reports/service_production_evidence.json

release_eligible / production are DERIVED from policy + run facts.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLIENTS = ["mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon"]


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def derive_for_service(sid: str, meta: dict, policy: dict, run_id: str, release_state: str) -> dict:
    mat = meta.get("materialization") or {}
    if isinstance(mat, str):
        mat_state, coverage = mat, "unknown"
    else:
        mat_state = mat.get("state") or "candidate"
        cov = mat.get("coverage") or meta.get("coverage") or {}
        if isinstance(cov, dict):
            coverage = cov.get("state") or "unknown"
        else:
            coverage = str(cov) if cov else "unknown"

    clients = {}
    for c in CLIENTS:
        clients[c] = {
            "eligible": True,  # refined later by capability matrix + rule types
            "semantic": "unknown",
            "artifact": "unknown",
        }

    blockers: list[str] = []
    if coverage == "partial":
        blockers.append("coverage_partial_forbids_production")

    identity_pass = bool(meta.get("provider") or (meta.get("identity") or {}).get("provider"))
    upstream_pass = mat_state in {"materialized", "verified_upstream", "production"}
    materialization_valid = mat_state == "materialized"
    coverage_policy_pass = coverage != "partial"
    no_blocker = len(blockers) == 0

    # Derived flags — never hand-authored as source of truth
    release_eligible = all(
        [
            identity_pass,
            upstream_pass,
            materialization_valid,
            coverage_policy_pass,
            no_blocker,
            release_state in {"RC_READY", "RELEASED", "PROMOTED"},
        ]
    )
    production_evidence_complete = release_eligible and all(
        clients[c]["semantic"] == "pass" for c in CLIENTS
    )
    # With semantic still unknown, production stays false
    production = production_evidence_complete and coverage != "partial"

    return {
        "service_id": sid,
        "identity": {
            "provider": meta.get("provider"),
            "materialization_state": mat_state,
            "coverage": coverage,
        },
        "runtime": {"run_id": run_id},
        "clients": clients,
        "semantic_probe": {"status": "unknown"},
        "release": {"run_level": release_state, "golden": "unknown"},
        "blockers": blockers,
        "derived": {
            "production_evidence_complete": production_evidence_complete,
            "release_eligible": release_eligible,
            "production": production,
        },
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    root = args.root
    run_dir = root / "data" / "runs" / args.run_id
    if not run_dir.is_dir():
        raise SystemExit(f"run not found: {run_dir}")

    policy = _load_yaml(root / "config" / "service_production_policy.yaml")
    services_doc = _load_yaml(root / "config" / "service_model" / "services.yaml")
    services = services_doc.get("services") or {}
    p0 = _load_yaml(root / "config" / "p0_materialization.yaml")
    p0_ids = {str(x.get("id")) for x in (p0.get("services") or []) if isinstance(x, dict)}

    manifest = _load_json(run_dir / "release" / "manifest.json")
    release_state = manifest.get("release_state") or "UNKNOWN"

    # Scope: P0 + materialized in service model (runtime-relevant), not all database/services
    selected = set(p0_ids)
    for sid, meta in services.items():
        if not isinstance(meta, dict):
            continue
        mat = meta.get("materialization") or {}
        state = mat.get("state") if isinstance(mat, dict) else mat
        if state == "materialized":
            selected.add(sid)

    items = []
    for sid in sorted(selected):
        meta = services.get(sid) or {}
        if not isinstance(meta, dict):
            meta = {"materialization": {"state": "candidate"}}
        items.append(derive_for_service(sid, meta, policy, args.run_id, release_state))

    out = {
        "schema": "service_production_evidence_v1",
        "run_id": args.run_id,
        "release_ssot": f"data/runs/{args.run_id}/release/manifest.json",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "config/service_production_policy.yaml",
        "scope": {
            "p0_count": len(p0_ids),
            "selected_count": len(selected),
            "note": "Excludes database/services legacy-only unless service_model runtime-relevant",
        },
        "summary": {
            "release_eligible_true": sum(1 for i in items if i["derived"]["release_eligible"]),
            "production_true": sum(1 for i in items if i["derived"]["production"]),
            "partial_blocked": sum(1 for i in items if "coverage_partial_forbids_production" in i["blockers"]),
        },
        "services": items,
    }
    reports = run_dir / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    target = reports / "service_production_evidence.json"
    target.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(target), "summary": out["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
