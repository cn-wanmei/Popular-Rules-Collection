from __future__ import annotations
"""V3 adapter — migrated from scripts/build_shadowrocket.py. Output paths unchanged."""
#!/usr/bin/env python3
"""build_shadowrocket.py — Shadowrocket RULE-SET / DOMAIN-SET lists."""

import sys
from pathlib import Path

import yaml

from src.adapters._common.paths import repo_root
ROOT = repo_root()
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
OUT = ROOT / "generated" / "shadowrocket"
LARGE = {"adblock", "china", "proxy", "gfw"}


def write_or_unlink(path: Path, lines: list[str]) -> None:
    if lines:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    elif path.exists():
        path.unlink()


def write_from_aggregates(sid: str) -> tuple[int, int]:
    rules_path = OUT / f"{sid}.list"
    domain_path = OUT / f"{sid}_domain.list"
    n_rules = n_dom = 0
    domain_buf: list[str] = []
    with rules_path.open("w", encoding="utf-8") as rf:
        dfile = DOMAINS / f"{sid}.txt"
        if dfile.exists():
            with dfile.open(encoding="utf-8") as f:
                for line in f:
                    d = line.strip()
                    if not d:
                        continue
                    rf.write(f"DOMAIN-SUFFIX,{d}\n")
                    domain_buf.append(f".{d}")
                    n_rules += 1
                    n_dom += 1
        ifile = IPS / f"{sid}.txt"
        if ifile.exists():
            with ifile.open(encoding="utf-8") as f:
                for line in f:
                    ip = line.strip()
                    if not ip:
                        continue
                    if ":" in ip:
                        rf.write(f"IP-CIDR6,{ip},no-resolve\n")
                    else:
                        rf.write(f"IP-CIDR,{ip},no-resolve\n")
                    n_rules += 1
    write_or_unlink(domain_path, domain_buf)
    return n_rules, n_dom


def write_from_service(doc: dict) -> tuple[int, int]:
    sid = doc["id"]
    lines: list[str] = []
    ds: list[str] = []
    for r in doc.get("rules") or []:
        t, v = r.get("type"), r.get("value")
        if not t or not v:
            continue
        if t == "domain":
            lines.append(f"DOMAIN,{v}")
            ds.append(v)
        elif t == "domain_suffix":
            lines.append(f"DOMAIN-SUFFIX,{v}")
            ds.append(f".{v}")
        elif t == "domain_keyword":
            lines.append(f"DOMAIN-KEYWORD,{v}")
        elif t == "ip_cidr":
            lines.append(f"IP-CIDR,{v},no-resolve")
        elif t == "ip_cidr6":
            lines.append(f"IP-CIDR6,{v},no-resolve")
    dfile = DOMAINS / f"{sid}.txt"
    seen = {x.lower().lstrip(".") for x in ds}
    if dfile.exists():
        for line in dfile.read_text(encoding="utf-8").splitlines():
            d = line.strip()
            if d and d.lower() not in seen:
                lines.append(f"DOMAIN-SUFFIX,{d}")
                ds.append(f".{d}")
                seen.add(d.lower())
    ifile = IPS / f"{sid}.txt"
    if ifile.exists():
        for line in ifile.read_text(encoding="utf-8").splitlines():
            ip = line.strip()
            if not ip:
                continue
            lines.append(f"IP-CIDR6,{ip},no-resolve" if ":" in ip else f"IP-CIDR,{ip},no-resolve")
    write_or_unlink(OUT / f"{sid}.list", lines)
    write_or_unlink(OUT / f"{sid}_domain.list", ds)
    return len(lines), len(ds)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        if sid in LARGE:
            n_r, n_d = write_from_aggregates(sid)
        else:
            n_r, n_d = write_from_service(doc)
        if n_r == 0 and n_d == 0:
            continue
        print(f"  shadowrocket {sid}: rules={n_r} domain_set={n_d}")
        count += 1
    for p in OUT.glob("*_domain.list"):
        if p.stat().st_size == 0:
            p.unlink()
            print(f"  removed stale empty {p.name}")
    print(f"[build_shadowrocket] wrote {count} → {OUT}")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
