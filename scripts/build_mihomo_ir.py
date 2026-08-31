#!/usr/bin/env python3
"""V2.4 Mihomo IR pilot — writes generated/mihomo_ir/ only; default mihomo unchanged."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from rule_loader import load_service_rules  # noqa: E402

IR = ROOT / "generated" / "ir" / "rules.jsonl"
OUT = ROOT / "generated" / "mihomo_ir"
PILOT = ("openai", "github", "telegram", "apple", "google", "microsoft", "discord")


def payload_items(bucket: dict) -> list[str]:
    domain = bucket.get("domain") or []
    domain_suffix = bucket.get("domain_suffix") or []
    domain_keyword = bucket.get("domain_keyword") or []
    domain_regex = bucket.get("domain_regex") or []
    ip_cidr = bucket.get("ip_cidr") or []
    ip_cidr6 = bucket.get("ip_cidr6") or []
    pure = not domain_keyword and not domain_regex and not ip_cidr and not ip_cidr6
    if pure:
        return list(domain) + [f"+.{s}" for s in domain_suffix]
    items = list(domain) + [f"+.{s}" for s in domain_suffix]
    items += [f"DOMAIN-KEYWORD,{k}" for k in domain_keyword]
    items += [f"DOMAIN-REGEX,{r}" for r in domain_regex]
    items += [f"IP-CIDR,{c}" for c in ip_cidr]
    items += [f"IP-CIDR6,{c}" for c in ip_cidr6]
    return items


def list_items(bucket: dict) -> list[str]:
    lines = []
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


def write_payload_yaml(path: Path, items: list[str]) -> None:
    path.write_text("payload:\n" + "".join(f"- {it}\n" for it in items), encoding="utf-8")


def buckets_from_ir(services: set[str]) -> dict:
    buckets = {}
    if not IR.exists():
        return buckets
    with IR.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            sid = rec.get("service")
            if sid not in services:
                continue
            m = rec.get("match") or {}
            typ, val = m.get("type"), m.get("value")
            if not typ or not val:
                continue
            b = buckets.setdefault(
                sid,
                {"id": sid, "domain": [], "domain_suffix": [], "domain_keyword": [], "domain_regex": [], "ip_cidr": [], "ip_cidr6": [], "_seen": defaultdict(set)},
            )
            key = str(val).lower().strip()
            if key in b["_seen"][typ]:
                continue
            b["_seen"][typ].add(key)
            if typ in b:
                b[typ].append(str(val).strip())
    for b in buckets.values():
        b.pop("_seen", None)
    return buckets


def main() -> int:
    services = set(PILOT)
    if not IR.exists():
        print("[build_mihomo_ir] WARN: no IR; rule_loader fallback")
        buckets = {sid: load_service_rules(sid)[0] for sid in services if load_service_rules(sid)}
        source = "rule_loader_fallback"
    else:
        buckets = buckets_from_ir(services)
        source = "universal_ir"
        for sid in services:
            if sid not in buckets:
                bl = load_service_rules(sid)
                if bl:
                    buckets[sid] = bl[0]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(
        "# Mihomo IR pilot (V2.4)\n\nParallel to generated/mihomo/. Not default.\n"
        f"Source: {source}\nPilot: {', '.join(PILOT)}\n",
        encoding="utf-8",
    )
    meta = {"source": source, "services": [], "pilot": list(PILOT)}
    count = 0
    for sid in sorted(buckets.keys()):
        bucket = buckets[sid]
        items, lines = payload_items(bucket), list_items(bucket)
        if not items and not lines:
            continue
        write_payload_yaml(OUT / f"{sid}.yaml", items)
        (OUT / f"{sid}.list").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        n = sum(len(bucket.get(k) or []) for k in ("domain", "domain_suffix", "domain_keyword", "domain_regex", "ip_cidr", "ip_cidr6"))
        meta["services"].append({"id": sid, "rules": n})
        print(f"  mihomo_ir {sid}: {n} rules")
        count += 1
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"[build_mihomo_ir] wrote {count} source={source}")
    return 0 if count else 1


if __name__ == "__main__":
    raise SystemExit(main())
