#!/usr/bin/env python3
"""build_mihomo.py — Emit Mihomo rule-provider YAML + classical .list via rule_loader.

Canonical input: rule_loader.load_service_rules()
  database/services/*.yaml  +  database/domains/*.txt  +  database/ips/*.txt

Large services (adblock etc.) stream-write YAML to avoid pyyaml memory/time cost.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "mihomo"
# Stream-write when total rules exceed this threshold
STREAM_THRESHOLD = 5_000

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rule_loader import load_service_rules  # noqa: E402


def bucket_counts(bucket: dict) -> int:
    return sum(
        len(bucket.get(k) or [])
        for k in (
            "domain",
            "domain_suffix",
            "domain_keyword",
            "domain_regex",
            "ip_cidr",
            "ip_cidr6",
        )
    )


def payload_items(bucket: dict) -> list[str]:
    domain = bucket.get("domain") or []
    domain_suffix = bucket.get("domain_suffix") or []
    domain_keyword = bucket.get("domain_keyword") or []
    domain_regex = bucket.get("domain_regex") or []
    ip_cidr = bucket.get("ip_cidr") or []
    ip_cidr6 = bucket.get("ip_cidr6") or []

    pure_domain = (
        not domain_keyword
        and not domain_regex
        and not ip_cidr
        and not ip_cidr6
    )
    if pure_domain:
        items: list[str] = []
        items.extend(domain)
        items.extend(f"+.{s}" for s in domain_suffix)
        return items

    items = []
    items.extend(domain)
    items.extend(f"+.{s}" for s in domain_suffix)
    items.extend(f"DOMAIN-KEYWORD,{k}" for k in domain_keyword)
    items.extend(f"DOMAIN-REGEX,{r}" for r in domain_regex)
    items.extend(f"IP-CIDR,{c}" for c in ip_cidr)
    items.extend(f"IP-CIDR6,{c}" for c in ip_cidr6)
    return items


def list_items(bucket: dict) -> list[str]:
    lines: list[str] = []
    for v in bucket.get("domain") or []:
        lines.append(f"DOMAIN,{v}")
    for v in bucket.get("domain_suffix") or []:
        lines.append(f"DOMAIN-SUFFIX,{v}")
    for v in bucket.get("domain_keyword") or []:
        lines.append(f"DOMAIN-KEYWORD,{v}")
    for v in bucket.get("domain_regex") or []:
        lines.append(f"DOMAIN-REGEX,{v}")
    for v in bucket.get("ip_cidr") or []:
        lines.append(f"IP-CIDR,{v},no-resolve")
    for v in bucket.get("ip_cidr6") or []:
        lines.append(f"IP-CIDR6,{v},no-resolve")
    return lines


def _yaml_escape(s: str) -> str:
    """Minimal YAML double-quote escape for payload strings."""
    if any(c in s for c in (":", "#", "{", "}", "[", "]", ",", "&", "*", "!", "|", ">", "'", '"', "%", "@", "`")) or s[:1] in (" ", "-") or s != s.strip():
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def write_payload_yaml(path: Path, items: list[str]) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("payload:\n")
        for item in items:
            f.write(f"- {_yaml_escape(item)}\n")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    buckets = load_service_rules()
    count = 0
    for bucket in buckets:
        sid = bucket["id"]
        n = bucket_counts(bucket)
        if n == 0:
            continue

        items = payload_items(bucket)
        list_lines = list_items(bucket)

        write_payload_yaml(OUT / f"{sid}.yaml", items)
        (OUT / f"{sid}.list").write_text(
            "\n".join(list_lines) + ("\n" if list_lines else ""),
            encoding="utf-8",
        )
        print(f"  mihomo {sid}: {n} rules")
        count += 1

    print(f"[build_mihomo] wrote {count} services → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
