#!/usr/bin/env python3
"""Statistics 2.0 — coverage / ecosystem / intentional-unmaterialized metrics.

Emits reports/YYYY-MM-DD/statistics.json (+ summary.json alias).
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# Registered but intentionally not materialized (documented reasons)
INTENTIONAL_UNMATERIALIZED = {
    "adblock-light": "no_database_yaml (hagezi profile deferred)",
    "adblock-pro": "no_database_yaml (hagezi profile deferred)",
    "blizzard": "no separate upstream (BM Blizzard → battlenet)",
    "stripe": "keyword-only / empty domain set",
}

CLIENTS = ("mihomo", "sing-box", "surge", "shadowrocket", "quantumult-x", "egern", "loon")


def count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    n = 0
    with p.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                n += 1
    return n


def load_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def primary_map() -> dict[str, dict]:
    prim = load_yaml(ROOT / "config" / "service_primary.yaml")
    services = dict(prim.get("services") or {})
    extra = load_yaml(ROOT / "config" / "service_primary_extra.yaml")
    services.update(extra.get("services") or {})
    for sid, ov in (extra.get("aggregate_overrides") or {}).items():
        base = dict(services.get(sid) or {})
        base.update(ov)
        services[sid] = base
    return {str(k): (v if isinstance(v, dict) else {}) for k, v in services.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    day = ROOT / "reports" / args.date
    day.mkdir(parents=True, exist_ok=True)

    P = primary_map()
    registered = set(P.keys())
    db_dir = ROOT / "database" / "services"
    materialized = {
        p.stem
        for p in db_dir.glob("*.yaml")
        if not p.name.startswith("example")
    } if db_dir.is_dir() else set()

    intentional = {
        sid: reason
        for sid, reason in INTENTIONAL_UNMATERIALIZED.items()
        if sid in registered and sid not in materialized
    }
    unexpected_missing = sorted(
        (registered - materialized) - set(intentional.keys())
    )
    reg_n = len(registered)
    mat_n = len(materialized & registered)
    cov = (mat_n / reg_n) if reg_n else 0.0

    ecosystem: dict[str, dict] = {}
    for sid, meta in P.items():
        eco = str(meta.get("primary_category") or "other")
        slot = ecosystem.setdefault(eco, {"registered": 0, "materialized": 0, "ids": []})
        slot["registered"] += 1
        slot["ids"].append(sid)
        if sid in materialized:
            slot["materialized"] += 1
    for eco, slot in ecosystem.items():
        slot["ids"] = sorted(slot["ids"])
        r, m = slot["registered"], slot["materialized"]
        slot["coverage"] = round(m / r, 4) if r else 0.0

    domains = sum(count_lines(p) for p in (ROOT / "database" / "domains").glob("*.txt"))
    cidr = sum(count_lines(p) for p in (ROOT / "database" / "ips").glob("*.txt"))

    builder_coverage: dict[str, dict] = {}
    for client in CLIENTS:
        d = ROOT / "generated" / client
        files = list(d.iterdir()) if d.is_dir() else []
        n = sum(1 for f in files if f.is_file())
        builder_coverage[client] = {
            "files": n,
            "status": "ok" if n > 0 else "missing",
        }

    reg = load_yaml(ROOT / "sources" / "registry.yaml")
    sources_on = sum(1 for s in reg.get("sources") or [] if s.get("enabled"))
    health = load_yaml(ROOT / "sources" / "health.yaml")
    source_health = {
        k: (v or {}).get("status")
        for k, v in (health.get("sources") or {}).items()
    }
    healthy = sum(1 for s in source_health.values() if s == "healthy")
    health_ratio = (healthy / len(source_health)) if source_health else None

    conflicts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    cpath = day / "conflicts" / "summary.json"
    if cpath.exists():
        conflicts.update(json.loads(cpath.read_text(encoding="utf-8")))

    validation = {
        "schema_validate": "unknown",
        "builder_validate": "unknown",
        "validate": "unknown",
    }
    bv = day / "builder-validation.json"
    if bv.exists():
        try:
            rep = json.loads(bv.read_text(encoding="utf-8"))
            validation["builder_validate"] = (
                "pass" if not rep.get("failures") else "fail"
            )
            validation["builder_failures"] = len(rep.get("failures") or [])
        except Exception:
            pass

    stats = {
        "date": args.date,
        "version": 2,
        "service_coverage": {
            "registered": reg_n,
            "materialized": mat_n,
            "intentional_unmaterialized": len(intentional),
            "unexpected_missing": unexpected_missing,
            "coverage": round(cov, 4),
        },
        "intentional_unmaterialized": intentional,
        "rule_coverage": {
            "domains": domains,
            "ips": cidr,
            "database_services": len(materialized),
        },
        "source_health": {
            "enabled_sources": sources_on,
            "statuses": source_health,
            "healthy_ratio": health_ratio,
        },
        "builder_coverage": builder_coverage,
        "ecosystem_coverage": dict(sorted(ecosystem.items())),
        "validation": validation,
        "conflicts": {
            "critical": conflicts.get("critical", 0),
            "high": conflicts.get("high", 0),
            "medium": conflicts.get("medium", 0),
            "low": conflicts.get("low", 0),
        },
        "sources": sources_on,
        "services": mat_n,
        "domains": domains,
        "cidr": cidr,
        "build": {c: v["status"] for c, v in builder_coverage.items()},
    }

    (day / "statistics.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (day / "summary.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    sc = stats["service_coverage"]
    print(
        f"[statistics] registered={sc['registered']} materialized={sc['materialized']} "
        f"intentional={sc['intentional_unmaterialized']} coverage={sc['coverage']} "
        f"domains={domains} ips={cidr}"
    )
    if unexpected_missing:
        print(f"  WARN unexpected_missing={unexpected_missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
