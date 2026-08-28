#!/usr/bin/env python3
"""collect_providers.py — Phase 3C provider CIDRs (Provider ≠ Service)."""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ip_cidr import normalize_lines  # noqa: E402

REG = ROOT / "sources" / "datasets" / "provider.yaml"
OUT = ROOT / "database" / "provider"
PROV = ROOT / "database" / "datasets_provenance"
REPORTS = ROOT / "reports"


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Popular-Rules-Collection/3C"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def parse_aws_json(data: bytes) -> list[str]:
    doc = json.loads(data.decode("utf-8"))
    prefixes = []
    for p in doc.get("prefixes") or []:
        cidr = p.get("ip_prefix")
        if cidr:
            prefixes.append(cidr)
    for p in doc.get("ipv6_prefixes") or []:
        cidr = p.get("ipv6_prefix")
        if cidr:
            prefixes.append(cidr)
    return prefixes


def main() -> int:
    if not REG.exists():
        print("[collect_providers] no provider.yaml")
        return 0
    cfg = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    now = datetime.now(timezone.utc)
    day = now.strftime("%Y-%m-%d")
    OUT.mkdir(parents=True, exist_ok=True)
    PROV.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    results = {}

    for ds in cfg.get("datasets") or []:
        if not ds.get("enabled"):
            continue
        did = ds.get("id", "?")
        path = ds.get("path")
        fetch = ds.get("fetch") or {}
        url = fetch.get("url")
        if not url or not path:
            print(f"  SKIP {did}: need url+path")
            fail += 1
            continue
        if str(path).startswith("database/ips/"):
            print(f"  HARD skip {did}: provider must not write database/ips/")
            fail += 1
            continue
        try:
            raw = http_get(url)
        except Exception as e:
            print(f"  FAIL {did}: {e}")
            fail += 1
            continue

        fmt = ds.get("format") or "text"
        if fmt == "aws_json":
            lines = parse_aws_json(raw)
        else:
            lines = [
                ln.strip()
                for ln in raw.decode("utf-8", errors="replace").splitlines()
                if ln.strip() and not ln.strip().startswith("#")
            ]
        merged = normalize_lines(lines)
        dest = ROOT / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("\n".join(merged) + ("\n" if merged else ""), encoding="utf-8")
        meta = {
            "id": did,
            "scope": "provider",
            "path": path,
            "lines": len(merged),
            "fetched_at": now.isoformat(),
            "source_url": url,
            "notes": ds.get("notes") or "Provider ≠ Service",
        }
        (PROV / f"{did}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        results[did] = meta
        ok += 1
        print(f"  OK {did} lines={len(merged)} → {path}")

    rep = REPORTS / day
    rep.mkdir(parents=True, exist_ok=True)
    (rep / "provider_collect.json").write_text(
        json.dumps({"date": day, "ok": ok, "failed": fail, "results": results}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(f"[collect_providers] ok={ok} failed={fail}")
    return 0 if fail == 0 or ok > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
