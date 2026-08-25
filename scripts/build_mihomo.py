#!/usr/bin/env python3
"""build_mihomo.py — Emit Mihomo rule-provider YAML from database/services/"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
OUT = ROOT / "generated" / "mihomo"


def service_to_payload(doc: dict) -> list[str]:
    lines: list[str] = []
    for r in doc.get("rules", []):
        t, v = r["type"], r["value"]
        if t == "domain_suffix":
            lines.append(f"+.{v}")
        elif t == "domain":
            lines.append(v)
        elif t == "domain_keyword":
            lines.append(f"DOMAIN-KEYWORD,{v}")
        elif t == "domain_regex":
            lines.append(f"DOMAIN-REGEX,{v}")
        elif t == "ip_cidr":
            lines.append(f"IP-CIDR,{v}")
        elif t == "ip_cidr6":
            lines.append(f"IP-CIDR6,{v}")
        elif t == "asn":
            lines.append(f"IP-ASN,{v}")
    pure_domain = all(
        r["type"] in ("domain", "domain_suffix") for r in doc.get("rules", [])
    )
    if pure_domain:
        return [
            (f"+.{r['value']}" if r["type"] == "domain_suffix" else r["value"])
            for r in doc.get("rules", [])
        ]
    return lines


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not doc or not doc.get("rules"):
            continue
        payload = service_to_payload(doc)
        out_path = OUT / f"{doc['id']}.yaml"
        out_path.write_text(
            yaml.dump({"payload": payload}, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )
        list_lines = []
        for r in doc["rules"]:
            t, v = r["type"], r["value"]
            if t == "domain_suffix":
                list_lines.append(f"DOMAIN-SUFFIX,{v}")
            elif t == "domain":
                list_lines.append(f"DOMAIN,{v}")
            elif t == "domain_keyword":
                list_lines.append(f"DOMAIN-KEYWORD,{v}")
            elif t == "ip_cidr":
                list_lines.append(f"IP-CIDR,{v},no-resolve")
            elif t == "ip_cidr6":
                list_lines.append(f"IP-CIDR6,{v},no-resolve")
        (OUT / f"{doc['id']}.list").write_text(
            "\n".join(list_lines) + ("\n" if list_lines else ""), encoding="utf-8"
        )
        print(f"  mihomo {doc['id']}: {len(payload)} payload / {len(list_lines)} list")
        count += 1
    print(f"[build_mihomo] wrote {count} services → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
