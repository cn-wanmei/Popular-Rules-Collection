#!/usr/bin/env python3
"""build_surge.py — Emit Surge DOMAIN-SET / RULE-SET style lists.
Only write *_domain.list when domain_set is non-empty; remove stale empties.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
OUT = ROOT / "generated" / "surge"


def write_or_unlink(path: Path, lines: list[str]) -> None:
    if lines:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    elif path.exists():
        path.unlink()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not doc or not doc.get("rules"):
            continue
        domain_set: list[str] = []
        rule_set: list[str] = []
        for r in doc["rules"]:
            t, v = r["type"], r["value"]
            if t == "domain_suffix":
                domain_set.append(f".{v}")
                rule_set.append(f"DOMAIN-SUFFIX,{v}")
            elif t == "domain":
                domain_set.append(v)
                rule_set.append(f"DOMAIN,{v}")
            elif t == "domain_keyword":
                rule_set.append(f"DOMAIN-KEYWORD,{v}")
            elif t == "ip_cidr":
                rule_set.append(f"IP-CIDR,{v},no-resolve")
            elif t == "ip_cidr6":
                rule_set.append(f"IP-CIDR6,{v},no-resolve")
        sid = doc["id"]
        write_or_unlink(OUT / f"{sid}.list", rule_set)
        write_or_unlink(OUT / f"{sid}_domain.list", domain_set)
        print(f"  surge {sid}: domain_set={len(domain_set)} rule_set={len(rule_set)}")
        count += 1
    # purge any leftover empty domain-set files (stale)
    for p in OUT.glob("*_domain.list"):
        if p.stat().st_size == 0:
            p.unlink()
            print(f"  removed stale empty {p.name}")
    print(f"[build_surge] wrote {count} services → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
