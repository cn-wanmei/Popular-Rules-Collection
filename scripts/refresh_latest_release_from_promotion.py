#!/usr/bin/env python3
"""Phase 0.4 — Refresh reports/latest_release.json ONLY after Promotion SUCCESS.

SSOT remains: data/runs/<run_id>/release/manifest.json
This writer is a projection for humans/CI status, not a second release authority.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--run-id", default="")
    args = ap.parse_args()
    root = args.root

    promo = _load(root / "generated" / "_promotion" / "latest.json")
    run_id = args.run_id or promo.get("run_id")
    if not run_id:
        raise SystemExit("run_id required (arg or generated/_promotion/latest.json)")

    manifest = _load(root / "data" / "runs" / str(run_id) / "release" / "manifest.json")
    state = _load(root / "data" / "runs" / str(run_id) / "release" / "state.json")
    if not manifest:
        raise SystemExit(f"release SSOT missing for {run_id}")

    release_state = manifest.get("release_state") or state.get("state")
    if release_state not in {"RC_READY", "RELEASED", "PROMOTED"} and promo.get("release_state") not in {
        "RC_READY",
        "RELEASED",
        "PROMOTED",
    }:
        raise SystemExit(f"refusing to refresh latest_release for state={release_state!r}")

    # Only refresh when promotion pointer matches this run (post-promotion contract)
    if promo.get("run_id") and str(promo.get("run_id")) != str(run_id):
        raise SystemExit(
            f"promotion pointer run_id={promo.get('run_id')} != requested {run_id}"
        )

    now = datetime.now(timezone.utc).isoformat()
    out = {
        "schema_version": 3,
        "schema": "latest_release_projection_v3",
        "source": "promotion+release_manifest_v3",
        "generated_at": now,
        "run_id": run_id,
        "snapshot_id": manifest.get("snapshot_id") or promo.get("snapshot_id"),
        "release_state": release_state or promo.get("release_state"),
        "release_ssot": f"data/runs/{run_id}/release/manifest.json",
        "promotion_pointer": "generated/_promotion/latest.json",
        "canonical_digest": manifest.get("canonical_digest"),
        "ir_digest": manifest.get("ir_digest"),
        "golden_digest": manifest.get("golden_digest"),
        "quality_digest": manifest.get("quality_digest"),
        "metrics_digest": manifest.get("metrics_digest"),
        "client_digests": manifest.get("client_digests") or promo.get("client_digests"),
        "quality_score": promo.get("quality_score") or state.get("quality_score"),
        "cas_verified": promo.get("cas_verified", state.get("cas_verified")),
        "baseline_path": promo.get("baseline_path"),
        "note": "Projection only. Authority is data/runs/<run_id>/release/manifest.json after successful promotion.",
    }

    target = root / "reports" / "latest_release.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(target), "run_id": run_id, "release_state": out["release_state"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
