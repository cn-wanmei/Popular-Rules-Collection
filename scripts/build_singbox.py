#!/usr/bin/env python3
"""build_singbox.py — Emit sing-box JSON rule-set (text format; SRS binary later)"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
OUT = ROOT / "generated" / "sing-box"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not doc or not doc.get("rules"):
            continue
        domain = []
        domain_suffix = []
        domain_keyword = []
        domain_regex = []
        ip_cidr = []
        for r in doc["rules"]:
            t, v = r["type"], r["value"]
            if t == "domain":
                domain.append(v)
            elif t == "domain_suffix":
                domain_suffix.append(v)
            elif t == "domain_keyword":
                domain_keyword.append(v)
            elif t == "domain_regex":
                domain_regex.append(v)
            elif t in ("ip_cidr", "ip_cidr6"):
                ip_cidr.append(v)
        headless = {"version": 2, "rules": []}
        rule: dict = {}
        if domain:
            rule["domain"] = sorted(set(domain))
        if domain_suffix:
            rule["domain_suffix"] = sorted(set(domain_suffix))
        if domain_keyword:
            rule["domain_keyword"] = sorted(set(domain_keyword))
        if domain_regex:
            rule["domain_regex"] = sorted(set(domain_regex))
        if ip_cidr:
            rule["ip_cidr"] = sorted(set(ip_cidr))
        if rule:
            headless["rules"].append(rule)
        out = OUT / f"{doc['id']}.json"
        out.write_text(json.dumps(headless, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  sing-box {doc['id']}: {sum(len(v) if isinstance(v, list) else 0 for v in rule.values())} items")
        count += 1
    print(f"[build_singbox] wrote {count} services → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
