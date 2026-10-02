#!/usr/bin/env python3
"""Spot-check default V6 icon URLs in a few service READMEs return HTTP 200."""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = [
    "docs/services/alibaba/taobao/README.md",
    "docs/services/apple/README.md",
    "docs/services/microsoft/README.md",
]
IMG_RE = re.compile(r'<img\s+src="(https://raw\.githubusercontent\.com/cn-wanmei/Popular-Rules-Icon/dist/v/[^"]+)"')

def main() -> int:
    errors = []
    for rel in SAMPLES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing sample {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        m = IMG_RE.search(text)
        if not m:
            errors.append(f"{rel}: no V6 dist img src")
            continue
        url = m.group(1)
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as resp:
                code = getattr(resp, "status", 200)
                if code >= 400:
                    errors.append(f"{rel}: HEAD {code} {url}")
        except urllib.error.HTTPError as e:
            # some CDNs dislike HEAD — try GET range
            try:
                req = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    if resp.status >= 400:
                        errors.append(f"{rel}: GET {resp.status} {url}")
            except Exception as e2:
                errors.append(f"{rel}: {e} / {e2}")
        except Exception as e:
            errors.append(f"{rel}: {e}")
    if errors:
        print("validate_icon_docs_sample_urls: FAIL")
        for e in errors:
            print(" ", e)
        return 1
    print("validate_icon_docs_sample_urls: OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
