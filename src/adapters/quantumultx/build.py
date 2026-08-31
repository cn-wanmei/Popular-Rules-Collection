from __future__ import annotations
"""V3 adapter — migrated from scripts/build_quantumultx.py. Output paths unchanged."""
#!/usr/bin/env python3
"""build_quantumultx.py — Quantumult X filter resources (streaming for large sets)."""

import sys
from pathlib import Path

import yaml

from src.adapters._common.paths import repo_root
ROOT = repo_root()
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
OUT = ROOT / "generated" / "quantumult-x"
LARGE = {"adblock", "china", "proxy", "gfw"}


def write_from_aggregates(sid: str, name: str) -> int:
    path = OUT / f"{sid}.list"
    n = 0
    with path.open("w", encoding="utf-8") as out:
        out.write(f"# {name} — Quantumult X filter\n")
        dfile = DOMAINS / f"{sid}.txt"
        if dfile.exists():
            with dfile.open(encoding="utf-8") as f:
                for line in f:
                    d = line.strip()
                    if d:
                        out.write(f"host-suffix, {d}\n")
                        n += 1
        ifile = IPS / f"{sid}.txt"
        if ifile.exists():
            with ifile.open(encoding="utf-8") as f:
                for line in f:
                    ip = line.strip()
                    if not ip:
                        continue
                    out.write(f"ip6-cidr, {ip}\n" if ":" in ip else f"ip-cidr, {ip}\n")
                    n += 1
    return n


def write_from_service(doc: dict) -> int:
    sid = doc["id"]
    lines: list[str] = [f"# {doc.get('name', sid)} — Quantumult X filter"]
    seen: set[str] = set()
    for r in doc.get("rules") or []:
        t, v = r.get("type"), r.get("value")
        if not t or not v:
            continue
        if t == "domain":
            lines.append(f"host, {v}")
            seen.add(v.lower())
        elif t == "domain_suffix":
            lines.append(f"host-suffix, {v}")
            seen.add(v.lower())
        elif t == "domain_keyword":
            lines.append(f"host-keyword, {v}")
        elif t == "ip_cidr":
            lines.append(f"ip-cidr, {v}")
        elif t == "ip_cidr6":
            lines.append(f"ip6-cidr, {v}")
    dfile = DOMAINS / f"{sid}.txt"
    if dfile.exists():
        for line in dfile.read_text(encoding="utf-8").splitlines():
            d = line.strip()
            if d and d.lower() not in seen:
                lines.append(f"host-suffix, {d}")
                seen.add(d.lower())
    ifile = IPS / f"{sid}.txt"
    if ifile.exists():
        for line in ifile.read_text(encoding="utf-8").splitlines():
            ip = line.strip()
            if not ip:
                continue
            lines.append(f"ip6-cidr, {ip}" if ":" in ip else f"ip-cidr, {ip}")
    (OUT / f"{sid}.list").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines) - 1


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
        print(f"  quantumult-x {sid}: {n}")
        count += 1
    print(f"[build_quantumultx] wrote {count} → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
