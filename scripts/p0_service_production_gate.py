#!/usr/bin/env python3
"""Hard gate for P0 Service-level production readiness.

PR/report mode validates the control-plane shape and reports blocked services.
Default mode is the Phase 0 exit hard gate: every P0 service must have complete
service-level evidence before it can be marked production.

RC publish must use --report-only until Phase 0 exits. Production is derived
and currently 0/50 (coverage=partial forbids production); blocking every
release candidate on that exit criterion starves the promotion lane.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
P0_PATH = CONFIG_DIR / "p0_materialization.yaml"
IDENTITY_PATH = CONFIG_DIR / "p0_service_identity.yaml"
MATRIX_PATH = CONFIG_DIR / "p0_service_production.yaml"
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


def resolve_run(run_id: str | None) -> Path:
    if run_id:
        path = RUNS_DIR / run_id
        if not path.is_dir():
            raise RuntimeError(f"run not found: {path}")
        return path
    return latest_run()


def service_client_artifact(
    run: Path, client: str, ext: str, sid: str, provider: str = "",
) -> Path | None:
    """Locate a per-service client artifact under the directory contract.

    Canonical layout: artifacts/<client>/<provider>/<service>/<service><ext>
    Legacy flat layout is accepted only as a migration fallback.
    Promoted layout: generated/<client>/<provider>/<service>/<service><ext>
    """
    search_roots: list[Path] = []
    if run is not None:
        search_roots.append(run / "artifacts" / client)
    search_roots.append(ROOT / "generated" / client)
    for client_dir in search_roots:
        candidates: list[Path] = []
        if provider:
            candidates.append(client_dir / provider / sid / f"{sid}{ext}")
        candidates.append(client_dir / f"{sid}{ext}")
        for path in candidates:
            if path.is_file() and path.stat().st_size > 0:
                return path
        if client_dir.is_dir():
            for path in client_dir.rglob(f"{sid}/{sid}{ext}"):
                if path.is_file() and path.stat().st_size > 0:
                    return path
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument(
        "--run-id",
        default="",
        help="Pin the gate to a specific data/runs/<run-id> directory",
    )
    return parser.parse_args()


def evidence_bundles() -> dict[str, dict[str, dict]]:
    """Load every batch evidence bundle without making batch 01 special."""
    bundles: dict[str, dict[str, dict]] = {}
    for path in sorted(CONFIG_DIR.glob("p0_batch*_source_evidence.yaml")):
        batch = load_yaml(path).get("batch")
        if batch is not None:
            bundles.setdefault(str(batch), {})["source"] = load_yaml(path)
    for path in sorted(CONFIG_DIR.glob("p0_batch*_canonical_membership.yaml")):
        batch = load_yaml(path).get("batch")
        if batch is not None:
            bundles.setdefault(str(batch), {})["canonical"] = load_yaml(path)
    for path in sorted(CONFIG_DIR.glob("p0_batch*_semantic_audit.yaml")):
        batch = load_yaml(path).get("batch")
        if batch is not None:
            bundles.setdefault(str(batch), {})["semantic"] = load_yaml(path)
    for path in sorted(CONFIG_DIR.glob("p0_batch*_overlap_audit.yaml")):
        batch = load_yaml(path).get("batch")
        if batch is not None:
            bundles.setdefault(str(batch), {})["overlap"] = load_yaml(path)
    return bundles


def evidence_errors_for_service(sid: str, bundles: dict[str, dict[str, dict]]) -> list[str]:
    errors: list[str] = []
    found = False
    for batch, bundle in bundles.items():
        services = set()
        for key in ("source", "canonical", "semantic"):
            services.update((bundle.get(key, {}).get("services") or {}).keys())
        if sid not in services:
            continue
        found = True
        source = (bundle.get("source", {}).get("services") or {}).get(sid) or {}
        canonical = (bundle.get("canonical", {}).get("services") or {}).get(sid) or {}
        semantic = (bundle.get("semantic", {}).get("services") or {}).get(sid) or {}
        overlap = bundle.get("overlap", {})

        snapshot = source.get("immutable_snapshot") or {}
        snapshot_path = snapshot.get("path")
        snapshot_hash = snapshot.get("sha256")
        if snapshot.get("status") != "complete" or not snapshot_path or not snapshot_hash:
            errors.append(f"{sid}: batch {batch} source snapshot is not complete")
        else:
            absolute = ROOT / snapshot_path
            if not absolute.is_file():
                errors.append(f"{sid}: batch {batch} snapshot file is missing: {snapshot_path}")
            else:
                actual = hashlib.sha256(absolute.read_bytes()).hexdigest()
                if actual != str(snapshot_hash).lower():
                    errors.append(f"{sid}: batch {batch} snapshot sha256 mismatch")

        if canonical.get("status") != "complete":
            errors.append(f"{sid}: batch {batch} canonical membership is not complete")
        else:
            if canonical.get("snapshot") != snapshot_path:
                errors.append(f"{sid}: batch {batch} canonical snapshot linkage mismatch")
            for membership in canonical.get("memberships") or []:
                typ = str(membership.get("type") or "").strip().lower()
                value = str(membership.get("value") or "").strip().lower()
                expected_key = f"{typ}|{value}"
                if membership.get("identity_key") != expected_key:
                    errors.append(f"{sid}: batch {batch} canonical identity_key mismatch for {expected_key}")
                expected_id = hashlib.sha256(expected_key.encode("utf-8")).hexdigest()
                if str(membership.get("rule_id") or "").lower() != expected_id:
                    errors.append(f"{sid}: batch {batch} canonical rule_id mismatch for {expected_key}")

        if semantic.get("snapshot") != snapshot_path:
            errors.append(f"{sid}: batch {batch} semantic snapshot linkage mismatch")
        if semantic.get("status") != "pass":
            errors.append(f"{sid}: batch {batch} semantic audit is not pass")
        probes = semantic.get("probes") or []
        if semantic.get("status") == "pass" and not probes:
            errors.append(f"{sid}: batch {batch} semantic audit has no probes")

        scoped_services = set((overlap.get("scope") or {}).get("services") or [])
        if sid not in scoped_services:
            errors.append(f"{sid}: batch {batch} overlap audit scope does not include service")
        if overlap.get("status") != "pass":
            errors.append(f"{sid}: batch {batch} overlap audit is not pass")
    if not found:
        errors.append(f"{sid}: no independent source/canonical/semantic/overlap evidence bundle found")
    return errors


def main() -> int:
    args = parse_args()
    structural_errors: list[str] = []
    p0 = load_yaml(P0_PATH).get("services") or []
    identity = load_yaml(IDENTITY_PATH).get("services") or []
    matrix = load_yaml(MATRIX_PATH).get("services") or {}
    bundles = evidence_bundles()

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
        run = resolve_run(args.run_id or None)
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

    derived_report = {}
    derived_path = run / "reports" / "phase_j_p0_service_evidence.json" if run is not None else None
    if derived_path is not None and derived_path.is_file():
        try:
            derived_report = json.loads(derived_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            structural_errors.append(f"invalid Phase J derived evidence report: {exc}")

    service_client_files: dict[str, list[str]] = {}
    blocked: list[str] = []
    production_count = 0

    phase_j_complete = bool(
        isinstance(derived_report, dict)
        and derived_report.get("production_complete") is True
    )

    for sid in p0_ids:
        row = matrix.get(sid) or {}
        failed = [field for field in HARD_FIELDS if row.get(field) != "pass"]
        evidence_errors = evidence_errors_for_service(sid, bundles)
        if all(row.get(field) == "pass" for field in ("source", "canonical", "semantic_audit", "overlap_audit")):
            structural_errors.extend(evidence_errors)
        present: list[str] = []
        if run is not None:
            provider = str((identity_by_id.get(sid) or {}).get("provider") or "")
            for client, ext in CLIENT_EXT.items():
                if client not in clients:
                    continue
                artifact = service_client_artifact(run, client, ext, sid, provider)
                if artifact is not None:
                    present.append(client)
        service_client_files[sid] = present

        if row.get("seven_client") == "pass" and len(present) != len(CLIENT_EXT):
            missing = sorted(set(CLIENT_EXT) - set(present))
            # Before Phase J globally completes, per-service artifact materialization
            # is a pending activation item rather than a structural queue error.
            if phase_j_complete:
                structural_errors.append(
                    f"{sid}: seven_client=pass but artifacts missing for {', '.join(missing)}"
                )
        derived_row = (derived_report.get("services") or {}).get(sid) if isinstance(derived_report, dict) else None
        derived_status = derived_row.get("status") if isinstance(derived_row, dict) else None
        ready_now = (
            phase_j_complete
            and derived_status == "production"
            and not failed
            and not evidence_errors
            and len(present) == len(CLIENT_EXT)
        )
        if ready_now:
            production_count += 1
        else:
            blocked_reasons = failed or ["status!=production"]
            if evidence_errors and all(row.get(field) == "pass" for field in HARD_FIELDS):
                blocked_reasons.extend(["evidence:" + e.split(": ", 1)[-1] for e in evidence_errors])
            blocked.append(f"{sid}: {', '.join(blocked_reasons)}")

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

    if isinstance(derived_report, dict) and derived_report:
        report_count = int(derived_report.get("queue_size", len(p0_ids)))
        if report_count != len(p0_ids):
            structural_errors.append(
                f"Phase J derived evidence queue_size={report_count}, expected {len(p0_ids)}"
            )

    # Per-service Phase J observations remain informational while the global
    # P0 queue is partial. Production activation is fail-closed on the explicit
    # production_complete flag.
    if not phase_j_complete:
        production_count = 0
        blocked = [
            f"{sid}: phase_j_production_complete=false"
            for sid in p0_ids
        ]

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

    if args.report_only:
        return 1 if structural_errors else 0
    return 1 if structural_errors or production_count != len(p0_ids) else 0


if __name__ == "__main__":
    raise SystemExit(main())
