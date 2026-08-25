#!/usr/bin/env python3
"""conflict_detector.py — reports only; CRITICAL = same match + different policy"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
REPORTS = ROOT / "reports"


def load_rules() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        policy = (doc.get("policy") or {}).get("default") or "proxy"
        sources = [s.get("id") for s in doc.get("source") or [] if isinstance(s, dict)]
        for r in doc.get("rules") or []:
            rows.append({
                "service": sid, "type": r.get("type"),
                "value": (r.get("value") or "").lower(),
                "policy": policy, "sources": sources,
            })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    day = REPORTS / args.date / "conflicts"
    day.mkdir(parents=True, exist_ok=True)
    rows = load_rules()
    by_match: dict[tuple[str, str], list] = defaultdict(list)
    for r in rows:
        if r["value"] and r["type"]:
            by_match[(r["type"], r["value"])].append(r)

    critical, high, medium, low = [], [], [], []
    for (typ, val), items in by_match.items():
        policies = {i["policy"] for i in items}
        services = sorted({i["service"] for i in items})
        all_src: set[str] = set()
        for i in items:
            all_src.update(i.get("sources") or [])
        if len(policies) > 1 and len(services) > 1:
            critical.append({
                "level": "CRITICAL", "kind": "POLICY_MISMATCH",
                "match": {"type": typ, "value": val},
                "policies": sorted(policies), "services": services,
                "sources": sorted(all_src),
            })
        elif len(all_src) > 1 and len(policies) == 1:
            low.append({
                "level": "LOW", "kind": "MULTI_SOURCE_DUPLICATE",
                "match": {"type": typ, "value": val},
                "policy": next(iter(policies)),
                "sources": sorted(all_src), "services": services,
            })
        types_here = {i["type"] for i in items}
        if "domain" in types_here and "domain_suffix" in types_here:
            medium.append({
                "level": "MEDIUM", "kind": "SEMANTIC_DOMAIN_VS_SUFFIX",
                "value": val, "services": services,
            })

    for i in rows:
        if i["type"] != "domain":
            continue
        parts = i["value"].split(".")
        for n in range(1, min(3, len(parts))):
            parent = ".".join(parts[n:])
            for j in rows:
                if j["type"] == "domain_suffix" and j["value"] == parent and j["policy"] != i["policy"]:
                    high.append({
                        "level": "HIGH", "kind": "PARENT_CHILD_POLICY",
                        "child": i["value"], "parent": parent,
                        "child_policy": i["policy"], "parent_policy": j["policy"],
                        "services": sorted({i["service"], j["service"]}),
                    })
                    break

    seen = set()
    high_u = []
    for h in high:
        k = (h["child"], h["parent"], h["child_policy"], h["parent_policy"])
        if k not in seen:
            seen.add(k)
            high_u.append(h)
    high = high_u[:500]

    for name, data in [("critical", critical), ("high", high), ("medium", medium), ("low", low)]:
        (day / f"{name}.json").write_text(json.dumps(data[:500], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {"date": args.date, "critical": len(critical), "high": len(high), "medium": len(medium), "low": len(low)}
    (day / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (day / "summary.md").write_text(
        f"# Conflicts {args.date}\n\n| Level | Count |\n|-------|------:|\n"
        f"| CRITICAL | {summary['critical']} |\n| HIGH | {summary['high']} |\n"
        f"| MEDIUM | {summary['medium']} |\n| LOW | {summary['low']} |\n",
        encoding="utf-8",
    )
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
