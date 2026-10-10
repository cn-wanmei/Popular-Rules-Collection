#!/usr/bin/env python3
"""Verify ecosystem release lock against current Collection index and live Icon identity.

This is a production consistency gate, not a best-effort diagnostic. A missing,
stale or unreadable Icon snapshot must fail closed rather than emit a warning.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "reports" / "ecosystem-release-lock.json"
INDEX = ROOT / "rule" / "_index.yaml"
ICON_SNAPSHOT_URL = (
    "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/main/"
    "config/collection_identity_snapshot.json"
)


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def read_live_icon_snapshot() -> dict:
    # Cache-bust the raw URL so verification does not depend on a stale CDN copy.
    url = f"{ICON_SNAPSHOT_URL}?v={time.time_ns()}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Popular-Rules-Collection-release-lock-verifier",
            "Cache-Control": "no-cache",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        snapshot = json.loads(response.read().decode("utf-8"))
    if not isinstance(snapshot, dict):
        raise ValueError("Icon snapshot root is not an object")
    return snapshot


def main() -> int:
    if not LOCK.is_file():
        return fail("missing reports/ecosystem-release-lock.json")
    if not INDEX.is_file():
        return fail("missing rule/_index.yaml")

    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"could not parse ecosystem-release-lock.json: {exc}")

    if not isinstance(lock, dict) or lock.get("schema") != "popular_rules_ecosystem_release_lock_v1":
        return fail("bad ecosystem release lock schema")

    index_sha = hashlib.sha256(INDEX.read_bytes()).hexdigest()
    collection = lock.get("collection") if isinstance(lock.get("collection"), dict) else {}
    locked_index_sha = str(collection.get("index_sha256") or "").strip().lower()
    if locked_index_sha != index_sha:
        return fail(f"lock index_sha256 {locked_index_sha or '<missing>'} != live {index_sha}")

    icon = lock.get("icon") if isinstance(lock.get("icon"), dict) else {}
    locked_icon_sha = str(icon.get("collection_identity_sha256") or "").strip().lower()
    if icon.get("identity_matches_index") is not True:
        return fail("lock icon.identity_matches_index is not true")
    if locked_icon_sha != index_sha:
        return fail(
            f"lock icon.collection_identity_sha256 {locked_icon_sha or '<missing>'} != live index {index_sha}"
        )

    try:
        snapshot = read_live_icon_snapshot()
    except Exception as exc:
        return fail(f"could not read live Icon identity snapshot: {exc}")

    source = snapshot.get("source") if isinstance(snapshot.get("source"), dict) else {}
    live_icon_sha = str(source.get("file_sha256") or source.get("file_sha") or "").strip().lower()
    if not live_icon_sha:
        return fail("live Icon identity snapshot has no file_sha256/file_sha")
    if live_icon_sha != index_sha:
        return fail(
            f"live Icon identity sha256 {live_icon_sha} != Collection index {index_sha}; "
            "refresh Icon identity before promoting this lock"
        )

    print(
        "OK: ecosystem-release-lock verifies against current Collection index and live Icon identity "
        f"(index_sha256={index_sha}, icon_ref={source.get('ref')!r})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
