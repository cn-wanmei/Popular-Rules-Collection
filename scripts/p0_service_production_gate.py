#!/usr/bin/env python3
"""Hard gate for P0 Service-level production readiness.

PR/report mode validates the control-plane shape and reports blocked services.
Default mode is the release hard gate: every P0 service must have complete
service-level evidence before it can be marked production.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

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
    "identity", "source", "canonical", "semantic_audit",
    "overlap_audit", "seven_client", "golden", "release",
)


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def latest_run() -> Path:
    if not RUNS_DIR.is_dir():
        raise RuntimeError("no data/runs directory is present")
    candidates = [p for p in RUNS_DIR.iterdir() if p.is_dir()]
    if not candidates:
        raise RuntimeError("no data/runs build run is present")
    return max(candidates, key=lambda p: p.name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    structural_errors: list[str] = []
    p0 = load_yaml(P0_PATH).get("services") or []
    identity = load_yaml(IDENTITY_PATH).get("services") or []
    matrix = load_yaml(MATRIX_PATH).get("services") or {}

    p0_ids = [str(x.get("id")) for x in p0 if isinstance(x, dict) and x.get("id")]
    if len(p0_ids) != 50 or len(set(p0_ids)) != 50:
        structural_errors.append(f"P0 queue must contain exactly 50 unique services; found {len(p0_ids)}")

    identity_by_id = {str(x.get("id")): x for x in identity if isinstance(x, dict) and x.get("id")}
    if set(identity_by_id) != set(p0_ids):
        structural_errors.append("P0 identity keys must exactly match P0 queue")

    seen_provider: dict[str, str] = {}
    for sid, item in identity_by_id.items():
        provider = str(item.get("provider") or "")
        aggregate = str(item.get("aggregate") or "")
        if not provider or not aggregate:
            structural_errors.append(f"{sid}: provider and aggregate are required")
        if sid == aggregate:
            structural_errors.append(f"{sid}: service_id must differ from aggregate_id")
        if sid in seen_provider and seen_provider[sid] != provider:
            structural_errors.append(f"{sid}: provider ownership is not unique")
        seen_provider[sid] = provider

    if set(matrix) != set(p0_ids):
        structural_errors.append("production matrix keys must exactly match P0 queue")

    try:
        run = latest_run()
    except RuntimeError as exc:
        structural_errors.append(str(exc))
        run = None

    build_views: set[str] = set()
    clients: dict = {}
    if run is not None:
        report_path = run / "artifacts" / "build_report.json"
        if not report_path.exists():
            structural_errors.append("latest run missing build_report.json")
        else:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            build_views = set((report.get("views") or {}).get("services") or [])
            clients = report.get("clients") or {}

    service_client_files: dict[str, list[str]] = {}
    blocked: list[str] = []
    production_count = 0

    for sid in p0_ids:
        row = matrix.get(sid) or {}
        failed = [field for field in HARD_FIELDS if row.get(field) != "pass"]
        present: list[str] = []
        if run is not None:
            for client, ext in CLIENT_EXT.items():
                if client not in clients:
                    continue
                artifact = run / "artifacts" / client / f"{sid}{ext}"
                if artifact.is_file() and artifact.stat().st_size > 0:
                    present.append(client)
        service_client_files[sid] = present

        if row.get("seven_client") == "pass" and len(present) != len(CLIENT_EXT):
            missing = sorted(set(CLIENT_EXT) - set(present))
            structural_errors.append(
                f"{sid}: seven_client=pass but artifacts missing for {', '.join(missing)}"
            )
        if row.get("status") == "production" and not failed:
            production_count += 1
        else:
            blocked.append(f"{sid}: {', '.join(failed) if failed else 'status!=production'}")

    if run is not None:
        golden_path = run / "golden" / "report.json"
        release_path = run / "release" / "state.json"
        if not golden_path.exists():
            structural_errors.append("latest run golden report missing")
        elif not json.loads(golden_path.read_text(encoding="utf-8")).get("all_pass"):
            structural_errors.append("latest run golden_all_pass is false")
        if not release_path.exists():
            structural_errors.append("latest run release state missing")
        elif not json.loads(release_path.read_text(encoding="utf-8")).get("all_hard_pass"):
            structural_errors.append("latest run release hard gates are not all pass")

    print(f"[p0_service_production_gate] p0={len(p0_ids)} production={production_count} blocked={len(blocked)}")
    for sid in p0_ids:
        print(f"  {sid}: client_artifacts={len(service_client_files.get(sid, []))}/{len(CLIENT_EXT)} view={'yes' if sid in build_views else 'no'}")
    if blocked:
        print("BLOCKED SERVICES:")
        for item in blocked:
            print(f"  {item}")
    if structural_errors:
        print("STRUCTURAL ERRORS:")
        for error in structural_errors:
            print(f"  ERROR {error}")

    # Report-only means blocked production is expected, but malformed control-plane
    # state remains a real CI error.
    if args.report_only:
        return 1 if structural_errors else 0
    return 1 if structural_errors or production_count != len(p0_ids) else 0


if __name__ == "__main__":
    raise SystemExit(main())
