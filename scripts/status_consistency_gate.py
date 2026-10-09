#!/usr/bin/env python3
"""Status Consistency Gate (P1-02 / audit 2026-10-09).

Locks Release Evidence SSOT to:
  data/runs/<run_id>/release/manifest.json

Also enforces ecosystem read-model freshness and semantic consistency:
  - reports/ecosystem_release_status.json observation_status / icon_vs_collection
  - Hard SLA: STALE OBSERVATION or icon_vs_collection=error fails the gate
    (blocks production promotion when wired into publish.yml)

Exit 0 = PASS, 1 = FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Hard SLA for ecosystem read-model age (seconds). Soft labels live in the
# generator; this gate only fails on hard stale / semantic error.
ECOSYSTEM_HARD_AGE_SECONDS = 7 * 86400


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _age_seconds(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return max(0, int((datetime.now(timezone.utc) - t).total_seconds()))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument(
        "--strict-latest-release",
        action="store_true",
        help="Fail when reports/latest_release.json lags promotion",
    )
    ap.add_argument(
        "--skip-ecosystem",
        action="store_true",
        help="Skip ecosystem read-model checks (local/dev only)",
    )
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
        if manifest.get("run_id") not in (None, run_id) and manifest.get("release_id") not in (
            None,
            run_id,
        ):
            if manifest.get("run_id") != run_id and manifest.get("release_id") != run_id:
                errors.append(
                    f"manifest run_id/release_id mismatch promo={run_id} "
                    f"manifest={manifest.get('run_id') or manifest.get('release_id')}"
                )
        snap_m = manifest.get("snapshot_id")
        snap_p = promo.get("snapshot_id")
        if snap_m and snap_p and snap_m != snap_p:
            errors.append(f"snapshot_id mismatch promo={snap_p} manifest={snap_m}")
        rs_m = manifest.get("release_state")
        rs_p = promo.get("release_state")
        if rs_m and rs_p and rs_m != rs_p:
            errors.append(f"release_state mismatch promo={rs_p} manifest={rs_m}")

    if state:
        if state.get("state") and promo.get("release_state") and state.get("state") != promo.get(
            "release_state"
        ):
            errors.append(
                f"state.json state={state.get('state')} != promo {promo.get('release_state')}"
            )

    baseline = root / "data" / "baseline" / "latest.json"
    if not baseline.is_file():
        warnings.append("data/baseline/latest.json missing (NO_BASELINE)")

    latest_release = _load(root / "reports" / "latest_release.json")
    if latest_release:
        gen = latest_release.get("generated_at") or latest_release.get("date")
        promo_run = str(run_id)
        if "20260901" in str(gen) or str(latest_release.get("date")) == "2026-09-01":
            msg = f"reports/latest_release.json stale (generated_at={gen}) while promotion={promo_run}"
            if args.strict_latest_release:
                errors.append(msg)
            else:
                warnings.append(msg)

    # --- P1-02: ecosystem read-model hard gate ---
    eco_path = root / "reports" / "ecosystem_release_status.json"
    eco_summary: dict = {}
    if not args.skip_ecosystem:
        eco = _load(eco_path)
        if not eco:
            warnings.append(
                "reports/ecosystem_release_status.json missing; "
                "run Ecosystem Status workflow before production promotion"
            )
        else:
            summary = eco.get("summary") if isinstance(eco.get("summary"), dict) else {}
            eco_summary = {
                "observation_status": summary.get("observation_status") or eco.get("observation_status"),
                "icon_vs_collection": summary.get("icon_vs_collection"),
                "semantic_consistency": summary.get("semantic_consistency"),
                "generated_at": eco.get("generated_at") or eco.get("observed_at"),
            }
            obs = str(eco_summary.get("observation_status") or "")
            icon_sem = str(eco_summary.get("icon_vs_collection") or "")
            overall_sem = str(eco_summary.get("semantic_consistency") or "")
            gen_at = eco_summary.get("generated_at")
            age = _age_seconds(gen_at if isinstance(gen_at, str) else None)

            if obs == "STALE OBSERVATION":
                errors.append(
                    "ecosystem observation_status=STALE OBSERVATION "
                    f"(generated_at={gen_at}); refresh Ecosystem Status before promotion"
                )
            if icon_sem == "error":
                errors.append(
                    "ecosystem icon_vs_collection=error; "
                    "resolve Icon identity drift (Identity Freshness) before promotion"
                )
            if overall_sem == "error":
                errors.append(
                    "ecosystem semantic_consistency=error; "
                    "resolve Source/Icon semantic issues before promotion"
                )
            if age is not None and age > ECOSYSTEM_HARD_AGE_SECONDS:
                errors.append(
                    f"ecosystem read-model age {age}s exceeds hard SLA "
                    f"{ECOSYSTEM_HARD_AGE_SECONDS}s (generated_at={gen_at})"
                )
            if age is None and gen_at:
                warnings.append(f"could not parse ecosystem generated_at={gen_at!r}")

    status = "FAIL" if errors else "PASS"
    out = {
        "schema": "status_consistency_gate_v2",
        "status": status,
        "promotion_run_id": run_id,
        "release_ssot": str(manifest_path.relative_to(root)) if manifest_path.exists() else None,
        "ecosystem": eco_summary or None,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
