#!/usr/bin/env python3
"""builder_validate.py — Rule Loss Ratio; FAIL if generated empty while DB non-empty."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LARGE = {"adblock", "china", "proxy", "gfw"}


def count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    return sum(1 for ln in p.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip())


def count_service_db(sid: str) -> int:
    return count_lines(ROOT / "database" / "domains" / f"{sid}.txt") + count_lines(
        ROOT / "database" / "ips" / f"{sid}.txt"
    )


def count_generated(client: str, sid: str) -> int:
    base = ROOT / "generated" / client
    candidates = [base / f"{sid}.list", base / f"{sid}.yaml", base / f"{sid}.json", base / f"{sid}_domain.list"]
    total = 0
    found = False
    for p in candidates:
        if p.exists() and p.stat().st_size > 0:
            found = True
            if p.suffix == "json":
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        for k in ("domain", "domain_suffix", "domain_keyword", "ip_cidr", "ip_cidr6"):
                            v = data.get(k)
                            if isinstance(v, list):
                                total += len(v)
                    elif isinstance(data, list):
                        total += len(data)
                except json.JSONDecodeError:
                    total += count_lines(p)
            elif p.suffix == ".yaml":
                text = p.read_text(encoding="utf-8", errors="replace")
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
    services = [p.stem for p in sorted((ROOT / "database" / "services").glob("*.yaml")) if not p.name.startswith("example")]
    clients = ["mihomo", "sing-box", "surge", "shadowrocket", "quantumult-x", "egern"]
    report = {"date": args.date, "failures": [], "warnings": [], "rows": []}
    fatal = False
    for sid in services:
        db_n = count_service_db(sid)
        row = {"service": sid, "database": db_n, "clients": {}}
        for c in clients:
            n = count_generated(c, sid)
            row["clients"][c] = n
            if db_n > 0 and n == 0:
                report["failures"].append(f"{sid}/{c}: database={db_n} generated=0")
                fatal = True
            elif db_n > 0 and n > 0 and sid not in LARGE:
                loss = max(0, db_n - n) / db_n
                if loss > 0.05:
                    report["warnings"].append(f"{sid}/{c}: loss_ratio={loss:.1%} db={db_n} out={n}")
        report["rows"].append(row)
    out = ROOT / "reports" / args.date
    out.mkdir(parents=True, exist_ok=True)
    (out / "builder-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[builder_validate] failures={len(report['failures'])} warnings={len(report['warnings'])}")
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
