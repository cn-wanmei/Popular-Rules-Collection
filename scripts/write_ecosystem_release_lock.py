#!/usr/bin/env python3
"""Write reports/ecosystem-release-lock.json (v1). Fail-closed if Icon snapshot SHA mismatch when --require-icon-identity."""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def git_head() -> str:
    head = ROOT / ".git" / "HEAD"
    if not head.exists():
        return "unknown"
    ref = head.read_text(encoding="utf-8").strip()
    if ref.startswith("ref:"):
        ref_path = ROOT / ".git" / ref.split(" ", 1)[1].strip()
        if ref_path.exists():
            return ref_path.read_text(encoding="utf-8").strip()
    return ref


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default="")
    ap.add_argument("--require-icon-identity", action="store_true")
    ap.add_argument("--out", default="reports/ecosystem-release-lock.json")
    args = ap.parse_args()

    index = ROOT / "rule" / "_index.yaml"
    if not index.is_file():
        print("missing rule/_index.yaml")
        return 1
    index_sha = sha256_file(index)
    commit = git_head()

    icon_snap = None
    try:
        icon_snap = fetch_json(
            "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/main/config/collection_identity_snapshot.json"
        )
    except Exception as e:
        print(f"WARN: could not fetch Icon snapshot: {e}")

    icon_sha = None
    icon_ref = None
    if icon_snap and isinstance(icon_snap.get("source"), dict):
        icon_sha = icon_snap["source"].get("file_sha256")
        icon_ref = icon_snap["source"].get("ref")

    if args.require_icon_identity:
        if not icon_sha:
            print("FAIL: Icon identity snapshot missing file_sha256")
            return 1
        if icon_sha != index_sha:
            print(f"FAIL: Icon identity sha256 {icon_sha} != Collection index {index_sha}")
            return 1

    pointers = {}
    try:
        import yaml

        pointers = yaml.safe_load(
            urllib.request.urlopen(
                "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/main/config/release-pointers.yaml"
            ).read()
        ) or {}
    except Exception as e:
        print(f"WARN: Icon release-pointers: {e}")

    lock = {
        "schema": "popular_rules_ecosystem_release_lock_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collection": {
            "commit": commit,
            "index_sha256": index_sha,
            "run_id": args.run_id or None,
        },
        "source": {
            "repository": "cn-wanmei/Popular-Rules-Source",
            "persistence_commit": None,
            "note": "Fill persistence_commit from durable-bridge report when available",
        },
        "icon": {
            "repository": "cn-wanmei/Popular-Rules-Icon",
            "branch": "dist",
            "release_id": pointers.get("production"),
            "collection_identity_ref": icon_ref,
            "collection_identity_sha256": icon_sha,
            "identity_matches_index": bool(icon_sha and icon_sha == index_sha),
        },
        "clients": {},
    }

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} identity_ok={lock['icon']['identity_matches_index']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
