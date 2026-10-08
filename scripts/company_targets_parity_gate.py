#!/usr/bin/env python3
"""Fail if Collection company_targets.yaml diverges from Source SSOT (byte or sha256)."""
from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "config" / "company_targets.yaml"
REMOTE = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source/main/config/company_targets.yaml"


def main() -> int:
    if not LOCAL.is_file():
        print("missing local company_targets.yaml")
        return 1
    local = LOCAL.read_bytes()
    # strip Collection mirror banner for compare if present
    local_body = local
    if local.startswith(b"# SSOT_MIRROR"):
        local_body = b"\n".join(local.splitlines(True)[2:]) if local.count(b"\n") >= 2 else local
    remote = urllib.request.urlopen(REMOTE, timeout=60).read()
    remote_body = remote
    if remote.startswith(b"# SSOT_AUTHORITY"):
        remote_body = b"\n".join(remote.splitlines(True)[2:]) if remote.count(b"\n") >= 2 else remote
    # normalize: compare without first comment banners only
    lh = hashlib.sha256(local_body).hexdigest()
    rh = hashlib.sha256(remote_body).hexdigest()
    print(f"local_sha256={lh}")
    print(f"source_sha256={rh}")
    if local_body != remote_body:
        print("FAIL: company_targets diverged from Source SSOT")
        return 1
    print("OK: company_targets parity with Source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
