#!/usr/bin/env python3
"""hot_missing_audit.py — Phase 3B missing-service audit with reason codes."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

HOT_WATCH = [
    "qwen", "kimi", "yuanbao", "wenxiaoyan", "deepseek", "doubao",
    "mistral", "midjourney", "openai", "claude", "gemini", "perplexity", "xai", "groq",
    "snapchat", "signal", "threads", "bluesky", "mastodon",
    "temu", "aliexpress", "etsy", "shopee", "lazada",
    "crunchyroll", "tidal",
    "roblox", "minecraft",
    "npm", "pypi", "supabase", "cursor",
    "googlemaps", "googledrive",
]


def load_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def load_primary() -> dict[str, dict]:
    services: dict = {}
    for name in ("service_primary.yaml", "service_primary_extra.yaml"):
        doc = load_yaml(ROOT / "config" / name)
        services.update(doc.get("services") or {})
        for sid, ov in (doc.get("aggregate_overrides") or {}).items():
            base = dict(services.get(sid) or {})
            base.update(ov or {})
            services[sid] = base
    return services


def classify(sid: str, primary: dict, intent: dict) -> dict:
    materialized = (ROOT / "database/services" / f"{sid}.yaml").exists()
    in_primary = sid in primary
    intent_meta = intent.get(sid)
    code = None
    reason = None
    if isinstance(intent_meta, dict):
        code = str(intent_meta.get("code") or "").upper() or None
        reason = intent_meta.get("reason")
    elif intent_meta:
        reason = str(intent_meta)
        code = "NO_UPSTREAM"

    if materialized:
        try:
            doc = yaml.safe_load(
                (ROOT / "database/services" / f"{sid}.yaml").read_text(encoding="utf-8")
            ) or {}
            rules = doc.get("rules") or []
            dom = ROOT / "database/domains" / f"{sid}.txt"
            has_dom = dom.exists() and dom.stat().st_size > 0
            if not rules and not has_dom:
                return {
                    "service": sid,
                    "status": "NORMALIZED_EMPTY",
                    "code": "NORMALIZED_EMPTY",
                    "reason": "materialized but empty rules/domains",
                }
        except Exception:
            pass
        return {
            "service": sid,
            "status": "MATERIALIZED",
            "code": "MATERIALIZED",
            "reason": reason or "ok",
        }

    if code:
        return {
            "service": sid,
            "status": "INTENTIONAL_UNMATERIALIZED",
            "code": code,
            "reason": reason or code,
        }

    if not in_primary:
        return {
            "service": sid,
            "status": "NOT_IN_PRIMARY",
            "code": "NOT_REGISTERED",
            "reason": "not in service_primary",
        }

    return {
        "service": sid,
        "status": "UNEXPECTED_MISSING",
        "code": "UNEXPECTED_MISSING",
        "reason": "in primary, not materialized, not in intentional_unmaterialized",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)

    primary = load_primary()
    intent = load_yaml(ROOT / "config/intentional_unmaterialized.yaml").get("services") or {}

    ids = set(HOT_WATCH) | set(intent.keys())
    for sid in primary:
        if not (ROOT / "database/services" / f"{sid}.yaml").exists() and sid not in intent:
            ids.add(sid)

    entries = [classify(sid, primary, intent) for sid in sorted(ids)]
    by_code: dict[str, list] = {}
    for e in entries:
        by_code.setdefault(e["code"], []).append(e["service"])

    hot_rows = [classify(sid, primary, intent) for sid in HOT_WATCH]
    report = {
        "date": args.date,
        "hot_watch": hot_rows,
        "all_audited": entries,
        "by_code": {k: sorted(v) for k, v in by_code.items()},
        "counts": {k: len(v) for k, v in by_code.items()},
    }
    (day / "hot_missing.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    md = [
        f"# HOT_MISSING_SERVICES ({args.date})",
        "",
        "Reason codes: `MATERIALIZED` / `NO_UPSTREAM` / `COVERED_BY_AGGREGATE` / "
        "`MAPS_TO` / `UNEXPECTED_MISSING` / `NORMALIZED_EMPTY` / `NOT_REGISTERED` / …",
        "",
        "## Hot watchlist",
        "",
        "| service | status | code | reason |",
        "|---------|--------|------|--------|",
    ]
    for e in hot_rows:
        md.append(
            f"| {e['service']} | {e['status']} | {e['code']} | {e.get('reason', '')} |"
        )
    md += ["", "## Counts by code", ""]
    for k, n in sorted(report["counts"].items(), key=lambda x: -x[1]):
        md.append(f"- **{k}**: {n}")
    md += ["", "## Unexpected missing", ""]
    for sid in report["by_code"].get("UNEXPECTED_MISSING") or []:
        md.append(f"- `{sid}`")
    if not report["by_code"].get("UNEXPECTED_MISSING"):
        md.append("- (none)")

    text = "\n".join(md) + "\n"
    (day / "HOT_MISSING_SERVICES.md").write_text(text, encoding="utf-8")
    (REPORTS / "HOT_MISSING_SERVICES.md").write_text(text, encoding="utf-8")
    print(
        f"[hot_missing_audit] audited={len(entries)} "
        f"unexpected={len(report['counts'].get('UNEXPECTED_MISSING', []))} "
        f"hot={len(hot_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
