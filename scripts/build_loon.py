#!/usr/bin/env python3
"""build_loon.py — Loon remote rule lists (.list), Surge-compatible syntax."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
OUT = ROOT / "generated" / "loon"
LARGE = {"adblock", "china", "proxy", "gfw"}


def write_from_aggregates(sid: str, name: str) -> int:
    path = OUT / f"{sid}.list"
    n = 0
    with path.open("w", encoding="utf-8") as out:
        out.write(f"# {name} — Loon remote rule\n# id: {sid}\n")
        dfile = DOMAINS / f"{sid}.txt"
        if dfile.exists():
            with dfile.open(encoding="utf-8") as f:
                for line in f:
                    d = line.strip()
                    if d:
                        out.write(f"DOMAIN-SUFFIX,{d}\n")
                        n += 1
        ifile = IPS / f"{sid}.txt"
        if ifile.exists():
            with ifile.open(encoding="utf-8") as f:
                for line in f:
                    ip = line.strip()
                    if not ip:
                        continue
                    out.write(
                        f"IP-CIDR6,{ip},no-resolve\n" if ":" in ip else f"IP-CIDR,{ip},no-resolve\n"
                    )
                    n += 1
    return n


def write_from_service(doc: dict) -> int:
    sid = doc["id"]
    name = doc.get("name", sid)
    lines: list[str] = [f"# {name} — Loon remote rule", f"# id: {sid}"]
    seen: set[str] = set()
    for r in doc.get("rules") or []:
        t, v = r.get("type"), r.get("value")
        if not t or not v:
            continue
        if t == "domain":
            lines.append(f"DOMAIN,{v}"); seen.add(v.lower())
        elif t == "domain_suffix":
            lines.append(f"DOMAIN-SUFFIX,{v}"); seen.add(v.lower())
        elif t == "domain_keyword":
            lines.append(f"DOMAIN-KEYWORD,{v}")
        elif t == "ip_cidr":
            lines.append(f"IP-CIDR,{v},no-resolve")
        elif t == "ip_cidr6":
            lines.append(f"IP-CIDR6,{v},no-resolve")
    dfile = DOMAINS / f"{sid}.txt"
    if dfile.exists():
        for line in dfile.read_text(encoding="utf-8").splitlines():
            d = line.strip()
            if d and d.lower() not in seen:
                lines.append(f"DOMAIN-SUFFIX,{d}"); seen.add(d.lower())
    ifile = IPS / f"{sid}.txt"
    if ifile.exists():
        for line in ifile.read_text(encoding="utf-8").splitlines():
            ip = line.strip()
            if ip:
                lines.append(
                    f"IP-CIDR6,{ip},no-resolve" if ":" in ip else f"IP-CIDR,{ip},no-resolve"
                )
    (OUT / f"{sid}.list").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return max(0, len(lines) - 2)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        name = doc.get("name", sid)
        n = write_from_aggregates(sid, name) if sid in LARGE else write_from_service(doc)
        if n <= 0:
            continue
        print(f"  loon {sid}: {n}")
        count += 1
    print(f"[build_loon] wrote {count} → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
