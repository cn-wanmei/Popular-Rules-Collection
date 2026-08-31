#!/usr/bin/env python3
"""V2.7 coverage / overlap / ownership reports."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SM = ROOT / "config" / "service_model"
OUT = ROOT / "reports" / "hierarchy"


def load(name):
    p = SM / name
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


def main() -> int:
    services = load("services.yaml").get("services") or {}
    providers = load("providers.yaml").get("providers") or {}
    aggregates = load("memberships.yaml").get("aggregates") or {}
    relations = load("relations.yaml") or {}
    by_prov = defaultdict(list)
    for sid, s in services.items():
        by_prov[(s or {}).get("provider")].append(sid)
    coverage = []
    for pid in sorted(providers.keys()):
        svcs = by_prov.get(pid) or []
        coverage.append({
            "provider": pid,
            "services_declared": len(svcs),
            "materialized": sum(1 for s in svcs if (services[s].get("materialization") or {}).get("state") == "materialized"),
            "candidate": sum(1 for s in svcs if (services[s].get("materialization") or {}).get("state") == "candidate"),
            "aggregate_members": len((aggregates.get(pid) or {}).get("members") or []),
        })
    def keys(sid):
        p = ROOT / "database" / "services" / f"{sid}.yaml"
        if not p.exists():
            return set()
        doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return {f"{r['type']}|{str(r['value']).strip().lower()}" for r in doc.get("rules") or [] if isinstance(r, dict) and r.get("type") and r.get("value")}
    major = [p for p in providers if (ROOT / "database" / "services" / f"{p}.yaml").exists()]
    key_owners = defaultdict(set)
    for p in major:
        for k in keys(p):
            key_owners[k].add(p)
    multi = {k: sorted(v) for k, v in key_owners.items() if len(v) > 1}
    report = {
        "coverage": coverage,
        "overlap": {"cross_provider_shared_keys": len(multi), "sample": dict(list(multi.items())[:30])},
        "ownership_entries": len(relations.get("ownership") or {}),
        "dependency_entries": len(relations.get("dependencies") or {}),
        "attribution_policy": relations.get("attribution_policy"),
        "shared_infrastructure": [sid for sid, s in services.items() if (s or {}).get("scope") == "shared_infrastructure"],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "coverage_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[hierarchy_coverage] providers={len(coverage)} cross_overlap={len(multi)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
