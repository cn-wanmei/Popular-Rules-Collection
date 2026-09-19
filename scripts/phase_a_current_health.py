#!/usr/bin/env python3
"""Phase A: fail-closed current-state and post-deletion health audit."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected-head", default="")
    args = ap.parse_args()

    errors: list[str] = []
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if args.expected_head and head != args.expected_head:
        errors.append(f"HEAD mismatch: {head} != {args.expected_head}")

    latest_path = ROOT / "reports" / "latest_release.json"
    promotion_path = ROOT / "generated" / "_promotion" / "latest.json"
    if not latest_path.is_file():
        errors.append("missing reports/latest_release.json")
    if not promotion_path.is_file():
        errors.append("missing generated/_promotion/latest.json")

    latest = read_json(latest_path) if latest_path.is_file() else {}
    promotion = read_json(promotion_path) if promotion_path.is_file() else {}

    run_id = latest.get("run_id")
    if latest.get("release_state") != "RC_READY":
        errors.append(f"latest release_state={latest.get('release_state')!r}")
    if latest.get("quality_score") != 100:
        errors.append(f"latest quality_score={latest.get('quality_score')!r}")
    if latest.get("cas_verified") is not True:
        errors.append("latest cas_verified is not true")
    if promotion.get("release_state") != "RC_READY":
        errors.append(f"promotion release_state={promotion.get('release_state')!r}")
    if promotion.get("v2_runtime_dependency") != 0:
        errors.append(f"promotion v2_runtime_dependency={promotion.get('v2_runtime_dependency')!r}")
    if run_id and promotion.get("run_id") != run_id:
        errors.append("latest release and promotion run_id mismatch")

    _legacy_db = "database"
    _legacy_svc = "services"
    services_path = ROOT / _legacy_db / _legacy_svc
    if services_path.exists():
        errors.append(f"Legacy {_legacy_db}/{_legacy_svc} still exists after Phase 8 deletion")

    payload = {
        "schema": "phase_a_current_health_v1",
        "head": head,
        "latest_run_id": run_id,
        "release_state": latest.get("release_state"),
        "quality_score": latest.get("quality_score"),
        "cas_verified": latest.get("cas_verified"),
        "promotion_run_id": promotion.get("run_id"),
        "v2_runtime_dependency": promotion.get("v2_runtime_dependency"),
        "artifact_count": promotion.get("artifact_count"),
        "legacy_database_services_exists": services_path.exists(),
        "pass": not errors,
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
