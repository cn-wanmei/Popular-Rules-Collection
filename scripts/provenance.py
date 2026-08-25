#!/usr/bin/env python3
"""
provenance.py — compact, sharded rule-level lineage

Writes:
  database/provenance/sources.json
  database/provenance/services.json
  database/provenance/domains/{00..ff}.jsonl   (256 shards by sha256[:2])
  database/provenance/summary.json

No single file may approach GitHub's 100MB limit.
Schema per line (compact):
  {"d":"example.com","s":[0,1],"r":[3],"t":"domain_suffix"}
where s/r are indexes into sources.json / services.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
OUT = ROOT / "database" / "provenance"
SHARDS = OUT / "domains"


def shard_key(domain: str) -> str:
    return hashlib.sha256(domain.encode("utf-8")).hexdigest()[:2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    SHARDS.mkdir(parents=True, exist_ok=True)

    legacy = OUT / "domains.jsonl"
    if legacy.exists():
        legacy.unlink()
        print("[provenance] removed legacy domains.jsonl")

    source_ids: dict[str, int] = {}
    service_ids: dict[str, int] = {}

    def sid_src(name: str) -> int:
        if name not in source_ids:
            source_ids[name] = len(source_ids)
        return source_ids[name]

    def sid_svc(name: str) -> int:
        if name not in service_ids:
            service_ids[name] = len(service_ids)
        return service_ids[name]

    prov: dict[str, dict[str, Any]] = {}

    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        svc = doc.get("id") or path.stem
        r_idx = sid_svc(svc)
        sources = [
            s.get("id")
            for s in (doc.get("source") or [])
            if isinstance(s, dict) and s.get("id")
        ]
        s_idxs = [sid_src(x) for x in sources if x]
        for r in doc.get("rules") or []:
            val = (r.get("value") or "").strip().lower()
            if not val:
                continue
            entry = prov.setdefault(
                val, {"s": set(), "r": set(), "t": r.get("type") or "domain"}
            )
            entry["s"].update(s_idxs)
            entry["r"].add(r_idx)
            if r.get("type"):
                entry["t"] = r.get("type")

    for path in sorted(DOMAINS.glob("*.txt")):
        svc = path.stem
        r_idx = sid_svc(svc)
        svc_path = SERVICES / f"{svc}.yaml"
        sources: list[str] = []
        if svc_path.exists():
            doc = yaml.safe_load(svc_path.read_text(encoding="utf-8")) or {}
            sources = [
                s.get("id")
                for s in (doc.get("source") or [])
                if isinstance(s, dict) and s.get("id")
            ]
        s_idxs = [sid_src(x) for x in sources if x]
        with path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                val = line.strip().lower()
                if not val:
                    continue
                entry = prov.setdefault(
                    val, {"s": set(), "r": set(), "t": "domain_suffix"}
                )
                entry["s"].update(s_idxs)
                entry["r"].add(r_idx)

    for old in SHARDS.glob("*.jsonl"):
        old.unlink()

    buckets: dict[str, list[str]] = {f"{i:02x}": [] for i in range(256)}
    for domain, meta in prov.items():
        sk = shard_key(domain)
        obj = {
            "d": domain,
            "s": sorted(meta["s"]),
            "r": sorted(meta["r"]),
            "t": meta.get("t") or "domain_suffix",
        }
        buckets[sk].append(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))

    max_shard_bytes = 0
    written_shards = 0
    total_lines = 0
    for sk, lines in buckets.items():
        if not lines:
            continue
        body = "\n".join(lines) + "\n"
        p = SHARDS / f"{sk}.jsonl"
        p.write_text(body, encoding="utf-8")
        max_shard_bytes = max(max_shard_bytes, len(body.encode("utf-8")))
        written_shards += 1
        total_lines += len(lines)

    inv_src = {v: k for k, v in source_ids.items()}
    inv_svc = {v: k for k, v in service_ids.items()}
    (OUT / "sources.json").write_text(
        json.dumps({str(i): inv_src[i] for i in sorted(inv_src)}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    (OUT / "services.json").write_text(
        json.dumps({str(i): inv_svc[i] for i in sorted(inv_svc)}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )

    multi = sum(1 for m in prov.values() if len(m["s"]) > 1)
    summary = {
        "date": args.date,
        "domains": total_lines,
        "shards_written": written_shards,
        "max_shard_bytes": max_shard_bytes,
        "max_shard_mb": round(max_shard_bytes / (1024 * 1024), 3),
        "sources": len(source_ids),
        "services": len(service_ids),
        "multi_source_domains": multi,
        "schema": {
            "line": {"d": "domain", "s": "source indexes", "r": "service indexes", "t": "type"},
            "lookup": "sources.json / services.json",
        },
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"[provenance] domains={total_lines} shards={written_shards} "
        f"max_shard={summary['max_shard_mb']}MB multi_source={multi}"
    )
    if max_shard_bytes > 90 * 1024 * 1024:
        print("[provenance] ERROR: shard exceeds 90MB safety threshold")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
