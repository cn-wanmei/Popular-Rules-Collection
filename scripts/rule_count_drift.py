#!/usr/bin/env python3
"""rule_count_drift.py — P1-2 per-service rule count delta (warn-first).

Writes reports/<date>/rule_counts.json and compares to previous baseline.
Thresholds: warn 20%, high 50%, review 80%. Exit 0 unless --strict.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
REPORTS = ROOT / "reports"

VOLATILE = frozenset({"adblock", "adblock-light", "adblock-pro", "china", "proxy", "gfw"})


def count_service(sid: str, doc: dict) -> int:
    stats = (doc.get("metadata") or {}).get("stats") or {}
    if isinstance(stats.get("total"), int) and stats["total"] > 0:
        return int(stats["total"])
    n = 0
    for r in doc.get("rules") or []:
        if isinstance(r, dict) and r.get("value"):
            n += 1
    dp = DOMAINS / f"{sid}.txt"
    if dp.exists():
        n = max(
            n,
            sum(
                1
                for line in dp.read_text(encoding="utf-8", errors="replace").splitlines()
                if line.strip()
            ),
        )
    ip = IPS / f"{sid}.txt"
    if ip.exists():
        n += sum(
            1
            for line in ip.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip()
        )
    return n


def load_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    if not SERVICES.is_dir():
        return out
    for p in SERVICES.glob("*.yaml"):
        if p.name.startswith("example"):
            continue
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        sid = str(doc.get("id") or p.stem)
        out[sid] = count_service(sid, doc if isinstance(doc, dict) else {})
    return out


def prev_baseline(date: str) -> dict[str, int] | None:
    try:
        dt = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return None
    for i in range(1, 14):
        d = (dt - timedelta(days=i)).isoformat()
        p = REPORTS / d / "rule_counts.json"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                return {k: int(v) for k, v in (data.get("counts") or {}).items()}
            except Exception:
                continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--warn-pct", type=float, default=20.0)
    ap.add_argument("--high-pct", type=float, default=50.0)
    ap.add_argument("--review-pct", type=float, default=80.0)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    counts = load_counts()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)
    payload = {
        "date": args.date,
        "counts": counts,
        "service_count": len(counts),
        "total_rules": sum(counts.values()),
    }
    (day / "rule_counts.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    baseline = prev_baseline(args.date)
    warnings: list[str] = []
    highs: list[str] = []
    reviews: list[str] = []

    if not baseline:
        print(f"[rule_count_drift] wrote {day / 'rule_counts.json'} (no baseline yet)")
        return 0

    for sid, n in sorted(counts.items()):
        old = baseline.get(sid)
        if old is None or old <= 0:
            continue
        delta = (n - old) / old * 100.0
        ad = abs(delta)
        thr_w, thr_h, thr_r = args.warn_pct, args.high_pct, args.review_pct
        if sid in VOLATILE:
            thr_w, thr_h = thr_h, thr_r
        msg = f"{sid}: {old} → {n} ({delta:+.1f}%)"
        if ad >= thr_r:
            reviews.append(msg)
        elif ad >= thr_h:
            highs.append(msg)
        elif ad >= thr_w:
            warnings.append(msg)

    print(
        f"[rule_count_drift] services={len(counts)} "
        f"warn={len(warnings)} high={len(highs)} review={len(reviews)}"
    )
    for m in warnings[:25]:
        print(f"  WARN   {m}")
    for m in highs[:25]:
        print(f"  HIGH   {m}")
    for m in reviews[:25]:
        print(f"  REVIEW {m}")

    report = {
        "date": args.date,
        "baseline_compared": True,
        "warn": warnings,
        "high": highs,
        "review": reviews,
    }
    (day / "rule_count_drift.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if args.strict and (highs or reviews):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
