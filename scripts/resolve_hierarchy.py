#!/usr/bin/env python3
"""Hierarchy resolve — V2 frozen baseline (self-contained)."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.core.models.rule import identity_key  # noqa: E402

SM = ROOT / "config" / "service_model"
OUT = ROOT / "reports" / "hierarchy"
MAX_EXPAND_DEPTH = 8


def load_yaml(name: str) -> dict:
    p = SM / name
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def rules_from_service_yaml(sid: str) -> list:
    p = ROOT / "database" / "services" / f"{sid}.yaml"
    if not p.exists():
        return []
    try:
        doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:
        return []
    out = []
    for r in doc.get("rules") or []:
        if not isinstance(r, dict):
            continue
        typ, val = r.get("type"), r.get("value")
        if not typ or not val:
            continue
        out.append({"type": typ, "value": str(val), "identity_key": identity_key(typ, str(val))})
    return out


def expand_members(agg: dict, services: dict, groups: dict) -> list:
    roots = list(agg.get("members") or [])
    exclude = set(agg.get("exclude") or [])
    expanded, seen = [], set()

    def walk(node: str, depth: int) -> None:
        if node in seen or depth > MAX_EXPAND_DEPTH:
            return
        seen.add(node)
        if node in groups:
            for child in (groups[node] or {}).get("members") or []:
                walk(child, depth + 1)
        elif node not in expanded:
            expanded.append(node)

    for m in roots:
        walk(m, 0)
    return [m for m in expanded if m not in exclude]


def file_sid_for_member(mid: str, services: dict) -> str:
    s = services.get(mid) or {}
    if s.get("legacy_body"):
        return str(s["legacy_body"])
    if mid.endswith("-core"):
        return mid[: -len("-core")]
    return mid


def resolve_aggregate(view_id: str) -> dict:
    aggregates = load_yaml("memberships.yaml").get("aggregates") or {}
    services = load_yaml("services.yaml").get("services") or {}
    groups = load_yaml("groups.yaml").get("groups") or {}
    agg = aggregates.get(view_id)
    if not agg:
        raise SystemExit(f"unknown aggregate: {view_id}")
    member_ids = expand_members(agg, services, groups)
    rule_map, per_member = {}, {}
    for mid in member_ids:
        rules = rules_from_service_yaml(file_sid_for_member(mid, services))
        for r in rules:
            if r["identity_key"] not in rule_map:
                rule_map[r["identity_key"]] = r
        per_member[mid] = len(rules)
    ordered = sorted(rule_map.values(), key=lambda r: r["identity_key"])
    sha = hashlib.sha256("\n".join(r["identity_key"] for r in ordered).encode()).hexdigest()
    return {
        "manifest": {
            "view": view_id, "kind": "aggregate", "schema": 1, "resolver_version": "v2.7-frozen",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "members": member_ids, "per_member_rule_rows": per_member,
            "canonical_rule_count": len(ordered), "sha256": sha,
            "note": "V2 freeze: legacy_body mapping remains for oracle only",
        },
        "rules": ordered,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    aggregates = load_yaml("memberships.yaml").get("aggregates") or {}
    summary = []
    for vid in sorted(aggregates.keys()):
        result = resolve_aggregate(vid)
        (OUT / f"{vid}_manifest.json").write_text(json.dumps(result["manifest"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary.append({"view": vid, "rules": result["manifest"]["canonical_rule_count"], "sha256": result["manifest"]["sha256"]})
        print(f"[resolve_hierarchy] {vid} rules={result['manifest']['canonical_rule_count']}")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
