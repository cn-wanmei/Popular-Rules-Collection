#!/usr/bin/env python3
"""V2.2 Quarantine scan of latest backup sources."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from source_content_validate import validate_file

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "backup"
OUT = ROOT / "reports" / "quarantine"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    days = sorted([d for d in BACKUP.iterdir() if d.is_dir()], reverse=True) if BACKUP.exists() else []
    day = days[0] if days else None
    results = []
    if day and (day / "sources").exists():
        for f in (day / "sources").rglob("*"):
            if not f.is_file():
                continue
            reasons = validate_file(f)
            results.append({
                "path": str(f.relative_to(ROOT)),
                "bytes": f.stat().st_size,
                "state": "REJECTED" if reasons else "ACCEPTED",
                "reasons": reasons,
            })
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backup_day": str(day.name) if day else None,
        "scanned": len(results),
        "rejected": sum(1 for r in results if r["state"] == "REJECTED"),
        "accepted": sum(1 for r in results if r["state"] == "ACCEPTED"),
        "items": results[:2000],
    }
    out = OUT / f"{(day.name if day else 'none')}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[quarantine] scanned={report['scanned']} rejected={report['rejected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
