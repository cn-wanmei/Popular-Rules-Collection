#!/usr/bin/env python3
"""
collect.py — V1.2 registry-driven collector

Single source of truth: sources/registry.yaml
  - enabled / priority / trust
  - fetch: { type, owner, repo, branch } | { type: cdn, bases }
  - files: [ { path, name, service? }, ... ]

No hardcoded SOURCE_FILES or per-source fetch defaults in this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fetchers import get_fetcher  # noqa: E402

REGISTRY_PATH = ROOT / "sources" / "registry.yaml"
HEALTH_PATH = ROOT / "sources" / "health.yaml"
BACKUP_ROOT = ROOT / "backup"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def today_str() -> str:
    return utc_now().strftime("%Y-%m-%d")


def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or "sources" not in data:
        raise SystemExit(f"[collect] invalid registry: {REGISTRY_PATH}")
    return data


def load_health() -> dict[str, Any]:
    if HEALTH_PATH.exists():
        return yaml.safe_load(HEALTH_PATH.read_text(encoding="utf-8")) or {"sources": {}}
    return {"sources": {}}


def save_health(data: dict[str, Any]) -> None:
    data["updated_at"] = utc_now().isoformat()
    HEALTH_PATH.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )


def fetcher_cfg_for(src: dict[str, Any]) -> dict[str, Any]:
    """Require explicit fetch block in registry (no silent code defaults)."""
    explicit = src.get("fetch")
    if not explicit or not isinstance(explicit, dict) or not explicit.get("type"):
        raise ValueError(
            f"source '{src.get('id')}' missing required fetch: block in registry.yaml"
        )
    return explicit


def files_for(src: dict[str, Any]) -> list[dict[str, str]]:
    """Require files: list in registry. Each entry needs path + name."""
    entries = src.get("files") or []
    if not entries:
        print(f"  WARN {src.get('id')}: no files: in registry — skipping")
        return []
    out: list[dict[str, str]] = []
    for i, e in enumerate(entries):
        if not isinstance(e, dict) or not e.get("path") or not e.get("name"):
            print(f"  WARN {src.get('id')}: files[{i}] needs path+name, got {e!r}")
            continue
        item = {"path": str(e["path"]), "name": str(e["name"])}
        if e.get("service"):
            item["service"] = str(e["service"])
        out.append(item)
    return out


def collect_source(src: dict[str, Any], day_dir: Path, health: dict[str, Any]) -> dict[str, Any]:
    sid = src["id"]
    entries = files_for(src)
    out_dir = day_dir / "sources" / sid
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = fetcher_cfg_for(src)
    fetcher = get_fetcher(cfg)

    files_meta: list[dict[str, Any]] = []
    ok = fail = empty_blocked = 0

    for entry in entries:
        result = fetcher.fetch_one(entry)
        result.source_id = sid
        name = result.name
        local = out_dir / name

        if not result.ok or not result.content:
            files_meta.append({
                "name": name, "path": result.path, "url": result.url,
                "service": entry.get("service"), "status": "failed",
                "error": result.error, "status_code": result.status_code,
            })
            fail += 1
            print(f"  FAIL {sid}/{name}: {result.error}")
            continue

        if len(result.content.strip()) == 0:
            files_meta.append({
                "name": name, "path": result.path, "url": result.url,
                "service": entry.get("service"), "status": "blocked_empty",
                "error": "empty body — refuse to write",
            })
            empty_blocked += 1
            fail += 1
            print(f"  BLOCK empty {sid}/{name}")
            continue

        local.write_bytes(result.content)
        files_meta.append({
            "name": name, "path": result.path, "url": result.url,
            "service": entry.get("service"),
            "local": str(local.relative_to(day_dir)),
            "size": result.size, "sha256": result.sha256, "status": "ok",
        })
        ok += 1
        print(f"  OK   {sid}/{name} ({result.size} bytes, {(result.sha256 or '')[:12]}…)")

    hs = health.setdefault("sources", {}).setdefault(sid, {})
    hs["last_attempt"] = utc_now().isoformat()
    hs["files_ok"] = ok
    hs["files_failed"] = fail
    hs["empty_blocked"] = empty_blocked
    hs["files_declared"] = len(entries)
    if ok > 0:
        hs["last_success"] = utc_now().isoformat()
        hs["failure_count"] = 0
        hs["status"] = "healthy" if fail == 0 else "degraded"
        if fail:
            hs["reason"] = f"{fail} file(s) failed"
        else:
            hs.pop("reason", None)
    else:
        hs["last_failure"] = utc_now().isoformat()
        hs["failure_count"] = int(hs.get("failure_count") or 0) + 1
        hs["status"] = "down"
        hs["reason"] = "all fetches failed" if entries else "no files in registry"

    return {
        "source": sid,
        "fetch": cfg.get("type"),
        "timestamp": utc_now().isoformat(),
        "files_ok": ok,
        "files_failed": fail,
        "empty_blocked": empty_blocked,
        "files_declared": len(entries),
        "files": files_meta,
        "registry_priority": src.get("priority"),
        "registry_trust": src.get("trust"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect upstream from sources/registry.yaml (V1.2)"
    )
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--source", action="append", help="Only these source id(s)")
    parser.add_argument("--list", action="store_true", help="Print registry plan and exit")
    args = parser.parse_args()

    registry = load_registry()
    sources = [s for s in registry.get("sources", []) if s.get("enabled")]

    if args.list:
        for s in registry.get("sources", []):
            n = len(s.get("files") or [])
            flag = "on " if s.get("enabled") else "off"
            ft = (s.get("fetch") or {}).get("type")
            print(f"  [{flag}] {s['id']:16} files={n:3} priority={s.get('priority')} fetch={ft}")
        return 0

    if args.source:
        sources = [s for s in sources if s["id"] in args.source]

    day_dir = BACKUP_ROOT / args.date
    (day_dir / "sources").mkdir(parents=True, exist_ok=True)
    manifests_dir = day_dir / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)

    health = load_health()
    print(f"[collect] registry={REGISTRY_PATH.relative_to(ROOT)} date={args.date} sources={len(sources)}")
    summary: list[dict[str, Any]] = []
    for src in sources:
        try:
            cfg = fetcher_cfg_for(src)
        except ValueError as e:
            print(f"[collect] SKIP {src.get('id')}: {e}")
            continue
        print(f"[collect] → {src['id']} ({cfg.get('type')}, {len(src.get('files') or [])} files)")
        man = collect_source(src, day_dir, health)
        summary.append(man)
        (manifests_dir / f"{src['id']}.json").write_text(
            json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    (manifests_dir / "_day.json").write_text(
        json.dumps(
            {
                "date": args.date,
                "timestamp": utc_now().isoformat(),
                "registry_version": registry.get("version"),
                "sources": summary,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    save_health(health)

    total_ok = sum(s["files_ok"] for s in summary)
    total_fail = sum(s["files_failed"] for s in summary)
    print(f"[collect] done ok={total_ok} failed={total_fail}")
    print(f"[collect] health → {HEALTH_PATH.relative_to(ROOT)}")
    return 0 if total_ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
