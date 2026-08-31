"""Universal IR v2 — hierarchy-focused services."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from src.v3.core.models.entity import EntityGraph
from src.v3.decision.engine import decide_for_service
from src.v3.hierarchy.resolver import body_service_id, expand_members


def build_ir(rules, memberships, graph: EntityGraph, out_dir: Path, focus_services=None) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    if focus_services is None:
        focus_services = set()
        for agg in graph.aggregates.values():
            for mid in expand_members(graph, agg.members, agg.exclude):
                focus_services.add(body_service_id(graph, mid))
                focus_services.add(mid)
        focus_services |= {"google", "apple", "microsoft", "tencent", "alibaba", "baidu"}
    sid_to_provider = {}
    for s in graph.services.values():
        if s.provider:
            sid_to_provider[s.id] = s.provider
            if s.body_service_id:
                sid_to_provider[s.body_service_id] = s.provider
    h = sha256()
    n = 0
    with (out_dir / "rules_v2.jsonl").open("w", encoding="utf-8") as f:
        for sid in sorted(focus_services):
            for rid in memberships.get(sid) or []:
                r = rules.get(rid)
                if not r:
                    continue
                cat = (r.get("classification") or {}).get("category") or "other"
                dec = decide_for_service(sid, str(cat))
                rec = {
                    "schema": "ir_v2",
                    "rule": {"id": rid, "type": r.get("type"), "value": r.get("value"), "identity_key": r.get("identity_key")},
                    "entity": {"provider": sid_to_provider.get(sid), "services": [sid], "groups": []},
                    "view": {"aggregates": []},
                    "decision": {"action": dec.action, "layer": dec.layer, "precedence": dec.precedence},
                    "provenance": r.get("provenance") or {},
                }
                line = json.dumps(rec, ensure_ascii=False)
                f.write(line + "\n")
                h.update(line.encode())
                n += 1
    meta = {"schema": "ir_v2", "generated_at": datetime.now(timezone.utc).isoformat(), "rules": n, "ir_digest": h.hexdigest(), "scope": "hierarchy_focus_services"}
    (out_dir / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta
