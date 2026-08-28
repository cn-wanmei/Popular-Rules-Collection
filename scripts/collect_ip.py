#!/usr/bin/env python3
"""collect_ip.py — Phase 2B-IP P0: fetch IP sources → database/ips/{maps_to}.txt

Respects sources/ip_registry.yaml scopes. Merges with existing sidecar lines,
runs CIDR normalize + containment dedup.
Does NOT invent service IPs from provider ranges.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fetchers import get_fetcher  # noqa: E402
from ip_cidr import merge_files  # noqa: E402

REG = ROOT / "sources" / "ip_registry.yaml"
IPS = ROOT / "database" / "ips"
BACKUP = ROOT / "backup"


def main() -> int:
    cfg = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    sources = [s for s in (cfg.get("sources") or []) if s.get("enabled")]
    if not sources:
        print("[collect_ip] no enabled sources")
        return 0

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    bak = BACKUP / day / "ip_sources"
    bak.mkdir(parents=True, exist_ok=True)
    IPS.mkdir(parents=True, exist_ok=True)

    by_target: dict[str, list[str]] = defaultdict(list)
    ok, fail = 0, 0

    for src in sources:
        sid = src.get("id", "?")
        scope = src.get("scope", "unknown")
        target = src.get("maps_to")
        if not target:
            print(f"  SKIP {sid}: missing maps_to")
            fail += 1
            continue
        if scope == "provider":
            print(f"  SKIP {sid}: provider scope must not map into product services")
            fail += 1
            continue

        fetch = src.get("fetch") or {}
        path = src.get("path")
        local = src.get("local") or f"{sid}.txt"
        if not path or not fetch.get("type"):
            print(f"  SKIP {sid}: incomplete fetch/path")
            fail += 1
            continue

        fetcher = get_fetcher(fetch)
        fr = fetcher.fetch_one({"path": path, "name": sid, "local": local})
        if not fr.ok or not fr.content:
            print(f"  FAIL {sid}: {fr.error}")
            fail += 1
            continue

        text = fr.content.decode("utf-8", errors="replace")
        (bak / local).write_text(text, encoding="utf-8")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        by_target[str(target)].extend(lines)
        ok += 1
        print(f"  OK {sid} scope={scope} → {target} lines={len(lines)}")

    written = 0
    for target, incoming in sorted(by_target.items()):
        dest = IPS / f"{target}.txt"
        existing: list[str] = []
        if dest.exists():
            existing = dest.read_text(encoding="utf-8", errors="replace").splitlines()
        merged = merge_files(existing, incoming, contain=True)
        dest.write_text("\n".join(merged) + ("\n" if merged else ""), encoding="utf-8")
        written += 1
        print(
            f"  WRITE database/ips/{target}.txt  "
            f"in={len(existing)}+{len(incoming)} out={len(merged)}"
        )

    print(f"[collect_ip] sources_ok={ok} failed={fail} targets={written}")
    return 0 if fail == 0 or written > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
