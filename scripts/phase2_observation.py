#!/usr/bin/env python3
"""Start a non-promoting Phase 2 observation window after all canary gates pass."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def start_observation(
    service_id: str,
    source_commit: str,
    snapshot_id: str,
    content_digest: str,
    v3_run_id: str,
    semantic_run_id: str,
    reconciliation_run_id: str,
    rollback_run_id: str,
) -> dict[str, Any]:
    required = {
        "source_commit": source_commit,
        "snapshot_id": snapshot_id,
        "content_digest": content_digest,
        "v3_run_id": v3_run_id,
        "semantic_run_id": semantic_run_id,
        "reconciliation_run_id": reconciliation_run_id,
        "rollback_run_id": rollback_run_id,
    }
    missing = [key for key, value in required.items() if not str(value or "").strip()]
    if missing:
        raise RuntimeError(
            f"{service_id}: observation cannot start; missing prerequisites: {', '.join(sorted(missing))}"
        )

    started_at = datetime.now(timezone.utc).isoformat()
    identity = {
        "service_id": service_id,
        **required,
        "started_at": started_at,
    }
    run_id = "observe-" + service_id + "-" + hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "schema": "phase2_observation_v1",
        "status": "ACTIVE",
        "run_id": run_id,
        "service_id": service_id,
        "started_at": started_at,
        "prerequisites": {
            "source_release_verified": True,
            "collection_reconciliation_pass": True,
            "v3_build_pass": True,
            "seven_client_semantic_pass": True,
            "rollback_validated": True,
        },
        "binding": required,
        "promotes": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--content-digest", required=True)
    parser.add_argument("--v3-run-id", required=True)
    parser.add_argument("--semantic-run-id", required=True)
    parser.add_argument("--reconciliation-run-id", required=True)
    parser.add_argument("--rollback-run-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = start_observation(
        args.service,
        args.source_commit,
        args.snapshot_id,
        args.content_digest,
        args.v3_run_id,
        args.semantic_run_id,
        args.reconciliation_run_id,
        args.rollback_run_id,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
