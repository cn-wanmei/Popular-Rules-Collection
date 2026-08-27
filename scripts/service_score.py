#!/usr/bin/env python3
"""service_score.py — Phase 3D scaffold: lightweight per-service score (soft)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
REPORTS = ROOT / "reports"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)

    drift = {}
    dp = day / "rule_count_drift.json"
    if dp.exists():
        try:
            d = json.loads(dp.read_text(encoding="utf-8"))
            for key in ("warn", "high", "review"):
                for msg in d.get(key) or []:
                    sid = msg.split(":")[0].strip()
                    drift[sid] = key
        except Exception:
            pass

    identity_warn = set()
    ip = day / "identity_report.json"
    if ip.exists():
        try:
            for w in json.loads(ip.read_text(encoding="utf-8")).get("warnings") or []:
                identity_warn.add(w.split(":")[0].strip())
        except Exception:
            pass

    scores = {}
    if SERVICES.is_dir():
        for p in SERVICES.glob("*.yaml"):
            if p.name.startswith("example"):
                continue
            sid = p.stem
            score = 80.0
            if sid in identity_warn:
                score -= 15
            st = drift.get(sid)
            if st == "warn":
                score -= 5
            elif st == "high":
                score -= 12
            elif st == "review":
                score -= 25
            age_h = (datetime.now(timezone.utc).timestamp() - p.stat().st_mtime) / 3600
            if age_h < 48:
                score += 10
            elif age_h > 168:
                score -= 10
            scores[sid] = {
                "score": round(max(0, min(100, score)), 1),
                "band": "stable"
                if score >= 90
                else "maintained"
                if score >= 75
                else "review",
            }

    out = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": args.date,
        "services": dict(sorted(scores.items(), key=lambda x: -x[1]["score"])),
        "note": "v1 heuristic — multi-source agreement later",
    }
    (day / "service_scores.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"[service_score] scored={len(scores)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
