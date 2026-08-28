#!/usr/bin/env python3
"""dataset_diff.py — Phase 3A content-aware dataset diff (not line-count only).

Compares current dataset files to previous snapshot:
  old_count / new_count / added / removed / shrink_ratio / sha256

Writes:
  reports/<date>/dataset_diff.json
  reports/<date>/dataset_snapshot.json  (becomes next baseline)
  reports/dataset_baseline.json         (rolling baseline)
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
BASELINE = REPORTS / "dataset_baseline.json"

DATASET_GLOBS = [
    ("network", "database/network/*.txt"),
    ("geosite", "database/geosite/*.txt"),
    ("geoip", "database/geoip/*.txt"),
    ("asn", "database/asn/*.yaml"),
    ("policy", "database/policies/**/*.*"),
    ("ip_sidecar", "database/ips/*.txt"),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_lines(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if s and not s.startswith("#"):
            out.append(s)
    return out


def collect_current() -> dict[str, dict]:
    items: dict[str, dict] = {}
    for kind, pattern in DATASET_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if not path.is_file():
                continue
            if path.name.startswith("_"):
                continue
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            lines = load_lines(path)
            sample = lines if len(lines) <= 200_000 else lines[:50_000]
            items[rel] = {
                "kind": kind,
                "path": rel,
                "count": len(lines),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
                "lines_sample_hash": hashlib.sha256(
                    "\n".join(sample).encode()
                ).hexdigest(),
                "lines": lines if len(lines) <= 50_000 else None,
            }
    return items


def diff_one(old: dict | None, new: dict) -> dict:
    if old is None:
        return {
            "old_count": 0,
            "new_count": new["count"],
            "added": new["count"],
            "removed": 0,
            "changed": 0,
            "shrink_ratio": 0.0,
            "growth_ratio": 0.0,
            "sha_changed": True,
            "status": "new",
        }
    oc, nc = int(old.get("count") or 0), int(new.get("count") or 0)
    added = removed = changed = 0
    if old.get("lines") is not None and new.get("lines") is not None:
        oset = set(old["lines"])
        nset = set(new["lines"])
        added = len(nset - oset)
        removed = len(oset - nset)
    else:
        if nc > oc:
            added = nc - oc
        elif oc > nc:
            removed = oc - nc
    shrink = 0.0
    growth = 0.0
    if oc > 0:
        if nc < oc:
            shrink = (oc - nc) / oc
        if nc > oc:
            growth = (nc - oc) / oc
    sha_changed = old.get("sha256") != new.get("sha256")
    return {
        "old_count": oc,
        "new_count": nc,
        "added": added,
        "removed": removed,
        "changed": changed,
        "shrink_ratio": round(shrink, 4),
        "growth_ratio": round(growth, 4) if growth else 0.0,
        "sha_changed": sha_changed,
        "status": "unchanged" if not sha_changed and oc == nc else "updated",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)

    current = collect_current()
    baseline: dict = {}
    if BASELINE.exists():
        try:
            baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        except Exception:
            baseline = {}
    prev_items = (baseline.get("items") or {}) if isinstance(baseline, dict) else {}

    diffs: dict[str, dict] = {}
    for rel, new in current.items():
        diffs[rel] = diff_one(prev_items.get(rel), new)

    for rel in prev_items:
        if rel not in current:
            diffs[rel] = {
                "old_count": prev_items[rel].get("count", 0),
                "new_count": 0,
                "added": 0,
                "removed": prev_items[rel].get("count", 0),
                "changed": 0,
                "shrink_ratio": 1.0,
                "growth_ratio": 0.0,
                "sha_changed": True,
                "status": "missing",
            }

    report = {
        "date": args.date,
        "compared_to": baseline.get("date"),
        "dataset_count": len(current),
        "diffs": diffs,
    }
    snap_items = {
        rel: {k: v for k, v in meta.items() if k != "lines"}
        for rel, meta in current.items()
    }
    snapshot = {"date": args.date, "items": snap_items}

    (day / "dataset_diff.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (day / "dataset_snapshot.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    BASELINE.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    shrinks = sum(1 for d in diffs.values() if (d.get("shrink_ratio") or 0) >= 0.3)
    print(
        f"[dataset_diff] datasets={len(current)} compared_to={baseline.get('date')} "
        f"shrink>=30%={shrinks}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
