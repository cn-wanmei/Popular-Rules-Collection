#!/usr/bin/env python3
"""V3 source collector: scheduled, conditional, content-addressed acquisition."""
from __future__ import annotations

import argparse
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
from src.engine.collection.acquisition_cas import load as cas_load, store as cas_store  # noqa: E402
from src.engine.collection.manifest import seal  # noqa: E402
from src.engine.collection.scheduler import decide, next_retry_at  # noqa: E402
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
    if not HEALTH_PATH.exists():
        return {"sources": {}}
    return yaml.safe_load(HEALTH_PATH.read_text(encoding="utf-8")) or {"sources": {}}


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
    out: list[dict[str, str]] = []
    for i, entry in enumerate(src.get("rules") or src.get("files") or []):
        if not isinstance(entry, dict) or not entry.get("path"):
            print(f"  WARN {src.get('id')}: rules[{i}] invalid: {entry!r}")
            continue
        local = str(entry.get("local") or entry.get("name") or Path(str(entry["path"])).name)
        service = str(entry.get("service") or entry.get("name") or Path(local).stem).lower()
        for prefix in ("clash_", "surge_"):
            if service.startswith(prefix):
                service = service[len(prefix):]
        out.append({"path": str(entry["path"]), "name": local, "service": service})
    return out


def _cache_key(source_id: str, entry_path: str) -> str:
    return f"{source_id}::{entry_path}"


def _load_cached(previous: dict[str, Any]) -> tuple[bytes, str] | None:
    digest = previous.get("cas_sha256") or previous.get("sha256")
    if not digest:
        return None
    try:
        content = cas_load(str(digest), ROOT)
    except (FileNotFoundError, RuntimeError, OSError):
        return None
    if digest_bytes(content) != str(digest):
        return None
    return content, str(digest)


def _fetch_entry(src: dict[str, Any], cfg: dict[str, Any], entry: dict[str, str], previous: dict[str, Any], *, force_refresh: bool = False) -> dict[str, Any]:
    sid = str(src["id"])
    decision = decide(previous, src, force=force_refresh)
    if decision.action.startswith("SKIP_"):
        cached = _load_cached(previous)
        if cached is not None:
            content, digest = cached
            return {"name": entry["name"], "path": entry["path"], "service": entry["service"], "url": previous.get("last_url"),
                    "status": "skipped", "decision": decision.action, "reason": decision.reason, "content": content,
                    "sha256": digest, "cas_sha256": digest, "size": len(content), "cached_from_cas": True}
        decision = type(decision)("FETCH_DUE", "cached_snapshot_unavailable")

    headers: dict[str, str] = {}
    if previous.get("etag"):
        headers["If-None-Match"] = str(previous["etag"])
    if previous.get("last_modified"):
        headers["If-Modified-Since"] = str(previous["last_modified"])
    result = get_fetcher(cfg).fetch_one({**entry, "headers": headers})
    result.source_id = sid
    meta = {"name": entry["name"], "path": entry["path"], "service": entry["service"], "url": result.url,
            "status_code": result.status_code, "etag": result.headers.get("etag"),
            "last_modified": result.headers.get("last-modified"), "decision": decision.action, "reason": decision.reason}
    if result.not_modified:
        cached = _load_cached(previous)
        if cached is not None:
            content, digest = cached
            return {**meta, "status": "not_modified", "content": content, "cas_sha256": digest, "sha256": digest,
                    "size": len(content), "cached_from_cas": True}
        result = get_fetcher(cfg).fetch_one(entry)
        result.source_id = sid
        meta.update({"url": result.url, "status_code": result.status_code, "etag": result.headers.get("etag") or meta.get("etag"),
                     "last_modified": result.headers.get("last-modified") or meta.get("last_modified"),
                     "decision": "FETCH_RECOVERY", "reason": "304_cache_unavailable"})
    if not result.ok or result.content is None:
        return {**meta, "status": "failed", "error": result.error}
    if not result.content.strip():
        return {**meta, "status": "blocked_empty", "error": "empty body"}
    sha = result.sha256 or digest_bytes(result.content)
    if digest_bytes(result.content) != sha:
        return {**meta, "status": "failed", "error": "content digest mismatch"}
    return {**meta, "status": "ok", "content": result.content, "sha256": sha, "cas_sha256": sha, "size": len(result.content)}


def _record_failure(state: FetchStateStore, key: str, previous: dict[str, Any], item: dict[str, Any]) -> None:
    failures = int(previous.get("failure_count") or 0) + 1
    now = utc_now()
    state.put(key, last_checked_at=now.isoformat(), last_failure_at=now.isoformat(), failure_count=failures,
              last_status=item.get("status"), last_url=item.get("url"),
              next_retry_at=next_retry_at(now=now, failure_count=failures).isoformat())


def collect_source(src: dict[str, Any], day_dir: Path, health: dict[str, Any], state: FetchStateStore,
                   max_workers: int, *, force_refresh: bool = False) -> dict[str, Any]:
    sid = str(src["id"])
    entries = rules_for(src)
    out_dir = day_dir / "sources" / sid
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = fetcher_cfg_for(src)
    workers = max(1, min(max_workers, len(entries) or 1))
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix=f"fetch-{sid}") as pool:
        futures = {pool.submit(_fetch_entry, src, cfg, entry, state.get(_cache_key(sid, entry["path"])), force_refresh=force_refresh): entry for entry in entries}
        for future in as_completed(futures):
            entry = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                results.append({"name": entry["name"], "path": entry["path"], "service": entry["service"], "status": "failed",
                                "decision": "FETCH_ERROR", "reason": type(exc).__name__, "error": f"{type(exc).__name__}: {exc}"})

    results.sort(key=lambda x: (x.get("service", ""), x.get("name", ""), x.get("path", "")))
    files_meta: list[dict[str, Any]] = []
    fetched = unchanged = skipped = fail = empty_blocked = 0
    for item in results:
        status = item["status"]
        key = _cache_key(sid, item["path"])
        previous = state.get(key)
        if status in {"ok", "not_modified", "skipped"}:
            content = item["content"]
            sha = str(item["cas_sha256"])
            cas_store(content, ROOT)
            local = out_dir / item["name"]
            local.write_bytes(content)
            fetched += status == "ok"
            unchanged += status == "not_modified"
            skipped += status == "skipped"
            meta = {k: v for k, v in item.items() if k != "content"}
            meta["local"] = str(local.relative_to(day_dir))
            meta["cas_object"] = f"data/cas/acquisition/{sha[:2]}/{sha[2:]}"
            files_meta.append(meta)
            if status != "skipped":
                now = utc_now()
                state.put(key, etag=item.get("etag"), last_modified=item.get("last_modified"), sha256=sha, cas_sha256=sha,
                          size=len(content), local=str(local.relative_to(ROOT)), last_checked_at=now.isoformat(),
                          last_success_at=now.isoformat(), last_changed_at=now.isoformat() if status == "ok" else previous.get("last_changed_at"),
                          last_status=status, last_url=item.get("url"), failure_count=0, next_retry_at="")
        else:
            fail += status != "blocked_empty"
            empty_blocked += status == "blocked_empty"
            files_meta.append({k: v for k, v in item.items() if k != "content"})
            _record_failure(state, key, previous, item)

    hs = health.setdefault("sources", {}).setdefault(sid, {})
    hs.update({"last_attempt": utc_now().isoformat(), "files_ok": fetched, "files_not_modified": unchanged, "files_skipped": skipped,
               "files_failed": fail, "empty_blocked": empty_blocked, "rules_declared": len(entries), "conditional_cache_hits": unchanged,
               "scheduler_skips": skipped, "fetch_workers": workers, "cas_objects": fetched + unchanged + skipped})
    if fetched + unchanged + skipped > 0:
        hs["last_success"] = utc_now().isoformat()
        hs["failure_count"] = 0
        hs["status"] = "healthy" if fail == 0 and empty_blocked == 0 else "degraded"
    else:
        hs["last_failure"] = utc_now().isoformat()
        hs["failure_count"] = int(hs.get("failure_count") or 0) + 1
        hs["status"] = "down"
        hs["reason"] = "all fetches failed" if entries else "no rules in registry"

    return {"source": sid, "fetch": cfg.get("type"), "files_ok": fetched, "files_not_modified": unchanged, "files_skipped": skipped,
            "files_failed": fail, "empty_blocked": empty_blocked, "rules_declared": len(entries), "conditional_cache_hits": unchanged,
            "scheduler_skips": skipped, "files": files_meta, "registry_priority": src.get("priority"), "registry_trust": src.get("trust"),
            "critical": bool(src.get("critical") or (src.get("collection") or {}).get("critical")), "concurrency_workers": workers}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect from registry.yaml (V3 scheduled source acquisition)")
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--source", action="append")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--force-refresh", action="store_true", help="bypass freshness and retry backoff for selected sources")
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 64:
        raise SystemExit("[collect] --workers must be between 1 and 64")

    registry = load_registry()
    sources = [s for s in registry.get("sources", []) if s.get("enabled")]
    if args.list:
        for source in registry.get("sources", []):
            print(f"  [{'on ' if source.get('enabled') else 'off'}] {source['id']:16} rules={len(source.get('rules') or source.get('files') or []):3} priority={source.get('priority')} fetch={(source.get('fetch') or {}).get('type')}")
        return 0
    if args.source:
        sources = [s for s in sources if s["id"] in args.source]

    day_dir = BACKUP_ROOT / args.date
    (day_dir / "sources").mkdir(parents=True, exist_ok=True)
    manifests_dir = day_dir / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    health = load_health()
    state = FetchStateStore(STATE_PATH)
    summary: list[dict[str, Any]] = []
    print(f"[collect] registry v{registry.get('version')} date={args.date} sources={len(sources)} workers={args.workers} force={args.force_refresh}")
    for source in sources:
        try:
            cfg = fetcher_cfg_for(source)
        except ValueError as exc:
            print(f"[collect] SKIP {source.get('id')}: {exc}")
            continue
        print(f"[collect] → {source['id']} ({cfg.get('type')}, {len(source.get('rules') or source.get('files') or [])} rules)")
        manifest = collect_source(source, day_dir, health, state, args.workers, force_refresh=args.force_refresh)
        summary.append(manifest)
        (manifests_dir / f"{source['id']}.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    state.save()
    day_manifest = seal({"date": args.date, "registry_version": registry.get("version"), "collection_leaf": "service_rules_v3", "sources": summary})
    (manifests_dir / "_day.json").write_text(json.dumps(day_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    save_health(health)
    total_ok = sum(s["files_ok"] for s in summary)
    total_unchanged = sum(s["files_not_modified"] for s in summary)
    total_skipped = sum(s["files_skipped"] for s in summary)
    total_fail = sum(s["files_failed"] for s in summary)
    print(f"[collect] done ok={total_ok} not_modified={total_unchanged} skipped={total_skipped} failed={total_fail}")
    return 0 if total_ok + total_unchanged + total_skipped > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
