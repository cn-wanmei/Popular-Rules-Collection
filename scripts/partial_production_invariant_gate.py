#!/usr/bin/env python3
"""CI hard invariant: coverage=partial MUST NEVER yield production=true.

Policy source: config/service_production_policy.yaml
Evidence source (optional): data/runs/<run_id>/reports/service_production_evidence.json
Service model is checked for forbidden explicit production + partial pairs.

This gate does not invent a second Service SSOT; it only rejects illegal states.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def coverage_of(meta: dict[str, Any]) -> str:
    cov = meta.get("coverage") or {}
    if isinstance(cov, dict):
        return str(cov.get("state") or "unknown").strip().lower()
    return str(cov or "unknown").strip().lower()


def mat_state_of(meta: dict[str, Any]) -> str:
    mat = meta.get("materialization") or {}
    if isinstance(mat, dict):
        return str(mat.get("state") or "unknown").strip().lower()
    return str(mat or "unknown").strip().lower()


def iter_services(model: dict[str, Any]):
    services = model.get("services")
    if isinstance(services, dict):
        for sid, meta in services.items():
            if isinstance(meta, dict):
                yield str(sid), meta
            else:
                yield str(sid), {}
    elif isinstance(services, list):
        for node in services:
            if isinstance(node, dict) and node.get("id"):
                yield str(node["id"]), node


def check_service_model(root: Path) -> list[str]:
    model = load_yaml(root / "config" / "service_model" / "services.yaml")
    errors: list[str] = []
    for sid, meta in iter_services(model):
        cov = coverage_of(meta)
        lifecycle = str(meta.get("lifecycle") or meta.get("status") or "").strip().lower()
        production_flag = meta.get("production")
        # Forbidden: explicit production truthy while coverage partial
        if cov == "partial" and (
            production_flag is True
            or str(production_flag).lower() in {"true", "yes", "1"}
            or lifecycle == "production"
            or mat_state_of(meta) == "production"
        ):
            errors.append(
                f"service_model:{sid}: coverage=partial forbids production "
                f"(lifecycle={lifecycle!r}, materialization={mat_state_of(meta)!r}, production={production_flag!r})"
            )
    return errors


def check_run_evidence(root: Path, run_id: str | None) -> list[str]:
    errors: list[str] = []
    if not run_id:
        promo = load_json(root / "generated" / "_promotion" / "latest.json")
        run_id = promo.get("run_id")
    if not run_id:
        return errors
    path = root / "data" / "runs" / str(run_id) / "reports" / "service_production_evidence.json"
    if not path.is_file():
        return errors
    data = load_json(path)
    for item in data.get("items") or []:
        cov = str((item.get("facts") or {}).get("coverage") or "").strip().lower()
        derived = item.get("derived") or {}
        if cov == "partial" and derived.get("production") is True:
            errors.append(
                f"evidence:{item.get('service')}: coverage=partial but derived.production=true"
            )
        if cov == "partial" and "coverage_partial_forbids_production" not in (item.get("blockers") or []):
            # Soft consistency: derive should always emit this blocker
            errors.append(
                f"evidence:{item.get('service')}: partial without coverage_partial_forbids_production blocker"
            )
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--run-id", default="")
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    policy = load_yaml(args.root / "config" / "service_production_policy.yaml")
    if not policy.get("principles", {}).get("partial_never_production", True):
        print("policy disables partial_never_production; gate skipped", file=sys.stderr)

    errors = check_service_model(args.root)
    errors.extend(check_run_evidence(args.root, args.run_id or None))
    result = {
        "schema": "partial_production_invariant_v1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "policy": "config/service_production_policy.yaml#partial_never_production",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
