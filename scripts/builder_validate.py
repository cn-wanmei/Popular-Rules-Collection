#!/usr/bin/env python3
"""builder_validate.py — Client output completeness vs database (loss ratio).

Does NOT check empty domain-set semantics (that is validate.py).
Focus: for each service with DB rules, each client should emit non-empty main output.

count_db prefers domains/ips text files; falls back to services yaml rules.
count_json_rules understands sing-box nested {"version":2,"rules":[{...}]} and top-level.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
GENERATED = ROOT / "generated"
LARGE = {"adblock", "china", "proxy", "gfw", "adblock-pro", "adblock-light"}

CLIENTS = {
    "mihomo": ["{id}.yaml"],
    "sing-box": ["{id}.json"],
    "surge": ["{id}.list"],
    "shadowrocket": ["{id}.list"],
    "quantumult-x": ["{id}.list"],
    "egern": ["{id}.yaml"],
    "loon": ["{id}.list"],
}


def count_lines(p: Path) -> int:
    if not p.exists() or p.stat().st_size == 0:
        return 0
    n = 0
    with p.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                n += 1
    return n


def count_db(sid: str) -> int:
    """Prefer domains/ips aggregates; fallback to yaml rules count."""
    n = 0
    d, i = DOMAINS / f"{sid}.txt", IPS / f"{sid}.txt"
    if d.exists():
        n += count_lines(d)
    if i.exists():
        n += count_lines(i)
    if n:
        return n
    sp = SERVICES / f"{sid}.yaml"
    if not sp.exists():
        return 0
    try:
        doc = yaml.safe_load(sp.read_text(encoding="utf-8")) or {}
    except Exception:
        return 0
    return len(doc.get("rules") or [])


def count_json_rules(data: object) -> int:
    """Count rules in sing-box JSON (nested rules[] or top-level keys)."""
    total = 0
    if isinstance(data, list):
        for item in data:
            total += count_json_rules(item)
        return total
    if not isinstance(data, dict):
        return 0
    # Nested: {"version": 2, "rules": [{domain: [...], ...}]}
    rules = data.get("rules")
    if isinstance(rules, list):
        for item in rules:
            if isinstance(item, dict):
                for k in (
                    "domain",
                    "domain_suffix",
                    "domain_keyword",
                    "domain_regex",
                    "ip_cidr",
                    "ip_cidr6",
                ):
                    v = item.get(k)
                    if isinstance(v, list):
                        total += len(v)
            elif isinstance(item, str):
                total += 1
        if total:
            return total
    # Top-level fallback
    for k in (
        "domain",
        "domain_suffix",
        "domain_keyword",
        "domain_regex",
        "ip_cidr",
        "ip_cidr6",
    ):
        v = data.get(k)
        if isinstance(v, list):
            total += len(v)
    return total


def count_client(client: str, sid: str) -> int:
    total = 0
    found = False
    for pat in CLIENTS.get(client, []):
        p = GENERATED / client / pat.format(id=sid)
        if not p.exists():
            continue
        found = True
        if p.suffix == ".json":
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                total += count_json_rules(data)
            except json.JSONDecodeError:
                total += count_lines(p)
        elif p.suffix == ".yaml":
            text = p.read_text(encoding="utf-8", errors="replace")
            # Mihomo: count payload list items (lines starting with "- ")
            n_payload = sum(
                1 for ln in text.splitlines() if ln.strip().startswith("- ")
            )
            if n_payload:
                total += n_payload
            else:
                total += count_lines(p)
        else:
            total += count_lines(p)
    return total if found else -1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    args = parser.parse_args()
    services = [
        p.stem
        for p in sorted(SERVICES.glob("*.yaml"))
        if not p.name.startswith("example")
    ]
    report: dict = {"date": args.date, "failures": [], "warnings": [], "rows": []}
    fatal = False
    for sid in services:
        db_n = count_db(sid)
        row: dict = {"service": sid, "database": db_n, "clients": {}}
        for c in CLIENTS:
            n = count_client(c, sid)
            row["clients"][c] = n
            if db_n > 0 and n == 0:
                report["failures"].append(f"{sid}/{c}: database={db_n} generated=0")
                fatal = True
            elif db_n > 0 and n == -1:
                report["failures"].append(f"{sid}/{c}: missing generated file")
                fatal = True
            elif db_n > 0 and n > 0 and sid not in LARGE:
                loss = max(0, db_n - n) / db_n
                if loss > 0.05:
                    report["warnings"].append(
                        f"{sid}/{c}: loss_ratio={loss:.1%} db={db_n} out={n}"
                    )
        report["rows"].append(row)
    out = ROOT / "reports" / args.date
    out.mkdir(parents=True, exist_ok=True)
    (out / "builder-validation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"[builder_validate] failures={len(report['failures'])} "
        f"warnings={len(report['warnings'])}"
    )
    for f in report["failures"][:30]:
        print("  FAIL", f)
    for w in report["warnings"][:20]:
        print("  WARN", w)
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
