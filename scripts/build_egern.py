#!/usr/bin/env python3
"""build_egern.py — Egern native rule_set YAML (streaming for large sets)."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
OUT = ROOT / "generated" / "egern"
LARGE = {"adblock", "china", "proxy", "gfw"}


def write_large(sid: str, name: str) -> int:
    path = OUT / f"{sid}.yaml"
    n = 0
    with path.open("w", encoding="utf-8") as out:
        out.write(f"# name: {name}\n# id: {sid}\n")
        out.write("no_resolve: true\n")
        dfile = DOMAINS / f"{sid}.txt"
        if dfile.exists():
            out.write("domain_suffix_set:\n")
            with dfile.open(encoding="utf-8") as f:
                for line in f:
                    d = line.strip()
                    if d:
                        if any(c in d for c in ":#{}[]&*?|>!%@`"):
                            out.write(f'  - "{d}"\n')
                        else:
                            out.write(f"  - {d}\n")
                        n += 1
        ifile = IPS / f"{sid}.txt"
        v4, v6 = [], []
        if ifile.exists():
            with ifile.open(encoding="utf-8") as f:
                for line in f:
                    ip = line.strip()
                    if not ip:
                        continue
                    (v6 if ":" in ip else v4).append(ip)
                    n += 1
        if v4:
            out.write("ip_cidr_set:\n")
            for ip in v4:
                out.write(f"  - {ip}\n")
        if v6:
            out.write("ip_cidr6_set:\n")
            for ip in v6:
                out.write(f"  - {ip}\n")
    return n


def write_small(doc: dict) -> int:
    sid = doc["id"]
    name = doc.get("name", sid)
    domain, suffix, keyword, v4, v6 = [], [], [], [], []
    seen: set[str] = set()
    for r in doc.get("rules") or []:
        t, v = r.get("type"), r.get("value")
        if not t or not v:
            continue
        if t == "domain":
            domain.append(v); seen.add(v.lower())
        elif t == "domain_suffix":
            suffix.append(v); seen.add(v.lower())
        elif t == "domain_keyword":
            keyword.append(v)
        elif t == "ip_cidr":
            v4.append(v)
        elif t == "ip_cidr6":
            v6.append(v)
    dfile = DOMAINS / f"{sid}.txt"
    if dfile.exists():
        for line in dfile.read_text(encoding="utf-8").splitlines():
            d = line.strip()
            if d and d.lower() not in seen:
                suffix.append(d); seen.add(d.lower())
    ifile = IPS / f"{sid}.txt"
    if ifile.exists():
        for line in ifile.read_text(encoding="utf-8").splitlines():
            ip = line.strip()
            if not ip:
                continue
            (v6 if ":" in ip else v4).append(ip)
    body: dict = {"no_resolve": True}
    if domain:
        body["domain_set"] = domain
    if suffix:
        body["domain_suffix_set"] = suffix
    if keyword:
        body["domain_keyword_set"] = keyword
    if v4:
        body["ip_cidr_set"] = v4
    if v6:
        body["ip_cidr6_set"] = v6
    total = sum(len(body[k]) for k in body if isinstance(body[k], list))
    header = f"# name: {name}\n# id: {sid}\n# count: {total}\n"
    (OUT / f"{sid}.yaml").write_text(header + yaml.dump(body, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8")
    return total


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        name = doc.get("name", sid)
        n = write_large(sid, name) if sid in LARGE else write_small(doc)
        if n <= 0:
            continue
        print(f"  egern {sid}: {n}")
        count += 1
    print(f"[build_egern] wrote {count} → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
