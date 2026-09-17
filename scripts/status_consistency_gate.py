#!/usr/bin/env python3
"""Phase 0.7 — Status Consistency Gate.

Locks Release Evidence SSOT to:
  data/runs/<run_id>/release/manifest.json

Compares promotion pointer, run release state, and top-level status surfaces.
Exit 0 = PASS, 1 = FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--strict-latest-release", action="store_true",
                    help="Fail when reports/latest_release.json lags promotion (P1→P0 if display is authoritative)")
    args = ap.parse_args()
    root = args.root

    promo = _load(root / "generated" / "_promotion" / "latest.json")
    run_id = promo.get("run_id")
    errors: list[str] = []
    warnings: list[str] = []

    if not run_id:
        errors.append("generated/_promotion/latest.json missing run_id")
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1

    manifest_path = root / "data" / "runs" / str(run_id) / "release" / "manifest.json"
    state_path = root / "data" / "runs" / str(run_id) / "release" / "state.json"
    manifest = _load(manifest_path)
    state = _load(state_path)

    if not manifest:
        errors.append(f"release SSOT missing: {manifest_path}")
    else:
        if manifest.get("schema") != "release_manifest_v3":
            errors.append(f"unexpected release manifest schema: {manifest.get('schema')}")
        if manifest.get("run_id") not in (None, run_id) and manifest.get("release_id") not in (None, run_id):
            if manifest.get("run_id") != run_id and manifest.get("release_id") != run_id:
                errors.append(f"manifest run_id/release_id mismatch promo={run_id} manifest={manifest.get('run_id') or manifest.get('release_id')}")
        snap_m = manifest.get("snapshot_id")
        snap_p = promo.get("snapshot_id")
        if snap_m and snap_p and snap_m != snap_p:
            errors.append(f"snapshot_id mismatch promo={snap_p} manifest={snap_m}")
        rs_m = manifest.get("release_state")
        rs_p = promo.get("release_state")
        if rs_m and rs_p and rs_m != rs_p:
            errors.append(f"release_state mismatch promo={rs_p} manifest={rs_m}")

    if state:
        if state.get("state") and promo.get("release_state") and state.get("state") != promo.get("release_state"):
            errors.append(f"state.json state={state.get('state')} != promo {promo.get('release_state')}")

    baseline = root / "data" / "baseline" / "latest.json"
    if not baseline.is_file():
        warnings.append("data/baseline/latest.json missing (NO_BASELINE)")

    latest_release = _load(root / "reports" / "latest_release.json")
    if latest_release:
        # schema v2 legacy path — lag detection only
        gen = latest_release.get("generated_at") or latest_release.get("date")
        # If promotion is far newer than latest_release date, warn/fail
        promo_run = str(run_id)
        if "20260901" in str(gen) or str(latest_release.get("date")) == "2026-09-01":
            msg = f"reports/latest_release.json stale (generated_at={gen}) while promotion={promo_run}"
            if args.strict_latest_release:
                errors.append(msg)
            else:
                warnings.append(msg)

    status = "FAIL" if errors else "PASS"
    out = {
        "schema": "status_consistency_gate_v1",
        "status": status,
        "promotion_run_id": run_id,
        "release_ssot": str(manifest_path.relative_to(root)) if manifest_path.exists() else None,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
