#!/usr/bin/env python3
"""build_surge.py — Emit Surge DOMAIN-SET / RULE-SET style lists via rule_loader.

Canonical input: rule_loader.load_service_rules()
Only write *_domain.list when domain_set is non-empty; remove stale empties.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "surge"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rule_loader import load_service_rules  # noqa: E402


def write_or_unlink(path: Path, lines: list[str]) -> None:
    if lines:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    elif path.exists():
        path.unlink()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    buckets = load_service_rules()
    count = 0
    for bucket in buckets:
        sid = bucket["id"]
        domain_set: list[str] = []
        rule_set: list[str] = []

        for v in bucket.get("domain") or []:
            domain_set.append(v)
            rule_set.append(f"DOMAIN,{v}")
        for v in bucket.get("domain_suffix") or []:
            domain_set.append(f".{v}")
            rule_set.append(f"DOMAIN-SUFFIX,{v}")
        for v in bucket.get("domain_keyword") or []:
            rule_set.append(f"DOMAIN-KEYWORD,{v}")
        for v in bucket.get("domain_regex") or []:
            rule_set.append(f"DOMAIN-REGEX,{v}")
        for v in bucket.get("ip_cidr") or []:
            rule_set.append(f"IP-CIDR,{v},no-resolve")
        for v in bucket.get("ip_cidr6") or []:
            rule_set.append(f"IP-CIDR6,{v},no-resolve")

        if not rule_set and not domain_set:
            continue

        write_or_unlink(OUT / f"{sid}.list", rule_set)
        write_or_unlink(OUT / f"{sid}_domain.list", domain_set)
        print(
            f"  surge {sid}: domain_set={len(domain_set)} rule_set={len(rule_set)}"
        )
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
