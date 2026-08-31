#!/usr/bin/env python3
"""V2.5 L4 Hierarchy + L5 Compatibility (same snapshot)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from resolve_hierarchy import resolve_aggregate, rules_from_service_yaml, identity_key, expand_members, load_yaml  # noqa: E402

REPORT = ROOT / "reports" / "hierarchy" / "golden.json"


def hash_keys(keys):
    return hashlib.sha256("\n".join(sorted(keys)).encode()).hexdigest()


def main() -> int:
    hard = 0
    agg = resolve_aggregate("google")
    h_agg = agg["manifest"]["sha256"]
    aggregates = load_yaml("memberships.yaml").get("aggregates") or {}
    services = load_yaml("services.yaml").get("services") or {}
    groups = load_yaml("groups.yaml").get("groups") or {}
    mids = expand_members(aggregates["google"], services, groups)
    load_map = {"google-core": "google"}
    keys = set()
    for mid in mids:
        for r in rules_from_service_yaml(load_map.get(mid, mid)):
            keys.add(r["identity_key"])
    h_union = hash_keys(list(keys))
    l4_ok = h_agg == h_union
    if not l4_ok:
        hard += 1
    legacy = {identity_key(r["type"], r["value"]) for r in rules_from_service_yaml("google")}
    agg_keys = {r["identity_key"] for r in agg["rules"]}
    l5_ok = legacy <= agg_keys
    if not l5_ok:
        hard += 1
    report = {
        "l4_hierarchy": {"pass": l4_ok, "aggregate_sha": h_agg, "union_sha": h_union},
        "l5_compatibility": {"pass": l5_ok, "equal": legacy == agg_keys, "legacy_count": len(legacy), "aggregate_count": len(agg_keys)},
        "hard_failures": hard,
        "pass": hard == 0,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[hierarchy_golden] L4={l4_ok} L5={l5_ok} equal={legacy == agg_keys} hard={hard}")
    return 0 if hard == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
