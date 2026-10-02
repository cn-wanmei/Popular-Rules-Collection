#!/usr/bin/env python3
"""Collection icon_v6.yaml must match Icon release-pointers production/rollback."""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
ICON_REPO = "cn-wanmei/Popular-Rules-Icon"
RAW = "https://raw.githubusercontent.com/{repo}/{ref}/{path}"

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def fetch_yaml(repo: str, ref: str, path: str):
    url = RAW.format(repo=repo, ref=ref, path=path)
    with urllib.request.urlopen(url, timeout=60) as resp:
        return yaml.safe_load(resp.read().decode("utf-8"))

def main() -> int:
    local = load_yaml(ROOT / "config" / "icon_v6.yaml")
    v6 = local.get("v6") or {}
    rb = local.get("rollback") or {}
    local_prod = v6.get("release_id")
    local_rb = rb.get("release_id")

    remote = fetch_yaml(ICON_REPO, "main", "config/release-pointers.yaml")
    remote_prod = remote.get("production")
    remote_rb = remote.get("rollback")

    errors = []
    if local_prod != remote_prod:
        errors.append(f"production mismatch: Collection={local_prod!r} Icon={remote_prod!r}")
    if local_rb != remote_rb:
        errors.append(f"rollback mismatch: Collection={local_rb!r} Icon={remote_rb!r}")

    # optional: docs default release pin
    docs_cfg = ROOT / "config" / "icon_docs.yaml"
    if docs_cfg.exists():
        docs = load_yaml(docs_cfg)
        pin = docs.get("production_release_id")
        if pin and pin != remote_prod:
            errors.append(f"icon_docs.production_release_id={pin!r} != Icon production={remote_prod!r}")

    if errors:
        print("check_icon_pointers: FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print(f"check_icon_pointers: OK production={remote_prod} rollback={remote_rb}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
