#!/usr/bin/env python3
"""provenance.py — rule-level lineage → database/provenance/domains.jsonl"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
OUT = ROOT / "database" / "provenance"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    prov: dict[str, dict[str, Any]] = {}

    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        sources = [s.get("id") for s in doc.get("source") or [] if isinstance(s, dict) and s.get("id")]
        for r in doc.get("rules") or []:
            val = (r.get("value") or "").lower()
            if not val:
                continue
            entry = prov.setdefault(val, {
                "rule": val, "type": r.get("type"), "sources": set(), "services": set(),
                "first_seen": args.date, "last_seen": args.date,
            })
            entry["sources"].update(sources)
            entry["services"].add(sid)
            entry["last_seen"] = args.date

    for path in DOMAINS.glob("*.txt"):
        sid = path.stem
        svc_path = SERVICES / f"{sid}.yaml"
        sources: list[str] = []
        if svc_path.exists():
            doc = yaml.safe_load(svc_path.read_text(encoding="utf-8")) or {}
            sources = [s.get("id") for s in doc.get("source") or [] if isinstance(s, dict) and s.get("id")]
        with path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                val = line.strip().lower()
                if not val:
                    continue
                entry = prov.setdefault(val, {
                    "rule": val, "type": "domain_suffix", "sources": set(), "services": set(),
                    "first_seen": args.date, "last_seen": args.date,
                })
                entry["sources"].update(sources)
                entry["services"].add(sid)
                entry["last_seen"] = args.date

    out_path = OUT / "domains.jsonl"
    count = multi = 0
    with out_path.open("w", encoding="utf-8") as out:
        for val in sorted(prov.keys()):
            e = prov[val]
            srcs = sorted(e["sources"])
            rec = {
                "rule": e["rule"], "type": e.get("type"), "sources": srcs,
                "services": sorted(e["services"]),
                "first_seen": e["first_seen"], "last_seen": e["last_seen"],
                "confidence": "high" if len(srcs) >= 2 else "medium",
            }
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            count += 1
            if len(srcs) >= 2:
                multi += 1

    summary = {"date": args.date, "rules_tracked": count, "multi_source_rules": multi,
               "path": str(out_path.relative_to(ROOT))}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
