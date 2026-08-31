#!/usr/bin/env python3
"""V2.7 L4/L5 all aggregates."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from resolve_hierarchy import resolve_aggregate, rules_from_service_yaml, identity_key, expand_members, load_yaml, file_sid_for_member  # noqa: E402

REPORT = ROOT / "reports" / "hierarchy" / "golden.json"


def hash_keys(keys):
    return hashlib.sha256("\n".join(sorted(keys)).encode()).hexdigest()


def main() -> int:
    aggregates = load_yaml("memberships.yaml").get("aggregates") or {}
    services = load_yaml("services.yaml").get("services") or {}
    groups = load_yaml("groups.yaml").get("groups") or {}
    results, hard = [], 0
    for vid, agg in aggregates.items():
        resolved = resolve_aggregate(vid)
        h_agg = resolved["manifest"]["sha256"]
        keys = set()
        for mid in expand_members(agg, services, groups):
            for r in rules_from_service_yaml(file_sid_for_member(mid, services)):
                keys.add(r["identity_key"])
        l4 = h_agg == hash_keys(list(keys))
        legacy = {identity_key(r["type"], r["value"]) for r in rules_from_service_yaml(vid)}
        agg_keys = {r["identity_key"] for r in resolved["rules"]}
        l5 = (not legacy) or (legacy <= agg_keys)
        if not l4 or not l5:
            hard += 1
        results.append({"view": vid, "l4": l4, "l5": l5, "equal": legacy == agg_keys, "legacy": len(legacy), "aggregate": len(agg_keys)})
    report = {"results": results, "hard_failures": hard, "pass": hard == 0}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[hierarchy_golden] providers={len(results)} hard={hard} pass={hard==0}")
    return 0 if hard == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
