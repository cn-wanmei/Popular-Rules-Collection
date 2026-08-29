#!/usr/bin/env python3
"""Statistics 2.0 — coverage / ecosystem / intentional-unmaterialized / icon metrics."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

_INTENTIONAL_FALLBACK = {
    "adblock-light": "hagezi_profile_deferred",
    "adblock-pro": "hagezi_profile_deferred",
    "blizzard": "maps_to_battlenet",
    "stripe": "keyword_only_empty_domain_set",
    "mistral": "no_verified_upstream",
    "gcp": "no_verified_upstream",
    "supabase": "no_verified_upstream",
    "roblox": "no_verified_upstream",
    "minecraft": "no_verified_upstream",
}

CLIENTS = ("mihomo", "sing-box", "surge", "shadowrocket", "quantumult-x", "egern", "loon")

VALID_CODES = {
    "NO_UPSTREAM",
    "COVERED_BY_AGGREGATE",
    "MAPS_TO",
    "DEFERRED_PROFILE",
    "KEYWORD_ONLY",
    "SOURCE_DRIFT",
}


def count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    n = 0
    with p.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                n += 1
    return n


def load_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def _infer_code(reason: str) -> str:
    r = (reason or "").lower()
    if "maps_to" in r or r.startswith("maps_to"):
        return "MAPS_TO"
    if "aggregate" in r or "covered_by" in r:
        return "COVERED_BY_AGGREGATE"
    if "deferred" in r or "hagezi" in r:
        return "DEFERRED_PROFILE"
    if "keyword" in r:
        return "KEYWORD_ONLY"
    if "drift" in r:
        return "SOURCE_DRIFT"
    return "NO_UPSTREAM"


def load_intentional_unmaterialized() -> dict:
    cfg = load_yaml(ROOT / "config" / "intentional_unmaterialized.yaml")
    services = cfg.get("services") if isinstance(cfg, dict) else None
    if isinstance(services, dict) and services:
        out = {}
        for sid, meta in services.items():
            if isinstance(meta, dict):
                reason = str(meta.get("reason") or "intentional")
                code = str(meta.get("code") or _infer_code(reason)).upper()
                if code not in VALID_CODES:
                    code = _infer_code(reason)
                out[str(sid)] = {"reason": reason, "code": code}
            else:
                reason = str(meta)
                out[str(sid)] = {"reason": reason, "code": _infer_code(reason)}
        return out
    return {k: {"reason": v, "code": _infer_code(v)} for k, v in _INTENTIONAL_FALLBACK.items()}


def _gate_status(path: Path) -> str:
    if not path.exists():
        return "unknown"
    try:
        rep = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return "unknown"
    if "status" in rep:
        return str(rep["status"])
    if "failures" in rep:
        return "fail" if rep.get("failures") else "pass"
    if "errors" in rep:
        return "fail" if rep.get("errors") else "pass"
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    day = ROOT / "reports" / args.date
    day.mkdir(parents=True, exist_ok=True)

    prim = load_yaml(ROOT / "config" / "service_primary.yaml")
    extra = load_yaml(ROOT / "config" / "service_primary_extra.yaml")
    services = dict(prim.get("services") or {})
    services.update(extra.get("services") or {})
    for sid, ov in (extra.get("aggregate_overrides") or {}).items():
        base = dict(services.get(sid) or {})
        base.update(ov)
        services[sid] = base

    registered = set(services.keys())
    reg_n = len(registered)

    materialized = set()
    services_dir = ROOT / "database" / "services"
    if services_dir.is_dir():
        for p in services_dir.glob("*.yaml"):
            if not p.name.startswith("example"):
                materialized.add(p.stem)
    mat_n = len(materialized)

    intentional_ssot = load_intentional_unmaterialized()
    intentional = {
        sid: meta
        for sid, meta in intentional_ssot.items()
        if sid in registered and sid not in materialized
    }
    intentional_reasons = {sid: meta.get("reason", "") for sid, meta in intentional.items()}
    intentional_by_code: dict = {}
    for sid, meta in intentional.items():
        code = meta.get("code") or "NO_UPSTREAM"
        intentional_by_code.setdefault(code, []).append(sid)
    for k in intentional_by_code:
        intentional_by_code[k] = sorted(intentional_by_code[k])

    unexpected_missing = sorted((registered - materialized) - set(intentional.keys()))
    cov = (mat_n / reg_n) if reg_n else 0.0
    daily_cov = ((mat_n + len(intentional)) / reg_n) if reg_n else 0.0

    domains = 0
    cidr = 0
    ddir = ROOT / "database" / "domains"
    idir = ROOT / "database" / "ips"
    if ddir.is_dir():
        for p in ddir.glob("*.txt"):
            domains += count_lines(p)
    if idir.is_dir():
        for p in idir.glob("*.txt"):
            cidr += count_lines(p)

    builder_coverage = {}
    try:
        from icon_stats_hook import collect_icon_coverage

        icon_coverage = collect_icon_coverage()
    except Exception as _e:
        icon_coverage = {"status": "error", "error": str(_e)}

    gen = ROOT / "generated"
    for c in CLIENTS:
        d = gen / c
        n = len(list(d.glob("*"))) if d.is_dir() else 0
        builder_coverage[c] = {"files": n, "status": "ok" if n > 0 else "missing"}

    ecosystem: dict = {}
    for sid, meta in services.items():
        if not isinstance(meta, dict):
            continue
        pc = meta.get("primary_category") or "other"
        ecosystem[str(pc)] = ecosystem.get(str(pc), 0) + 1

    reg = load_yaml(ROOT / "sources" / "registry.yaml")
    all_sources = list(reg.get("sources") or [])
    configured_sources = len(all_sources)
    enabled_ids = [s.get("id") for s in all_sources if s.get("enabled")]
    sources_on = len(enabled_ids)
    health = load_yaml(ROOT / "sources" / "health.yaml")
    health_sources = health.get("sources") or {}
    source_health = {k: (v or {}).get("status") for k, v in health_sources.items()}
    historical_ids = sorted(source_health.keys())
    healthy = sum(1 for s in source_health.values() if s == "healthy")
    enabled_health = [source_health.get(i) for i in enabled_ids if i in source_health]
    if enabled_health:
        health_ratio = sum(1 for s in enabled_health if s == "healthy") / len(enabled_health)
    else:
        health_ratio = (healthy / len(source_health)) if source_health else None
    collected_ids = []
    for sid in enabled_ids:
        meta = health_sources.get(sid) or {}
        if meta.get("status") == "healthy" and int(meta.get("files_ok") or 0) > 0:
            collected_ids.append(sid)
        elif meta.get("last_success") and int(meta.get("files_failed") or 0) == 0 and int(meta.get("files_ok") or 0) > 0:
            collected_ids.append(sid)
    collected_this_run = len(collected_ids)

    conflicts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    cpath = day / "conflicts" / "summary.json"
    if cpath.exists():
        conflicts.update(json.loads(cpath.read_text(encoding="utf-8")))

    validation = {
        "schema_validate": _gate_status(day / "schema_validate.json"),
        "builder_validate": _gate_status(day / "builder-validation.json"),
        "validate": _gate_status(day / "validation_report.json"),
    }
    bv = day / "builder-validation.json"
    if bv.exists():
        try:
            rep = json.loads(bv.read_text(encoding="utf-8"))
            validation["builder_failures"] = len(rep.get("failures") or [])
            if validation["builder_validate"] == "unknown":
                validation["builder_validate"] = "pass" if not rep.get("failures") else "fail"
        except Exception:
            pass

    stats = {
        "date": args.date,
        "version": 3,
        "service_coverage": {
            "registered": reg_n,
            "materialized": mat_n,
            "intentional_unmaterialized": len(intentional),
            "unexpected_missing": unexpected_missing,
            "coverage": round(cov, 4),
            "daily_coverage": round(daily_cov, 4),
        },
        "intentional_unmaterialized": intentional_reasons,
        "intentional_detail": intentional,
        "intentional_by_code": intentional_by_code,
        "rule_coverage": {
            "domains": domains,
            "ips": cidr,
            "database_services": len(materialized),
        },
        "source_health": {
            "configured_sources": configured_sources,
            "enabled_sources": sources_on,
            "collected_this_run": collected_this_run,
            "collected_ids": collected_ids,
            "historical_in_health": len(historical_ids),
            "enabled_ids": enabled_ids,
            "historical_ids": historical_ids,
            "statuses": source_health,
            "healthy_ratio": health_ratio,
        },
        "builder_coverage": builder_coverage,
        "ecosystem_coverage": dict(sorted(ecosystem.items())),
        "icon_coverage": icon_coverage,
        "validation": validation,
        "conflicts": {
            "critical": conflicts.get("critical", 0),
            "high": conflicts.get("high", 0),
            "medium": conflicts.get("medium", 0),
            "low": conflicts.get("low", 0),
        },
        "sources": sources_on,
        "services": mat_n,
        "domains": domains,
        "cidr": cidr,
        "build": {c: v["status"] for c, v in builder_coverage.items()},
    }

    ip_files = 0
    ip_lines = 0
    ip_dir = ROOT / "database" / "ips"
    if ip_dir.is_dir():
        for fp in ip_dir.glob("*.txt"):
            if fp.name.startswith("_"):
                continue
            ip_files += 1
            ip_lines += count_lines(fp)
    ip_reg = load_yaml(ROOT / "sources" / "ip_registry.yaml")
    ip_srcs = [s for s in (ip_reg.get("sources") or []) if isinstance(s, dict)]
    ip_enabled = sum(1 for s in ip_srcs if s.get("enabled"))
    stats["ip_track"] = {
        "registry_sources": len(ip_srcs),
        "enabled_sources": ip_enabled,
        "sidecar_files": ip_files,
        "cidr_lines": ip_lines,
        "note": "Prefer health/scope correctness over raw CIDR count",
    }

    (day / "statistics.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (day / "summary.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    sc = stats["service_coverage"]
    print(
        f"[statistics] registered={sc['registered']} materialized={sc['materialized']} "
        f"intentional={sc['intentional_unmaterialized']} coverage={sc['coverage']} "
        f"daily_coverage={sc['daily_coverage']} domains={domains} ips={cidr}"
    )
    print(
        f"  sources configured={configured_sources} enabled={sources_on} "
        f"collected={collected_this_run} historical_health={len(historical_ids)}"
    )
    print(f"  ip_track files={ip_files} cidrs={ip_lines} ip_sources_enabled={ip_enabled}")
    ic = stats.get("icon_coverage") or {}
    if isinstance(ic, dict) and "real_icons" in ic:
        print(
            f"  icon_coverage real={ic.get('real_icons')} placeholder={ic.get('placeholder')} "
            f"verified={ic.get('verified')} png256={ic.get('png256')}"
        )
    if unexpected_missing:
        print(f"  WARN unexpected_missing={unexpected_missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
