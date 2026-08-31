#!/usr/bin/env python3
"""P1.1 Growth anomaly vs previous snapshot."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
SNAP = ROOT / "reports" / "growth_snapshot.json"
OUT = ROOT / "reports" / "growth_anomaly.json"
HARD_SHRINK = 0.50
HARD_GROW = 5.0


def counts() -> dict[str, int]:
    out = {}
    for p in SERVICES.glob("*.yaml"):
        if p.name.startswith("example"):
            continue
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        sid = doc.get("id") or p.stem
        n = len(doc.get("rules") or [])
        if n == 0:
            d = ROOT / "database" / "domains" / f"{sid}.txt"
            if d.exists():
                n = sum(1 for ln in d.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip())
        out[sid] = n
    return out


def main() -> int:
    cur = counts()
    prev = {}
    if SNAP.exists():
        try:
            prev = json.loads(SNAP.read_text()).get("counts") or {}
        except Exception:
            prev = {}
    hard, warn = [], []
    for sid, n in cur.items():
        o = prev.get(sid)
        if o is None or o == 0:
            continue
        ratio = n / o if o else 999
        if n < o * (1 - HARD_SHRINK) and o >= 50:
            hard.append({"service": sid, "was": o, "now": n, "kind": "shrink"})
        elif ratio >= HARD_GROW and o >= 20:
            hard.append({"service": sid, "was": o, "now": n, "kind": "grow"})
        elif abs(n - o) / o >= 0.30 and o >= 50:
            warn.append({"service": sid, "was": o, "now": n})
    report = {"hard": hard, "warn": warn[:100], "services": len(cur)}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    SNAP.write_text(json.dumps({"counts": cur}, indent=2) + "\n", encoding="utf-8")
    print(f"[growth_anomaly] hard={len(hard)} warn={len(warn)} services={len(cur)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
