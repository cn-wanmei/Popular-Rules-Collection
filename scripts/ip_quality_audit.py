#!/usr/bin/env python3
"""ip_quality_audit.py — audit database/ips + ip_registry consistency.

Checks: invalid CIDR, exact dupes, unscoped files (no registry maps_to),
provenance presence.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ip_cidr import parse_cidr, containment_dedup  # noqa: E402

IPS = ROOT / "database" / "ips"
REG = ROOT / "sources" / "ip_registry.yaml"
PROV_DIR = ROOT / "database" / "ips_provenance"
REPORTS = ROOT / "reports"


def main() -> int:
    cfg = yaml.safe_load(REG.read_text(encoding="utf-8")) if REG.exists() else {}
    sources = cfg.get("sources") or []
    maps_to_sources: dict[str, list[str]] = defaultdict(list)
    for src in sources:
        if not isinstance(src, dict):
            continue
        mt = src.get("maps_to")
        if mt and src.get("enabled", True):
            maps_to_sources[str(mt)].append(str(src.get("id")))

    invalid = 0
    exact_dup_lines = 0
    total_lines = 0
    files = 0
    unscoped: list[str] = []
    by_target: dict[str, dict] = {}

    if IPS.is_dir():
        for path in sorted(IPS.glob("*.txt")):
            if path.name.startswith("_"):
                continue
            files += 1
            sid = path.stem
            raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
            valid_raw = []
            seen: set[str] = set()
            local_dup = 0
            for line in raw:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                total_lines += 1
                net = parse_cidr(s)
                if net is None:
                    invalid += 1
                    continue
                key = net.with_prefixlen
                if key in seen:
                    local_dup += 1
                    exact_dup_lines += 1
                    continue
                seen.add(key)
                valid_raw.append(key)
            collapsed = containment_dedup(valid_raw)
            removable = len(valid_raw) - len(collapsed)
            by_target[sid] = {
                "unique": len(valid_raw),
                "after_containment": len(collapsed),
                "containment_reducible": removable,
                "exact_dupes": local_dup,
                "registry_sources": maps_to_sources.get(sid, []),
            }
            if sid not in maps_to_sources and len(valid_raw) >= 50:
                unscoped.append(f"{sid} ({len(valid_raw)} cidrs, no ip_registry maps_to)")

    missing_prov = []
    if PROV_DIR.is_dir():
        for sid in by_target:
            if not (PROV_DIR / f"{sid}.json").exists() and by_target[sid]["unique"] > 20:
                missing_prov.append(sid)
    else:
        missing_prov = [s for s, m in by_target.items() if m["unique"] > 20]

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = REPORTS / day
    out_dir.mkdir(parents=True, exist_ok=True)
    rep = {
        "date": day,
        "files": files,
        "total_lines": total_lines,
        "invalid_cidr": invalid,
        "exact_duplicate_lines": exact_dup_lines,
        "unscoped_large": unscoped,
        "missing_provenance": missing_prov[:40],
        "targets": by_target,
        "registry_enabled_sources": sum(1 for s in sources if s.get("enabled")),
        "status": "pass" if invalid == 0 else "fail",
    }
    (out_dir / "ip_quality_audit.json").write_text(
        json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(
        f"[ip_quality_audit] files={files} lines={total_lines} "
        f"invalid={invalid} exact_dupes={exact_dup_lines} "
        f"unscoped_large={len(unscoped)} missing_prov={len(missing_prov)}"
    )
    for u in unscoped[:10]:
        print(f"  WARN unscoped: {u}")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
