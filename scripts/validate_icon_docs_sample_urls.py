#!/usr/bin/env python3
from __future__ import annotations
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = [
    "docs/services/alibaba/taobao/README.md",
    "docs/services/apple/README.md",
    "docs/services/microsoft/README.md",
]
IMG_RE = re.compile(
    r'<img\s+src="(https://raw\.githubusercontent\.com/cn-wanmei/Popular-Rules-Icon/dist/v/[^"]+)"'
)

def check_url(url: str):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return None if getattr(resp, "status", 200) < 400 else f"HEAD {resp.status}"
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return None if resp.status < 400 else f"GET {resp.status}"
        except Exception as e:
            return str(e)

def main() -> int:
    errors = []
    checked = 0
    for rel in SAMPLES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        m = IMG_RE.search(text)
        if not m:
            errors.append(f"{rel}: no V6 dist img")
            continue
        err = check_url(m.group(1))
        checked += 1
        if err:
            errors.append(f"{rel}: {err}")
    if errors:
        print("validate_icon_docs_sample_urls: FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print(f"validate_icon_docs_sample_urls: OK (checked {checked})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
