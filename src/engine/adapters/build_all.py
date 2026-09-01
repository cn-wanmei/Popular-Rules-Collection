"""Build 7 client artifacts under data/generated/artifacts/."""
from __future__ import annotations
import json
from pathlib import Path
from src.engine.adapters.base import format_line
from src.engine.core.models.entity import EntityGraph
from src.engine.hierarchy.resolver import body_service_id, expand_members

CLIENTS = ("mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon")

def build_service_lists(rules, memberships, graph: EntityGraph, artifacts_dir: Path) -> dict:
    stats = {}
    for client in CLIENTS:
        cdir = artifacts_dir / client
        cdir.mkdir(parents=True, exist_ok=True)
        n_files = 0
        for vid, agg in graph.aggregates.items():
            members = expand_members(graph, agg.members, agg.exclude)
            lines, seen = [], set()
            for mid in members:
                body = body_service_id(graph, mid)
                for rid in memberships.get(body) or memberships.get(mid) or []:
                    r = rules.get(rid)
                    if not r: continue
                    line = format_line(client, r.get("type") or "", r.get("value") or "")
                    if line and line not in seen:
                        seen.add(line); lines.append(line)
            (cdir / f"{vid}.list").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
            n_files += 1
        for body in ("google", "apple", "microsoft", "tencent", "alibaba", "baidu"):
            lines, seen = [], set()
            for rid in memberships.get(body) or []:
                r = rules.get(rid)
                if not r: continue
                line = format_line(client, r.get("type") or "", r.get("value") or "")
                if line and line not in seen:
                    seen.add(line); lines.append(line)
            if lines:
                (cdir / f"{body}.list").write_text("\n".join(lines) + "\n", encoding="utf-8")
                n_files += 1
        stats[client] = {"files": n_files}
    (artifacts_dir / "manifest.json").write_text(json.dumps({"clients": stats}, indent=2) + "\n")
    return stats
