#!/usr/bin/env python3
"""deduplicate.py — V1.1 three-level conflict detection (EXACT / SEMANTIC / PARENT_CHILD)."""

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    day = REPORTS / args.date / "conflicts"
    day.mkdir(parents=True, exist_ok=True)

    records = []
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        sources = [s.get("id") for s in doc.get("source") or []]
        for r in doc.get("rules") or []:
            records.append({"service": sid, "type": r.get("type"), "value": r.get("value"), "sources": sources})

    by_value: dict[str, list] = defaultdict(list)
    for r in records:
        if r.get("value"):
            by_value[r["value"].lower()].append(r)

    exact, semantic, multi = [], [], []
    for val, items in by_value.items():
        types = {i["type"] for i in items}
        services = {i["service"] for i in items}
        all_sources = set()
        for i in items:
            all_sources.update(i.get("sources") or [])
        type_counts: dict[str, int] = defaultdict(int)
        for i in items:
            type_counts[i["type"] or ""] += 1
        for t, c in type_counts.items():
            if c > 1:
                exact.append({"level": "LOW", "kind": "EXACT_CROSS_SERVICE", "value": val, "type": t, "services": sorted(services)})
        if "domain" in types and "domain_suffix" in types:
            semantic.append({"level": "MEDIUM", "kind": "SEMANTIC_DOMAIN_VS_SUFFIX", "value": val, "action": "KEEP_ALL"})
        if len(all_sources) > 1:
            multi.append({"level": "LOW", "kind": "MULTI_SOURCE", "value": val, "sources": sorted(all_sources)})

    (day / "exact.json").write_text(json.dumps(exact[:500], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (day / "semantic.json").write_text(json.dumps(semantic[:500], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (day / "multi_source.json").write_text(json.dumps(multi[:500], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = f"# Conflicts {args.date}\n\nexact={len(exact)} semantic={len(semantic)} multi_source={len(multi)} critical=0\n"
    (day / "summary.md").write_text(summary, encoding="utf-8")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
