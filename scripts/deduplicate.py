#!/usr/bin/env python3
"""deduplicate.py — canonical domain/ip sets (mutates database/canonical + domains/ips)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from registry_map import source_priority  # noqa: E402

DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
SERVICES = ROOT / "database" / "services"
CANON = ROOT / "database" / "canonical"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    CANON.mkdir(parents=True, exist_ok=True)
    (CANON / "domains").mkdir(exist_ok=True)
    (CANON / "ips").mkdir(exist_ok=True)
    prio = source_priority()
    stats = {"services": 0, "domains_in": 0, "domains_out": 0, "ips_in": 0, "ips_out": 0}

    for path in sorted(DOMAINS.glob("*.txt")):
        sid = path.stem
        lines = [ln.strip() for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
        stats["domains_in"] += len(lines)
        seen: dict[str, str] = {}
        for ln in lines:
            k = ln.lower()
            if k not in seen or len(ln) < len(seen[k]):
                seen[k] = ln
        out_lines = sorted(seen.values(), key=str.lower)
        stats["domains_out"] += len(out_lines)
        text = "\n".join(out_lines) + ("\n" if out_lines else "")
        (CANON / "domains" / f"{sid}.txt").write_text(text, encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        stats["services"] += 1

    for path in sorted(IPS.glob("*.txt")):
        lines = [ln.strip() for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
        stats["ips_in"] += len(lines)
        seen = sorted(set(lines))
        stats["ips_out"] += len(seen)
        text = "\n".join(seen) + ("\n" if seen else "")
        (CANON / "ips" / path.name).write_text(text, encoding="utf-8")
        path.write_text(text, encoding="utf-8")

    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        srcs = doc.get("source") or []
        if isinstance(srcs, list) and srcs:
            for s in srcs:
                if isinstance(s, dict) and "priority" not in s:
                    s["priority"] = prio.get(s.get("id", ""), 50)
            srcs.sort(key=lambda x: -int((x or {}).get("priority") or 50))
            doc["source"] = srcs
            doc["canonical_source"] = srcs[0].get("id") if isinstance(srcs[0], dict) else None
            path.write_text(
                yaml.dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False),
                encoding="utf-8",
            )

    meta = {
        "date": args.date,
        **stats,
        "domain_removed": stats["domains_in"] - stats["domains_out"],
        "ip_removed": stats["ips_in"] - stats["ips_out"],
    }
    (CANON / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
