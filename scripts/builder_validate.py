#!/usr/bin/env python3
"""builder_validate.py — Client output completeness vs Canonical DB (loss ratio).

Does NOT check empty domain-set semantics (that is validate.py).
Focus: for each service with DB rules, each client should emit non-empty main output.

sing-box JSON is headless rule-set:
  {"version": 2, "rules": [{"domain_suffix": [...], ...}]}
Count must walk nested rules[], not only top-level keys.
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

JSON_RULE_KEYS = (
    "domain",
    "domain_suffix",
    "domain_keyword",
    "domain_regex",
    "ip_cidr",
    "ip_cidr6",
)


def count_lines(p: Path) -> int:
    if not p.exists() or p.stat().st_size == 0:
        return 0
    n = 0
    with p.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                n += 1
    return n


def count_json_rules(data: object) -> int:
    """Count rule items in sing-box (nested or flat) JSON."""
    total = 0
    if isinstance(data, list):
        return len(data)
    if not isinstance(data, dict):
        return 0
    for k in JSON_RULE_KEYS:
        v = data.get(k)
        if isinstance(v, list):
            total += len(v)
    for rule in data.get("rules") or []:
        if isinstance(rule, dict):
            for k in JSON_RULE_KEYS:
                v = rule.get(k)
                if isinstance(v, list):
                    total += len(v)
        elif isinstance(rule, str):
            total += 1
    return total


def count_db(sid: str) -> int:
    """Canonical count: domains.txt + ips.txt, else yaml rules length."""
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
            # payload list or egern domain_suffix_set lines
            total += sum(1 for ln in text.splitlines() if ln.strip().startswith("- "))
            if total == 0:
                total += count_lines(p)
        else:
            total += count_lines(p)
    return total if found else -1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    services = [
        p.stem
        for p in sorted(SERVICES.glob("*.yaml"))
        if not p.name.startswith("example")
    ]
    report = {"date": args.date, "failures": [], "warnings": [], "rows": []}
    fatal = False
    for sid in services:
        db_n = count_db(sid)
        row = {"service": sid, "database": db_n, "clients": {}}
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
