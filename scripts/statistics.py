#!/usr/bin/env python3
"""Emit reports/YYYY-MM-DD/summary.json + statistics.json"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    n = 0
    with p.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    day = ROOT / "reports" / args.date
    day.mkdir(parents=True, exist_ok=True)

    reg = yaml.safe_load((ROOT / "sources" / "registry.yaml").read_text(encoding="utf-8")) or {}
    sources_on = sum(1 for s in reg.get("sources") or [] if s.get("enabled"))

    domains = sum(count_lines(p) for p in (ROOT / "database" / "domains").glob("*.txt"))
    cidr = sum(count_lines(p) for p in (ROOT / "database" / "ips").glob("*.txt"))
    services = len(list((ROOT / "database" / "services").glob("*.yaml")))

    conflicts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    cpath = day / "conflicts" / "summary.json"
    if cpath.exists():
        conflicts.update(json.loads(cpath.read_text(encoding="utf-8")))

    build = {}
    for client in ("mihomo", "sing-box", "surge", "shadowrocket", "quantumult-x", "egern"):
        d = ROOT / "generated" / client
        build[client] = "success" if d.exists() and any(d.iterdir()) else "missing"

    health = {}
    hp = ROOT / "sources" / "health.yaml"
    if hp.exists():
        health = yaml.safe_load(hp.read_text(encoding="utf-8")) or {}

    stats = {
        "date": args.date,
        "sources": sources_on,
        "services": services,
        "domains": domains,
        "cidr": cidr,
        "conflicts": {
            "critical": conflicts.get("critical", 0),
            "high": conflicts.get("high", 0),
            "medium": conflicts.get("medium", 0),
            "low": conflicts.get("low", 0),
        },
        "build": build,
        "source_health": {
            k: (v or {}).get("status")
            for k, v in (health.get("sources") or {}).items()
        },
    }
    (day / "statistics.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    (day / "summary.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
