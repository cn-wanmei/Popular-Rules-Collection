#!/usr/bin/env python3
"""Spot-check default V6 icon URLs in service READMEs return HTTP 200."""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = [
    "docs/services/alibaba/taobao/README.md",
    "docs/services/apple/README.md",
    "docs/services/microsoft/README.md",
    "docs/services/google/google/README.md",
]
IMG_RE = re.compile(
    r'<img\s+src="(https://raw\.githubusercontent\.com/cn-wanmei/Popular-Rules-Icon/dist/v/[^"]+)"'
)

def check_url(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as resp:
            if getattr(resp, "status", 200) >= 400:
                return f"HEAD {resp.status}"
            return None
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status >= 400:
                    return f"GET {resp.status}"
                return None
        except Exception as e:
            return str(e)

def main() -> int:
    errors = []
    checked = 0
    for rel in SAMPLES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing sample {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        m = IMG_RE.search(text)
        if not m:
            # discover under provider
            prov = path.parent
            found = None
            for cand in prov.rglob("README.md"):
                t = cand.read_text(encoding="utf-8", errors="ignore")
                m2 = IMG_RE.search(t)
                if m2:
                    found = (cand, m2)
                    break
            if not found:
                errors.append(f"{rel}: no V6 dist img src")
                continue
            path, m = found[0], found[1]
            rel = str(path.relative_to(ROOT))
        err = check_url(m.group(1))
        checked += 1
        if err:
            errors.append(f"{rel}: {err} {m.group(1)}")
    if errors:
        print("validate_icon_docs_sample_urls: FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print(f"validate_icon_docs_sample_urls: OK (checked {checked})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
