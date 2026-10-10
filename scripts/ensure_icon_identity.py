#!/usr/bin/env python3
"""Wait until Icon pins the exact Collection rule/_index.yaml content.

When the pin is stale, dispatch Icon Identity Freshness once and poll the
public snapshot until its content SHA-256 matches. This is an orchestration
helper only: the release-lock writer and Icon CI remain authoritative gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ICON_SNAPSHOT_URL = (
    "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/main/"
    "config/collection_identity_snapshot.json"
)
COLLECTION_INDEX_URL = (
    "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/"
    "rule/_index.yaml"
)
ICON_DISPATCH_URL = "https://api.github.com/repos/cn-wanmei/Popular-Rules-Icon/dispatches"


def fetch_snapshot(timeout: int = 20) -> dict:
    # Cache-bust the raw URL: the caller must observe a newly merged pin promptly.
    url = f"{ICON_SNAPSHOT_URL}?v={time.time_ns()}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Popular-Rules-Collection-identity-coordinator",
            "Accept": "application/vnd.github+json",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Icon identity snapshot root is not an object")
    return data


def fetch_current_collection_index(timeout: int = 30) -> bytes:
    # Cache-bust so stale build artifacts are never allowed to drive Icon backwards.
    url = f"{COLLECTION_INDEX_URL}?v={time.time_ns()}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Popular-Rules-Collection-identity-coordinator",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def pinned_sha(snapshot: dict) -> str:
    source = snapshot.get("source")
    if not isinstance(source, dict):
        return ""
    return str(source.get("file_sha256") or source.get("file_sha") or "").strip().lower()


def pinned_ref(snapshot: dict) -> str:
    source = snapshot.get("source")
    return str(source.get("ref") or "") if isinstance(source, dict) else ""


def current_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return os.environ.get("GITHUB_SHA", "unknown")


def dispatch_identity_refresh(token: str, source: str, collection_sha: str, index_sha: str) -> None:
    payload = {
        "event_type": "collection-identity-changed",
        "client_payload": {
            "source": source,
            "collection_sha": collection_sha,
            "index_sha256": index_sha,
        },
    }
    req = urllib.request.Request(
        ICON_DISPATCH_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Popular-Rules-Collection-identity-coordinator",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status not in (200, 201, 202, 204):
                raise RuntimeError(f"GitHub dispatch returned HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"GitHub rejected Icon identity dispatch (HTTP {exc.code}); "
            "verify ICON_DISPATCH_TOKEN repository secret and its cross-repository permission"
        ) from None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-path", type=Path, default=Path("rule/_index.yaml"))
    parser.add_argument("--source", default="ecosystem-release-lock")
    parser.add_argument(
        "--require-current-main-index",
        action="store_true",
        help="refuse to synchronize Icon to a build index that differs from current Collection main",
    )
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--poll-interval-seconds", type=int, default=10)
    args = parser.parse_args()

    if args.timeout_seconds < 1 or args.poll_interval_seconds < 1:
        parser.error("timeout and poll interval must be positive")
    if not args.index_path.is_file():
        raise SystemExit(f"Collection index not found: {args.index_path}")

    expected_sha = hashlib.sha256(args.index_path.read_bytes()).hexdigest()
    collection_sha = current_git_sha()
    print(
        f"Collection index identity: sha256={expected_sha}; "
        f"collection_ref={collection_sha}; source={args.source}",
        flush=True,
    )

    if args.require_current_main_index:
        try:
            main_index_sha = hashlib.sha256(fetch_current_collection_index()).hexdigest()
        except Exception as exc:
            raise SystemExit(f"Cannot read current Collection main index; refusing stale-build sync: {exc}") from None
        if main_index_sha != expected_sha:
            raise SystemExit(
                "Build index is stale relative to current Collection main; refusing to synchronize Icon "
                f"backward or publish stale rules (build_sha256={expected_sha}, "
                f"main_sha256={main_index_sha}). Rebuild from current main and retry Publish."
            )

    try:
        snapshot = fetch_snapshot()
    except Exception as exc:
        raise SystemExit(f"Cannot read Icon identity snapshot: {exc}") from None

    current_sha = pinned_sha(snapshot)
    if current_sha == expected_sha:
        print(f"Icon identity already matches ({current_sha}).", flush=True)
        return 0

    token = os.environ.get("ICON_DISPATCH_TOKEN", "").strip()
    if not token:
        raise SystemExit(
            "Icon identity is stale and ICON_DISPATCH_TOKEN is not configured. "
            f"Expected {expected_sha}, found {current_sha or '<missing>'}; "
            "refusing to write/publish a mismatched ecosystem lock."
        )

    print(
        f"Icon identity mismatch (found={current_sha or '<missing>'}, "
        f"ref={pinned_ref(snapshot)!r}); dispatching an exact-content refresh.",
        flush=True,
    )
    try:
        dispatch_identity_refresh(token, args.source, collection_sha, expected_sha)
    except Exception as exc:
        raise SystemExit(str(exc)) from None

    deadline = time.monotonic() + args.timeout_seconds
    last_reported = None
    while time.monotonic() < deadline:
        time.sleep(min(args.poll_interval_seconds, max(0, deadline - time.monotonic())))
        try:
            snapshot = fetch_snapshot()
            current_sha = pinned_sha(snapshot)
            current_ref = pinned_ref(snapshot)
            if current_sha == expected_sha:
                print(
                    f"Icon identity synchronized: sha256={current_sha}, ref={current_ref}.",
                    flush=True,
                )
                return 0
            state = (current_sha, current_ref)
            if state != last_reported:
                print(
                    f"Waiting for Icon CI + merge: pinned_sha={current_sha or '<missing>'}, "
                    f"pinned_ref={current_ref!r}; expected_sha={expected_sha}.",
                    flush=True,
                )
                last_reported = state
        except Exception as exc:
            print(f"Warning: transient Icon snapshot read failed: {exc}", flush=True)

    raise SystemExit(
        f"Timed out after {args.timeout_seconds}s waiting for Icon identity to match "
        f"Collection index sha256={expected_sha}; last pinned sha256={current_sha or '<missing>'}, "
        f"ref={pinned_ref(snapshot)!r}. No lock/publish promotion was performed."
    )


if __name__ == "__main__":
    sys.exit(main())
