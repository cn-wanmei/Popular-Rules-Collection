#!/usr/bin/env python3
"""generate_ecosystem_release_status.py

Cross-repo **read model** (not a new SSOT).
Pulls public signals from Collection / Source / Icon and writes a single JSON view.

Usage:
  python scripts/generate_ecosystem_release_status.py
  python scripts/generate_ecosystem_release_status.py --out reports/ecosystem_release_status.json
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA = {"User-Agent": "popular-rules-ecosystem-status/1.0"}


def fetch_text(url: str, timeout: int = 45) -> tuple[str | None, str | None]:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace"), None
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


def fetch_json(url: str) -> tuple[dict | list | None, str | None]:
    text, err = fetch_text(url)
    if err:
        return None, err
    try:
        return json.loads(text or ""), None
    except json.JSONDecodeError as exc:
        return None, f"JSONDecodeError: {exc}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("reports/ecosystem_release_status.json"),
    )
    args = ap.parse_args()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    sources = {
        "collection_publish_status": "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/PUBLISH_STATUS.md",
        "collection_main_sha": "https://api.github.com/repos/cn-wanmei/Popular-Rules-Collection/commits/main",
        "source_durable_bridge": "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source/main/reports/durable-bridge/latest.json",
        "icon_identity_snapshot": "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/main/config/collection_identity_snapshot.json",
        "icon_release_pointers": "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/main/config/release-pointers.yaml",
    }

    report: dict = {
        "schema": "ecosystem_release_status_v1",
        "generated_at": now,
        "authority_note": (
            "READ MODEL ONLY. Does not replace Collection/Source/Icon SSOT. "
            "See docs/STATE_MODEL.md."
        ),
        "repos": {
            "collection": "cn-wanmei/Popular-Rules-Collection",
            "source": "cn-wanmei/Popular-Rules-Source",
            "icon": "cn-wanmei/Popular-Rules-Icon",
        },
        "signals": {},
        "summary": {},
    }

    # Collection publish status (markdown → length + head)
    text, err = fetch_text(sources["collection_publish_status"])
    report["signals"]["collection_publish_status"] = {
        "url": sources["collection_publish_status"],
        "ok": err is None,
        "error": err,
        "bytes": len(text or ""),
        "preview": (text or "")[:400],
    }

    # Collection HEAD
    data, err = fetch_json(sources["collection_main_sha"])
    sha = None
    if isinstance(data, dict):
        sha = data.get("sha")
    report["signals"]["collection_main"] = {
        "url": sources["collection_main_sha"],
        "ok": err is None and bool(sha),
        "error": err,
        "sha": sha,
        "message": (data.get("commit") or {}).get("message") if isinstance(data, dict) else None,
    }

    # Source durable bridge
    data, err = fetch_json(sources["source_durable_bridge"])
    persisted = 0
    incomplete = []
    if isinstance(data, dict):
        services = data.get("services") or {}
        if isinstance(services, dict):
            persisted = sum(1 for v in services.values() if isinstance(v, dict) and v.get("status") == "PERSISTED")
        incomplete = data.get("incomplete") or []
    report["signals"]["source_durable_bridge"] = {
        "url": sources["source_durable_bridge"],
        "ok": err is None and isinstance(data, dict),
        "error": err,
        "persisted_count": persisted,
        "incomplete_count": len(incomplete) if isinstance(incomplete, list) else None,
        "persistence_commit": data.get("persistence_commit") if isinstance(data, dict) else None,
        "created_at": data.get("created_at") if isinstance(data, dict) else None,
    }

    # Icon identity snapshot
    data, err = fetch_json(sources["icon_identity_snapshot"])
    svc_count = None
    gen_at = None
    src_ref = None
    if isinstance(data, dict):
        svc_count = data.get("service_count")
        gen_at = data.get("generated_at")
        src = data.get("source")
        if isinstance(src, dict):
            src_ref = src.get("ref")
        elif isinstance(src, str):
            src_ref = src
    report["signals"]["icon_identity_snapshot"] = {
        "url": sources["icon_identity_snapshot"],
        "ok": err is None and isinstance(data, dict),
        "error": err,
        "service_count": svc_count,
        "generated_at": gen_at,
        "source_ref": src_ref,
    }

    # Icon release pointers (YAML as text preview)
    text, err = fetch_text(sources["icon_release_pointers"])
    report["signals"]["icon_release_pointers"] = {
        "url": sources["icon_release_pointers"],
        "ok": err is None,
        "error": err,
        "bytes": len(text or ""),
        "preview": (text or "")[:500],
    }

    report["summary"] = {
        "collection_head": report["signals"]["collection_main"].get("sha"),
        "source_durable_persisted": persisted,
        "icon_snapshot_services": svc_count,
        "icon_snapshot_generated_at": gen_at,
        "all_core_signals_ok": all(
            report["signals"][k].get("ok")
            for k in (
                "collection_main",
                "source_durable_bridge",
                "icon_identity_snapshot",
            )
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
