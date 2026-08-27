#!/usr/bin/env python3
"""source_snapshot.py — Phase 3A/3B: freeze source health + lifecycle view."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HEALTH = ROOT / "sources" / "health.yaml"
REGISTRY = ROOT / "sources" / "registry.yaml"
LIFECYCLE = ROOT / "config" / "source_lifecycle.yaml"
INTENTIONAL = ROOT / "config" / "intentional_unmaterialized.yaml"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()

    health = {}
    if HEALTH.exists():
        health = yaml.safe_load(HEALTH.read_text(encoding="utf-8")) or {}

    reg_sources = []
    if REGISTRY.exists():
        reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
        for s in reg.get("sources") or []:
            sid = s.get("id")
            h = (health.get("sources") or {}).get(sid) or {}
            files_failed = int(h.get("files_failed") or 0)
            status = h.get("status") or "unknown"
            if not s.get("enabled", True):
                life = "retired"
            elif status == "healthy" and files_failed == 0:
                life = "active"
            elif status == "degraded" or files_failed > 0:
                life = "degraded"
            else:
                life = status or "active"
            reg_sources.append(
                {
                    "id": sid,
                    "enabled": s.get("enabled", True),
                    "priority": s.get("priority"),
                    "rules_declared": h.get("rules_declared") or len(s.get("rules") or []),
                    "files_ok": h.get("files_ok"),
                    "files_failed": files_failed,
                    "health_status": status,
                    "lifecycle": life,
                    "last_success": h.get("last_success"),
                    "last_attempt": h.get("last_attempt"),
                }
            )

    intentional = {}
    if INTENTIONAL.exists():
        intentional = yaml.safe_load(INTENTIONAL.read_text(encoding="utf-8")) or {}

    snap = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": args.date,
        "sources": reg_sources,
        "intentional_unmaterialized": intentional.get("services") or intentional,
        "lifecycle_enum": ["active", "degraded", "unmaterialized", "review", "retired"],
    }
    day = ROOT / "reports" / args.date
    day.mkdir(parents=True, exist_ok=True)
    (day / "source_snapshot.json").write_text(
        json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    idx = {s["id"]: s["lifecycle"] for s in reg_sources if s.get("id")}
    LIFECYCLE.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "updated": args.date,
                "states": idx,
                "enum": snap["lifecycle_enum"],
                "policy": {
                    "active": "files_failed==0 and enabled",
                    "degraded": "files_failed>0 — keep visible, fix registry path explicitly",
                    "retired": "enabled:false — do not auto-delete history",
                    "unmaterialized": "see intentional_unmaterialized.yaml",
                },
            },
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    print(f"[source_snapshot] sources={len(reg_sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
