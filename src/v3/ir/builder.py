"""Universal IR v2 — full corpus (streaming) or hierarchy focus."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from src.v3.core.models.entity import EntityGraph
from src.v3.decision.engine import decide_for_service
from src.v3.hierarchy.resolver import body_service_id, expand_members


def _invert_memberships(memberships: dict[str, list[str]]) -> dict[str, list[str]]:
    inv: dict[str, list[str]] = defaultdict(list)
    for sid, rids in memberships.items():
        for rid in rids:
            inv[rid].append(sid)
    return inv


def build_ir(rules, memberships, graph: EntityGraph, out_dir: Path, focus_services=None, full: bool = False) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    sid_to_provider: dict[str, str] = {}
    for s in graph.services.values():
        if s.provider:
            sid_to_provider[s.id] = s.provider
            if s.body_service_id:
                sid_to_provider[s.body_service_id] = s.provider
    if not full:
        if focus_services is None:
            focus_services = set()
            for agg in graph.aggregates.values():
                for mid in expand_members(graph, agg.members, agg.exclude):
                    focus_services.add(body_service_id(graph, mid))
                    focus_services.add(mid)
            focus_services |= {"google", "apple", "microsoft", "tencent", "alibaba", "baidu"}
    rid_to_svcs = _invert_memberships(memberships)
    h = sha256()
    n = 0
    by_action: dict[str, int] = {}
    path = out_dir / ("rules_v2_full.jsonl" if full else "rules_v2.jsonl")
    with path.open("w", encoding="utf-8") as f:
        if full:
            iterable = sorted(rules.keys())
        else:
            rids: set[str] = set()
            for sid in focus_services or []:
                rids.update(memberships.get(sid) or [])
            iterable = sorted(rids)
        for rid in iterable:
            r = rules.get(rid)
            if not r:
                continue
            svcs = rid_to_svcs.get(rid) or ["unknown"]
            primary = svcs[0]
            cat = (r.get("classification") or {}).get("category") or "other"
            dec = decide_for_service(primary, str(cat))
            rec = {
                "schema": "ir_v2",
                "rule": {"id": rid, "type": r.get("type"), "value": r.get("value"), "identity_key": r.get("identity_key")},
                "entity": {"provider": sid_to_provider.get(primary), "services": svcs[:32], "groups": []},
                "view": {"aggregates": []},
                "decision": {"action": dec.action, "layer": dec.layer, "precedence": dec.precedence},
                "provenance": r.get("provenance") or {},
            }
            line = json.dumps(rec, ensure_ascii=False)
            f.write(line + "\n")
            h.update(line.encode())
            n += 1
            by_action[dec.action] = by_action.get(dec.action, 0) + 1
    meta = {
        "schema": "ir_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rules": n,
        "ir_digest": h.hexdigest(),
        "scope": "full" if full else "hierarchy_focus_services",
        "file": path.name,
        "by_action": by_action,
    }
    (out_dir / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def build_ir_streaming_full(canon_dir: Path, graph: EntityGraph, out_dir: Path) -> dict:
    """Full IR streaming from canonical jsonl."""
    out_dir.mkdir(parents=True, exist_ok=True)
    sid_to_provider: dict[str, str] = {}
    for s in graph.services.values():
        if s.provider:
            sid_to_provider[s.id] = s.provider
            if s.body_service_id:
                sid_to_provider[s.body_service_id] = s.provider
    rid_to_svcs: dict[str, list[str]] = defaultdict(list)
    mem_path = canon_dir / "service_rules.jsonl"
    if mem_path.exists():
        with mem_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                m = json.loads(line)
                rid_to_svcs[m["rule_id"]].append(m["service"])
    h = sha256()
    n = 0
    by_action: dict[str, int] = {}
    rules_path = canon_dir / "rules.jsonl"
    out_path = out_dir / "rules_v2_full.jsonl"
    with rules_path.open(encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rid = r["id"]
            svcs = rid_to_svcs.get(rid) or ["unknown"]
            primary = svcs[0]
            cat = (r.get("classification") or {}).get("category") or "other"
            dec = decide_for_service(primary, str(cat))
            rec = {
                "schema": "ir_v2",
                "rule": {"id": rid, "type": r.get("type"), "value": r.get("value"), "identity_key": r.get("identity_key")},
                "entity": {"provider": sid_to_provider.get(primary), "services": svcs[:32], "groups": []},
                "view": {"aggregates": []},
                "decision": {"action": dec.action, "layer": dec.layer, "precedence": dec.precedence},
                "provenance": r.get("provenance") or {},
            }
            out_line = json.dumps(rec, ensure_ascii=False)
            fout.write(out_line + "\n")
            h.update(out_line.encode())
            n += 1
            by_action[dec.action] = by_action.get(dec.action, 0) + 1
    meta = {
        "schema": "ir_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rules": n,
        "ir_digest": h.hexdigest(),
        "scope": "full",
        "file": "rules_v2_full.jsonl",
        "by_action": by_action,
    }
    (out_dir / "manifest_full.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta
