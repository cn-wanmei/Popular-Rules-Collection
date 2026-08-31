from __future__ import annotations
"""V3 adapter — migrated from scripts/build_singbox.py. Output paths unchanged."""
#!/usr/bin/env python3
"""build_singbox.py — Emit sing-box JSON rule-set via rule_loader."""

import json
import sys
from pathlib import Path

from src.adapters._common.paths import repo_root
ROOT = repo_root()
OUT = ROOT / "generated" / "sing-box"

from src.adapters._common.rule_loader import load_service_rules  # noqa: E402

KEYS = (
    "domain",
    "domain_suffix",
    "domain_keyword",
    "domain_regex",
    "ip_cidr",
    "ip_cidr6",
)


def write_json_stream(path: Path, bucket: dict) -> int:
    n = 0
    with path.open("w", encoding="utf-8") as f:
        f.write('{\n  "version": 2,\n  "rules": [\n    {\n')
        first_key = True
        for key in KEYS:
            vals = bucket.get(key) or []
            if not vals:
                continue
            if not first_key:
                f.write(",\n")
            first_key = False
            f.write(f'      "{key}": [\n')
            for i, v in enumerate(vals):
                comma = "," if i < len(vals) - 1 else ""
                f.write(f"        {json.dumps(v, ensure_ascii=False)}{comma}\n")
            f.write("      ]")
            n += len(vals)
        f.write("\n    }\n  ]\n}\n")
    return n


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    buckets = load_service_rules()
    count = 0
    for bucket in buckets:
        sid = bucket["id"]
        has_any = any(bucket.get(k) for k in KEYS)
        if not has_any:
            continue
        n = write_json_stream(OUT / f"{sid}.json", bucket)
        print(f"  sing-box {sid}: {n} items")
        count += 1
    print(f"[build_singbox] wrote {count} services → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
