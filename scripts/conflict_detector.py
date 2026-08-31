#!/usr/bin/env python3
"""conflict_detector.py — reports only.

V2: policy from Decision SSOT when available, else service-layer heuristic.
Never silently assign every service to PROXY.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DEC_JSONL = ROOT / "generated" / "routing" / "decisions.jsonl"
REPORTS = ROOT / "reports"

DIRECT_HINTS = {
    "china", "private", "lan", "alibaba", "tencent", "baidu", "bytedance",
    "jingdong", "meituan", "bilibili", "wechat", "qq", "zhihu", "weibo",
    "xiaohongshu", "douyin", "netease", "iqiyi", "youku", "kuaishou",
    "unionpay", "alipay", "chinamobile", "chinatelecom", "chinaunicom",
    "12306", "ctrip", "pinduoduo", "xianyu", "eleme",
}


def service_default_action(sid: str, doc: dict) -> str:
    if doc.get("policy") and isinstance(doc["policy"], dict) and doc["policy"].get("default"):
        return str(doc["policy"]["default"]).lower()
    cat = str(doc.get("category") or "").lower()
    sid_l = sid.lower()
    if cat == "adblock" or sid_l.startswith("adblock"):
        return "reject"
    if cat in ("china", "domestic") or sid_l in DIRECT_HINTS or any(h in sid_l for h in DIRECT_HINTS):
        return "direct"
    return "proxy"


def load_decision_map() -> dict[str, str]:
    out: dict[str, str] = {}
    if not DEC_JSONL.exists():
        return out
    with DEC_JSONL.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            d = (rec.get("domain") or "").lower()
            a = str(rec.get("action") or "").lower()
            if d and a in ("direct", "proxy", "reject"):
                out[d] = a
    return out


def load_rules(decision_map: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        svc_policy = service_default_action(sid, doc)
        sources = [s.get("id") for s in doc.get("source") or [] if isinstance(s, dict)]
        for r in doc.get("rules") or []:
            val = (r.get("value") or "").lower()
            typ = r.get("type")
            if not typ or not val:
                continue
            policy = decision_map.get(val) or svc_policy
            rows.append({
                "service": sid,
                "type": typ,
                "value": val,
                "policy": policy,
                "sources": sources,
                "policy_source": "decision" if val in decision_map else "service_heuristic",
            })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()
    day = REPORTS / args.date / "conflicts"
    day.mkdir(parents=True, exist_ok=True)

    decision_map = load_decision_map()
    rows = load_rules(decision_map)
    by_match: dict[tuple[str, str], list] = defaultdict(list)
    for r in rows:
        by_match[(r["type"], r["value"])].append(r)

    critical, high, medium, low = [], [], [], []
    for (typ, val), items in by_match.items():
        policies = {i["policy"] for i in items}
        services = sorted({i["service"] for i in items})
        all_src: set[str] = set()
        for i in items:
            all_src.update(i.get("sources") or [])
        if len(policies) > 1 and len(services) > 1:
            critical.append({
                "level": "CRITICAL",
                "kind": "POLICY_MISMATCH",
                "match": {"type": typ, "value": val},
                "policies": sorted(policies),
                "services": services,
                "sources": sorted(all_src),
            })
        elif len(all_src) > 1 and len(policies) == 1:
            low.append({
                "level": "LOW",
                "kind": "MULTI_SOURCE_DUPLICATE",
                "match": {"type": typ, "value": val},
                "policy": next(iter(policies)),
                "sources": sorted(all_src),
                "services": services,
            })
        types_here = {i["type"] for i in items}
        if "domain" in types_here and "domain_suffix" in types_here:
            medium.append({
                "level": "MEDIUM",
                "kind": "SEMANTIC_DOMAIN_VS_SUFFIX",
                "value": val,
                "services": services,
            })

    summary = {
        "date": args.date,
        "decision_ssot_domains": len(decision_map),
        "rows": len(rows),
        "critical": len(critical),
        "high": len(high),
        "medium": len(medium),
        "low": len(low),
        "policy_source": "decision_ssot+service_heuristic",
        "note": "V2: no longer default all services to proxy",
    }
    (day / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (day / "critical.json").write_text(json.dumps(critical[:2000], indent=2) + "\n", encoding="utf-8")
    (day / "medium.json").write_text(json.dumps(medium[:2000], indent=2) + "\n", encoding="utf-8")
    (day / "summary.md").write_text(
        f"# Conflicts {args.date}\n\n| Level | Count |\n|-------|------:|\n"
        f"| CRITICAL | {summary['critical']} |\n| HIGH | {summary['high']} |\n"
        f"| MEDIUM | {summary['medium']} |\n| LOW | {summary['low']} |\n"
        f"\nDecision SSOT domains: {summary['decision_ssot_domains']}\n",
        encoding="utf-8",
    )
    print(
        f"[conflict_detector] rows={len(rows)} decision_map={len(decision_map)} "
        f"critical={len(critical)} medium={len(medium)} low={len(low)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
