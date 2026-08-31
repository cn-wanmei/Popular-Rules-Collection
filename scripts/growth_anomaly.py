#!/usr/bin/env python3
"""V2.2 Growth anomaly — lines + bytes + ratio."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
SNAP = ROOT / "reports" / "growth_snapshot.json"
OUT = ROOT / "reports" / "growth_anomaly.json"


def counts():
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
        bytes_ = p.stat().st_size
        if n == 0:
            d = ROOT / "database" / "domains" / f"{sid}.txt"
            if d.exists():
                n = sum(1 for ln in d.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip())
                bytes_ += d.stat().st_size
        out[sid] = {"lines": n, "bytes": bytes_}
    return out


def main() -> int:
    cur = counts()
    prev = {}
    if SNAP.exists():
        try:
            raw = json.loads(SNAP.read_text())
            prev = raw.get("counts") or {}
            if prev and not isinstance(next(iter(prev.values()), {}), dict):
                prev = {k: {"lines": v, "bytes": 0} for k, v in prev.items()}
        except Exception:
            prev = {}
    hard, warn = [], []
    for sid, now in cur.items():
        o = prev.get(sid)
        if not o:
            continue
        ol, nl = int(o.get("lines") or 0), int(now.get("lines") or 0)
        ob, nb = int(o.get("bytes") or 0), int(now.get("bytes") or 0)
        if ol >= 50 and nl < ol * 0.5:
            hard.append({"service": sid, "kind": "shrink_lines", "was": ol, "now": nl})
        elif ol >= 20 and nl >= ol * 5:
            hard.append({"service": sid, "kind": "grow_lines_ratio", "was": ol, "now": nl})
        elif ob >= 100_000 and nb < ob * 0.5:
            hard.append({"service": sid, "kind": "shrink_bytes", "was": ob, "now": nb})
        elif ol >= 50 and abs(nl - ol) / ol >= 0.3:
            warn.append({"service": sid, "kind": "delta_lines", "was": ol, "now": nl})
    report = {"hard": hard, "warn": warn[:100], "services": len(cur), "metrics": ["lines", "bytes", "ratio"]}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    SNAP.write_text(json.dumps({"counts": cur}, indent=2) + "\n", encoding="utf-8")
    print(f"[growth_anomaly] hard={len(hard)} warn={len(warn)} services={len(cur)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
