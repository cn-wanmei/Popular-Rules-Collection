#!/usr/bin/env python3
"""Validate release, baseline, promotion and client evidence consistency."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = yaml.safe_load(fh) or {}
    if not isinstance(value, dict):
        raise ValueError(f"expected YAML mapping: {path}")
    return value


def canonical_baseline_present(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size == 0:
        return False
    try:
        value = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    return bool(value)


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def validate(root: Path = ROOT, run_id: str | None = None, require_latest: bool = False) -> dict[str, Any]:
    policy = load_yaml(root / "config/evidence_policy.yaml")
    promotion = load_json(root / policy["status_consistency"]["promotion_pointer"])
    selected_run = run_id or promotion.get("run_id")
    if not selected_run:
        raise ValueError("no run_id available")

    manifest_path = root / policy["release_evidence"]["ssot"].format(run_id=selected_run)
    baseline_path = root / policy["baseline"]["evidence_path"].format(run_id=selected_run)
    canonical_path = root / policy["baseline"]["canonical_path"]
    canonical_present = canonical_baseline_present(canonical_path)

    errors: list[str] = []
    warnings: list[str] = []
    if not manifest_path.exists():
        errors.append(f"release manifest missing: {manifest_path}")
        manifest: dict[str, Any] = {}
    else:
        manifest = load_json(manifest_path)

    release_state = manifest.get("release_state")
    if release_state != policy["release_evidence"]["required_state"]:
        errors.append(f"release_state must be {policy['release_evidence']['required_state']}, got {release_state!r}")
    if manifest.get("run_id") != selected_run:
        errors.append(f"manifest run_id mismatch: expected {selected_run}, got {manifest.get('run_id')!r}")
    if promotion.get("run_id") != selected_run:
        errors.append(f"promotion run_id mismatch: expected {selected_run}, got {promotion.get('run_id')!r}")
    for field in ("snapshot_id", "release_state"):
        if promotion.get(field) != manifest.get(field):
            errors.append(f"promotion/manifest {field} mismatch: {promotion.get(field)!r} != {manifest.get(field)!r}")

    required_clients = set(load_yaml(root / policy["evidence"]["clients_from"]).get("clients", {}))
    manifest_clients = set((manifest.get("client_digests") or {}).keys())
    missing_clients = sorted(required_clients - manifest_clients)
    extra_clients = sorted(manifest_clients - required_clients)
    if missing_clients:
        errors.append(f"manifest missing required clients: {missing_clients}")
    if extra_clients:
        warnings.append(f"manifest has non-policy clients: {extra_clients}")

    if manifest.get("v2_runtime_dependency") != 0:
        errors.append(f"v2_runtime_dependency must be 0, got {manifest.get('v2_runtime_dependency')!r}")

    baseline = load_json(baseline_path) if baseline_path.exists() else {}
    if policy["baseline"].get("enabled"):
        if not baseline_path.exists():
            errors.append(f"baseline evidence missing: {baseline_path}")
        decision = baseline.get("decision")
        declared_path = baseline.get("baseline_path")
        if canonical_present and decision == "NO_BASELINE":
            errors.append("baseline contradiction: canonical baseline exists but evidence decision is NO_BASELINE")
        if canonical_present and not declared_path and policy["baseline"].get("require_declared_path_when_present"):
            errors.append("baseline contradiction: canonical baseline exists but baseline_path is null")
        if declared_path and not (root / declared_path).exists():
            errors.append(f"baseline evidence points to missing path: {declared_path}")

    latest_path = root / policy["status_consistency"]["latest_release_path"]
    latest = load_json(latest_path) if latest_path.exists() else None
    if latest is None:
        warnings.append(f"latest release report missing: {latest_path}")
    else:
        mismatches = []
        for field in ("run_id", "snapshot_id", "release_state"):
            if field in latest and latest.get(field) != manifest.get(field):
                mismatches.append(field)
        if mismatches:
            message = f"latest_release stale/mismatched fields: {mismatches}"
            if require_latest:
                errors.append(message)
            else:
                warnings.append(message)

    generated_at = parse_timestamp(manifest.get("generated_at"))
    ttl_days = int(policy["evidence"].get("ttl_days", 7))
    if generated_at is not None:
        age_days = (datetime.now(timezone.utc) - generated_at).total_seconds() / 86400
        if age_days > ttl_days:
            errors.append(f"release evidence older than TTL ({age_days:.2f}d > {ttl_days}d)")
    else:
        warnings.append("manifest generated_at is absent or invalid")

    result = {
        "schema": "evidence_consistency_v1",
        "run_id": selected_run,
        "snapshot_id": manifest.get("snapshot_id"),
        "release_state": release_state,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "release_manifest_ssot": manifest_path.as_posix(),
            "baseline_evidence": baseline_path.as_posix(),
            "canonical_baseline_present": canonical_present,
            "required_clients": sorted(required_clients),
            "manifest_clients": sorted(manifest_clients),
        },
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--run-id")
    parser.add_argument("--require-latest", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = validate(args.root, args.run_id, args.require_latest)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
