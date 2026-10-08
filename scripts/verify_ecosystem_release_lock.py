#!/usr/bin/env python3
"""Verify reports/ecosystem-release-lock.json against live Collection index + Icon snapshot."""
from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "reports" / "ecosystem-release-lock.json"
INDEX = ROOT / "rule" / "_index.yaml"


def main() -> int:
    if not LOCK.is_file():
        print("FAIL: missing reports/ecosystem-release-lock.json")
        return 1
    if not INDEX.is_file():
        print("FAIL: missing rule/_index.yaml")
        return 1
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if lock.get("schema") != "popular_rules_ecosystem_release_lock_v1":
        print("FAIL: bad schema")
        return 1
    index_sha = hashlib.sha256(INDEX.read_bytes()).hexdigest()
    locked = (lock.get("collection") or {}).get("index_sha256")
    if locked != index_sha:
        print(f"FAIL: lock index_sha256 {locked} != live {index_sha}")
        return 1
    icon = lock.get("icon") or {}
    if icon.get("identity_matches_index") is False:
        print("FAIL: lock icon.identity_matches_index is false")
        return 1
    try:
        snap = json.loads(
            urllib.request.urlopen(
                "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/main/config/collection_identity_snapshot.json",
                timeout=60,
            ).read()
        )
        live_icon = (snap.get("source") or {}).get("file_sha256")
        if live_icon and live_icon != index_sha:
            print(f"WARN: Icon live snapshot {live_icon} != index {index_sha} (lock still ok if commit-scoped)")
    except Exception as e:
        print(f"WARN: Icon fetch {e}")
    print("OK: ecosystem-release-lock verifies against Collection index")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
