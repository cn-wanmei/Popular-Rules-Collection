#!/usr/bin/env python3
"""Write reports/ecosystem-release-lock.json (v1).

Pulls Source durable-bridge persistence_commit and Icon identity/release pointers.
Optional --require-icon-identity fails closed on SHA mismatch.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def fetch_repo_file_bytes(
    repository_full_name: str, path: str, ref: str = "main", timeout: int = 60
) -> bytes:
    # Use the Contents API for live branch files: raw.githubusercontent.com/main
    # may return pre-promotion content while the GitHub branch already advanced.
    url = (
        f"https://api.github.com/repos/{repository_full_name}/contents/{path}"
        f"?ref={ref}&v={time.time_ns()}"
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Popular-Rules-Collection-release-lock-writer",
            "Accept": "application/vnd.github.raw+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    # Decode an API JSON envelope only when it explicitly contains base64 file data.
    if raw.lstrip().startswith(b"{"):
        try:
            envelope = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            envelope = None
        if (
            isinstance(envelope, dict)
            and envelope.get("encoding") == "base64"
            and isinstance(envelope.get("content"), str)
        ):
            return base64.b64decode(envelope["content"])
    return raw


def fetch_repo_json(repository_full_name: str, path: str, ref: str = "main") -> dict:
    data = json.loads(fetch_repo_file_bytes(repository_full_name, path, ref=ref).decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object from {repository_full_name}/{path}")
    return data


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

    icon_snap = {}
    try:
        icon_snap = fetch_repo_json(
            "cn-wanmei/Popular-Rules-Icon", "config/collection_identity_snapshot.json"
        )
    except Exception as e:
        print(f"WARN: Icon snapshot: {e}")

    icon_sha = None
    icon_ref = None
    src = icon_snap.get("source") if isinstance(icon_snap, dict) else None
    if isinstance(src, dict):
        icon_sha = src.get("file_sha256") or src.get("file_sha")
        icon_ref = src.get("ref")

    if args.require_icon_identity:
        if not icon_sha:
            print("FAIL: Icon identity snapshot missing file_sha256")
            return 1
        if icon_sha != index_sha:
            print(
                f"FAIL: Icon identity sha256 {icon_sha} != Collection index {index_sha}\n"
                f"  Icon snapshot ref={icon_ref!r}\n"
                "  Recovery:\n"
                "    1) Run Popular-Rules-Icon workflow Identity Freshness\n"
                "    2) Merge the chore(icon) identity snapshot PR\n"
                "    3) Re-run this Publish Release Candidate workflow\n"
                "  Publish is fail-closed until Icon tracks the same rule/_index.yaml bytes."
            )
            return 1

    pointers: dict = {}
    try:
        import yaml

        pointers = yaml.safe_load(
            fetch_repo_file_bytes("cn-wanmei/Popular-Rules-Icon", "config/release-pointers.yaml")
        ) or {}
    except Exception as e:
        print(f"WARN: Icon release-pointers: {e}")

    durable: dict = {}
    try:
        durable = fetch_repo_json(
            "cn-wanmei/Popular-Rules-Source", "reports/durable-bridge/latest.json"
        )
    except Exception as e:
        print(f"WARN: Source durable-bridge: {e}")

    clients: dict = {}
    man = ROOT / "generated" / "manifest.json"
    if man.is_file():
        try:
            m = json.loads(man.read_text(encoding="utf-8"))
            if isinstance(m, dict):
                for k in ("clients", "client_digests", "artifacts", "by_client"):
                    if isinstance(m.get(k), dict):
                        clients.update({str(ck): cv for ck, cv in m[k].items()})
                        break
                if not clients and "digest" in m:
                    clients["manifest_digest"] = m.get("digest")
        except Exception as e:
            print(f"WARN: local manifest: {e}")

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
            "persistence_commit": durable.get("persistence_commit"),
            "run_completeness": durable.get("run_completeness"),
            "seal_completeness": durable.get("seal_completeness"),
            "persisted_count": durable.get("persisted_count"),
        },
        "icon": {
            "repository": "cn-wanmei/Popular-Rules-Icon",
            "branch": "dist",
            "release_id": pointers.get("production"),
            "rollback_id": pointers.get("rollback"),
            "frozen": pointers.get("frozen"),
            "collection_identity_ref": icon_ref,
            "collection_identity_sha256": icon_sha,
            "identity_matches_index": bool(icon_sha and icon_sha == index_sha),
        },
        "clients": clients,
    }

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {out} identity_ok={lock['icon']['identity_matches_index']} "
        f"source_persist={lock['source']['persistence_commit']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
