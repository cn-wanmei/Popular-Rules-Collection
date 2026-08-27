#!/usr/bin/env python3
"""generated_manifest.py — Phase 3A: per-file inventory of generated/ outputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
CLIENTS = ("mihomo", "sing-box", "surge", "shadowrocket", "quantumult-x", "egern", "loon")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rule_count(p: Path) -> int:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    if p.suffix == ".json":
        try:
            data = json.loads(text)
            if isinstance(data, dict) and isinstance(data.get("rules"), list):
                n = 0
                for r in data["rules"]:
                    if not isinstance(r, dict):
                        continue
                    for k in ("domain", "domain_suffix", "domain_keyword", "ip_cidr", "ip_cidr6"):
                        v = r.get(k)
                        if isinstance(v, list):
                            n += len(v)
                        elif v:
                            n += 1
                return n
        except Exception:
            pass
    n = 0
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("---") or s.startswith("payload"):
            continue
        if s.startswith("- ") or "DOMAIN" in s or "IP-CIDR" in s or "," in s:
            n += 1
        elif p.suffix in (".list",) and not s.startswith("["):
            n += 1
    return n


def service_id(name: str) -> str:
    for suf in ("_domain.list", ".list", ".yaml", ".json"):
        if name.endswith(suf):
            return name[: -len(suf)]
    return name.rsplit(".", 1)[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    now = datetime.now(timezone.utc).isoformat()
    entries = []
    if GENERATED.is_dir():
        for client in CLIENTS:
            d = GENERATED / client
            if not d.is_dir():
                continue
            for f in sorted(d.iterdir()):
                if not f.is_file() or f.name == "manifest.json":
                    continue
                entries.append(
                    {
                        "service": service_id(f.name),
                        "client": client,
                        "file": str(f.relative_to(ROOT)),
                        "rule_count": rule_count(f),
                        "sha256": sha256_file(f),
                        "size": f.stat().st_size,
                        "generated_at": now,
                    }
                )

    manifest = {
        "schema_version": 1,
        "generated_at": now,
        "date": args.date,
        "file_count": len(entries),
        "clients": list(CLIENTS),
        "files": entries,
    }
    GENERATED.mkdir(parents=True, exist_ok=True)
    out = GENERATED / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    day = ROOT / "reports" / args.date
    day.mkdir(parents=True, exist_ok=True)
    (day / "generated_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"[generated_manifest] files={len(entries)} → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
