#!/usr/bin/env python3
"""Hard gate for P0 Service-level production readiness.

The repository pipeline can PASS while individual services remain unaudited.
This gate closes that gap by requiring explicit identity plus service-level
semantic/overlap/client/golden/release evidence before a P0 service is marked
production.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
P0_PATH = ROOT / "config" / "p0_materialization.yaml"
IDENTITY_PATH = ROOT / "config" / "p0_service_identity.yaml"
MATRIX_PATH = ROOT / "config" / "p0_service_production.yaml"
RUNS_DIR = ROOT / "data" / "runs"

CLIENT_EXT = {
    "mihomo": ".yaml",
    "singbox": ".json",
    "surge": ".list",
    "shadowrocket": ".list",
    "quantumultx": ".list",
    "egern": ".yaml",
    "loon": ".list",
}
HARD_FIELDS = (
    "identity",
    "source",
    "canonical",
    "semantic_audit",
    "overlap_audit",
    "seven_client",
    "golden",
    "release",
)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def latest_run() -> Path:
    candidates = [p for p in RUNS_DIR.iterdir() if p.is_dir()]
    if not candidates:
        raise RuntimeError("no data/runs build run is present")
    return sorted(candidates, key=lambda p: p.name)[-1]


def main() -> int:
    errors: list[str] = []
    p0 = load_yaml(P0_PATH).get("services") or []
    identity = load_yaml(IDENTITY_PATH).get("services") or []
    matrix = load_yaml(MATRIX_PATH).get("services") or {}

    p0_ids = [str(x.get("id")) for x in p0]
    if len(p0_ids) != 50 or len(set(p0_ids)) != 50:
        errors.append(f"P0 queue must contain exactly 50 unique services; found {len(p0_ids)}")

    identity_by_id = {str(x.get("id")): x for x in identity}
    if set(identity_by_id) != set(p0_ids):
        missing = sorted(set(p0_ids) - set(identity_by_id))
        extra = sorted(set(identity_by_id) - set(p0_ids))
        if missing:
            errors.append(f"P0 identity missing: {', '.join(missing)}")
        if extra:
            errors.append(f"P0 identity extra: {', '.join(extra)}")

    seen_provider: dict[str, str] = {}
    for sid, item in identity_by_id.items():
        provider = str(item.get("provider") or "")
        aggregate = str(item.get("aggregate") or "")
        if not provider or not aggregate:
            errors.append(f"{sid}: provider and aggregate are required")
        if sid == aggregate:
            errors.append(f"{sid}: service_id must differ from aggregate_id")
        prior = seen_provider.get(sid)
        if prior and prior != provider:
            errors.append(f"{sid}: provider ownership is not unique")
        seen_provider[sid] = provider

    if set(matrix) != set(p0_ids):
        errors.append("production matrix keys must exactly match P0 queue")

    run = latest_run()
    build_report_path = run / "artifacts" / "build_report.json"
    if not build_report_path.exists():
        errors.append(f"latest run missing build report: {build_report_path}")
        build_views = set()
        clients = {}
    else:
        build_report = json.loads(build_report_path.read_text(encoding="utf-8"))
        build_views = set(build_report.get("views", {}).get("services", []))
        clients = build_report.get("clients", {})

    for sid in p0_ids:
        if sid not in build_views:
            errors.append(f"{sid}: latest build has no service view")
        else:
            for client, ext in CLIENT_EXT.items():
                if client not in clients:
                    errors.append(f"{sid}: client {client} absent from build report")
                    continue
                artifact = run / "artifacts" / client / f"{sid}{ext}"
                if not artifact.exists() or artifact.stat().st_size == 0:
                    errors.append(f"{sid}: missing/empty {client} artifact {artifact.relative_to(ROOT)}")

    golden_path = run / "golden" / "report.json"
    release_path = run / "release" / "state.json"
    if golden_path.exists():
        golden = json.loads(golden_path.read_text(encoding="utf-8"))
        if not golden.get("all_pass"):
            errors.append("latest run golden_all_pass is false")
    else:
        errors.append("latest run golden report missing")
    if release_path.exists():
        release = json.loads(release_path.read_text(encoding="utf-8"))
        if not release.get("all_hard_pass"):
            errors.append("latest run release hard gates are not all pass")
    else:
        errors.append("latest run release state missing")

    blocked: list[str] = []
    production_count = 0
    for sid in p0_ids:
        row = matrix.get(sid) or {}
        failed = [field for field in HARD_FIELDS if row.get(field) != "pass"]
        status = row.get("status")
        if status == "production" and not failed:
            production_count += 1
        else:
            blocked.append(f"{sid}: " + (", ".join(failed) if failed else "status!=production"))

    print(f"[p0_service_production_gate] p0={len(p0_ids)} production={production_count} blocked={len(blocked)}")
    if blocked:
        print("BLOCKED SERVICES:")
        for item in blocked:
            print(f"  {item}")

    if errors:
        print("STRUCTURAL ERRORS:")
        for error in errors:
            print(f"  ERROR {error}")

    return 1 if errors or production_count != len(p0_ids) else 0


if __name__ == "__main__":
    raise SystemExit(main())
