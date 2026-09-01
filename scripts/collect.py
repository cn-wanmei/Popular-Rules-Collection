#!/usr/bin/env python3
"""V3 source collector: concurrent, conditional, content-addressed acquisition."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fetchers import get_fetcher  # noqa: E402
from src.engine.cas.store import digest_bytes  # noqa: E402
from src.engine.collection.acquisition_cas import load as cas_load  # noqa: E402
from src.engine.collection.acquisition_cas import store as cas_store  # noqa: E402
from src.engine.collection.manifest import seal  # noqa: E402
from src.engine.collection.source_state import FetchStateStore  # noqa: E402

REGISTRY_PATH = ROOT / "sources" / "registry.yaml"
HEALTH_PATH = ROOT / "sources" / "health.yaml"
STATE_PATH = ROOT / "data" / "collection" / "fetch_state.json"
BACKUP_ROOT = ROOT / "backup"
DEFAULT_WORKERS = 12


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def today_str() -> str:
    return utc_now().strftime("%Y-%m-%d")


def load_registry() -> dict[str, Any]:
    data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not data or "sources" not in data:
        raise SystemExit(f"[collect] invalid registry: {REGISTRY_PATH}")
    return data


def load_health() -> dict[str, Any]:
    if HEALTH_PATH.exists():
        return yaml.safe_load(HEALTH_PATH.read_text(encoding="utf-8")) or {"sources": {}}
    return {"sources": {}}


def save_health(data: dict[str, Any]) -> None:
    data["updated_at"] = utc_now().isoformat()
    tmp = HEALTH_PATH.with_name(f".{HEALTH_PATH.name}.tmp")
    tmp.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8")
    tmp.replace(HEALTH_PATH)


def fetcher_cfg_for(src: dict[str, Any]) -> dict[str, Any]:
    explicit = src.get("fetch")
    if not explicit or not isinstance(explicit, dict) or not explicit.get("type"):
        raise ValueError(f"source '{src.get('id')}' missing fetch: in registry.yaml")
    return explicit


def rules_for(src: dict[str, Any]) -> list[dict[str, str]]:
    raw = src.get("rules") or src.get("files") or []
    out: list[dict[str, str]] = []
    for i, e in enumerate(raw):
        if not isinstance(e, dict) or not e.get("path"):
            print(f"  WARN {src.get('id')}: rules[{i}] invalid: {e!r}")
            continue
        local = str(e.get("local") or e.get("name") or Path(str(e["path"])).name)
        service = str(e.get("service") or e.get("name") or Path(local).stem).lower()
        for prefix in ("clash_", "surge_"):
            if service.startswith(prefix): service = service[len(prefix):]
        out.append({"path": str(e["path"]), "name": local, "service": service})
    return out


def _cache_key(source_id: str, entry_path: str) -> str:
    return f"{source_id}::{entry_path}"


def _fetch_entry(src_id: str, cfg: dict[str, Any], entry: dict[str, str], previous: dict[str, Any]) -> dict[str, Any]:
    headers: dict[str, str] = {}
    if previous.get("etag"): headers["If-None-Match"] = str(previous["etag"])
    if previous.get("last_modified"): headers["If-Modified-Since"] = str(previous["last_modified"])
    fetcher = get_fetcher(cfg)
    result = fetcher.fetch_one({**entry, "headers": headers})
    result.source_id = src_id
    meta: dict[str, Any] = {"name": entry["name"], "path": entry["path"], "service": entry["service"],
        "url": result.url, "status_code": result.status_code, "etag": result.headers.get("etag"),
        "last_modified": result.headers.get("last-modified")}

    if result.not_modified:
        cached_digest = previous.get("cas_sha256") or previous.get("sha256")
        if cached_digest:
            try:
                content = cas_load(str(cached_digest), ROOT)
                if digest_bytes(content) == str(cached_digest):
                    return {**meta, "status": "not_modified", "content": content, "cas_sha256": str(cached_digest),
                            "sha256": str(cached_digest), "size": len(content), "cached_from_cas": True}
            except (FileNotFoundError, RuntimeError, OSError):
                pass
        # A 304 without a valid immutable cached object is unsafe; refetch unconditionally.
        result = fetcher.fetch_one(entry)
        result.source_id = src_id
        meta.update({"status_code": result.status_code, "etag": result.headers.get("etag") or meta.get("etag"),
                     "last_modified": result.headers.get("last-modified") or meta.get("last_modified")})

    if not result.ok or result.content is None:
        return {**meta, "status": "failed", "error": result.error}
    if not result.content.strip():
        return {**meta, "status": "blocked_empty", "error": "empty body"}
    digest = result.sha256 or digest_bytes(result.content)
    if digest_bytes(result.content) != digest:
        return {**meta, "status": "failed", "error": "content digest mismatch"}
    return {**meta, "status": "ok", "content": result.content, "sha256": digest, "cas_sha256": digest, "size": len(result.content)}


def collect_source(src: dict[str, Any], day_dir: Path, health: dict[str, Any], state: FetchStateStore, max_workers: int) -> dict[str, Any]:
    sid = str(src["id"]); entries = rules_for(src); out_dir = day_dir / "sources" / sid
    out_dir.mkdir(parents=True, exist_ok=True); cfg = fetcher_cfg_for(src)
    workers = max(1, min(max_workers, len(entries) or 1)); results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix=f"fetch-{sid}") as pool:
        futures = {pool.submit(_fetch_entry, sid, cfg, e, state.get(_cache_key(sid, e["path"]))): e for e in entries}
        for future in as_completed(futures):
            entry = futures[future]
            try: results.append(future.result())
            except Exception as exc: results.append({"name": entry["name"], "path": entry["path"], "service": entry["service"], "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    results.sort(key=lambda x: (x.get("service", ""), x.get("name", ""), x.get("path", "")))
    files_meta: list[dict[str, Any]] = []; ok = not_modified = fail = empty_blocked = 0
    for item in results:
        status = item["status"]; local = out_dir / item["name"]
        if status in {"ok", "not_modified"}:
            content = item["content"]; sha = str(item["cas_sha256"])
            cas_store(content, ROOT)
            local.write_bytes(content)
            ok += status == "ok"; not_modified += status == "not_modified"
            meta = {k: v for k, v in item.items() if k != "content"}; meta["local"] = str(local.relative_to(day_dir)); meta["cas_object"] = f"data/cas/acquisition/{sha[:2]}/{sha[2:]}"
            files_meta.append(meta)
            state.put(_cache_key(sid, item["path"]), etag=item.get("etag"), last_modified=item.get("last_modified"), sha256=sha, cas_sha256=sha, size=len(content), local=str(local.relative_to(ROOT)))
        else:
            fail += status != "blocked_empty"; empty_blocked += status == "blocked_empty"
            files_meta.append({k: v for k, v in item.items() if k != "content"})
    hs = health.setdefault("sources", {}).setdefault(sid, {})
    hs.update({"last_attempt": utc_now().isoformat(), "files_ok": ok, "files_not_modified": not_modified, "files_failed": fail, "empty_blocked": empty_blocked, "rules_declared": len(entries), "conditional_cache_hits": not_modified, "fetch_workers": workers, "cas_objects": ok + not_modified})
    if ok + not_modified > 0:
        hs["last_success"] = utc_now().isoformat(); hs["failure_count"] = 0; hs["status"] = "healthy" if fail == 0 and empty_blocked == 0 else "degraded"
    else:
        hs["last_failure"] = utc_now().isoformat(); hs["failure_count"] = int(hs.get("failure_count") or 0) + 1; hs["status"] = "down"; hs["reason"] = "all fetches failed" if entries else "no rules in registry"
    return {"source": sid, "fetch": cfg.get("type"), "files_ok": ok, "files_not_modified": not_modified, "files_failed": fail, "empty_blocked": empty_blocked, "rules_declared": len(entries), "conditional_cache_hits": not_modified, "files": files_meta, "registry_priority": src.get("priority"), "registry_trust": src.get("trust"), "concurrency_workers": workers}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect from registry.yaml (V3 source acquisition)")
    parser.add_argument("--date", default=today_str()); parser.add_argument("--source", action="append"); parser.add_argument("--list", action="store_true"); parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 64: raise SystemExit("[collect] --workers must be between 1 and 64")
    registry = load_registry(); sources = [s for s in registry.get("sources", []) if s.get("enabled")]
    if args.list:
        for s in registry.get("sources", []): print(f"  [{'on ' if s.get('enabled') else 'off'}] {s['id']:16} rules={len(s.get('rules') or s.get('files') or []):3} priority={s.get('priority')} fetch={(s.get('fetch') or {}).get('type')}")
        return 0
    if args.source: sources = [s for s in sources if s["id"] in args.source]
    day_dir = BACKUP_ROOT / args.date; (day_dir / "sources").mkdir(parents=True, exist_ok=True); manifests_dir = day_dir / "manifests"; manifests_dir.mkdir(parents=True, exist_ok=True)
    health = load_health(); state = FetchStateStore(STATE_PATH); summary = []
    print(f"[collect] registry v{registry.get('version')} date={args.date} sources={len(sources)} workers={args.workers}")
    for src in sources:
        try: cfg = fetcher_cfg_for(src)
        except ValueError as e: print(f"[collect] SKIP {src.get('id')}: {e}"); continue
        print(f"[collect] → {src['id']} ({cfg.get('type')}, {len(src.get('rules') or src.get('files') or [])} rules)")
        man = collect_source(src, day_dir, health, state, args.workers); summary.append(man)
        (manifests_dir / f"{src['id']}.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    state.save()
    day_manifest = seal({"date": args.date, "registry_version": registry.get("version"), "collection_leaf": "service_rules_v3", "sources": summary})
    (manifests_dir / "_day.json").write_text(json.dumps(day_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"); save_health(health)
    total_ok = sum(s["files_ok"] for s in summary); total_unchanged = sum(s["files_not_modified"] for s in summary); total_fail = sum(s["files_failed"] for s in summary)
    print(f"[collect] done ok={total_ok} not_modified={total_unchanged} failed={total_fail}")
    return 0 if total_ok + total_unchanged > 0 else 1

if __name__ == "__main__": sys.exit(main())
