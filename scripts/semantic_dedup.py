#!/usr/bin/env python3
"""P1.1 Semantic dedup report (exact vs suffix). Report-only."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
OUT = ROOT / "reports" / "semantic_dedup.json"


def main() -> int:
    exact: dict[str, set[str]] = defaultdict(set)
    suffix: dict[str, set[str]] = defaultdict(set)
    for p in SERVICES.glob("*.yaml"):
        if p.name.startswith("example"):
            continue
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        sid = doc.get("id") or p.stem
        for r in doc.get("rules") or []:
            if not isinstance(r, dict):
                continue
            t, v = r.get("type"), (r.get("value") or "").lower().strip()
            if not t or not v:
                continue
            if t == "domain":
                exact[v].add(sid)
            elif t == "domain_suffix":
                suffix[v].add(sid)
    contained = []
    for host, svcs in exact.items():
        if host in suffix:
            contained.append({
                "kind": "EXACT_ALSO_SUFFIX",
                "value": host,
                "exact_services": sorted(svcs),
                "suffix_services": sorted(suffix[host]),
            })
    report = {
        "exact_hosts": len(exact),
        "suffix_hosts": len(suffix),
        "exact_also_suffix": len(contained),
        "samples": contained[:500],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[semantic_dedup] exact={len(exact)} suffix={len(suffix)} exact_also_suffix={len(contained)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
