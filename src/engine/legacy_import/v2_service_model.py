"""Load config/service_model into EntityGraph."""
from __future__ import annotations
from pathlib import Path
import yaml
from src.engine.core.models.entity import AggregateView, EntityGraph, Group, Provider, Service

def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def load_entity_graph(sm_dir: Path) -> EntityGraph:
    g = EntityGraph()
    for pid, p in (_load(sm_dir / "providers.yaml").get("providers") or {}).items():
        p = p or {}
        g.providers[pid] = Provider(id=pid, display_name=p.get("display_name") or pid, meta=p)
    for sid, s in (_load(sm_dir / "services.yaml").get("services") or {}).items():
        s = s or {}
        body = None
        br = s.get("body_ref") or {}
        if isinstance(br, dict) and br.get("id"):
            body = str(br["id"])
        elif s.get("legacy_body"):
            body = str(s["legacy_body"])
        elif sid.endswith("-core"):
            body = sid[: -len("-core")]
        g.services[sid] = Service(id=sid, provider=s.get("provider"), display_name=s.get("display_name") or sid, body_service_id=body, meta=s)
    for gid, gr in (_load(sm_dir / "groups.yaml").get("groups") or {}).items():
        gr = gr or {}
        g.groups[gid] = Group(id=gid, members=list(gr.get("members") or []), meta=gr)
    for aid, a in (_load(sm_dir / "memberships.yaml").get("aggregates") or {}).items():
        a = a or {}
        g.aggregates[aid] = AggregateView(id=aid, members=list(a.get("members") or []), exclude=list(a.get("exclude") or []), meta=a)
    for al, spec in (_load(sm_dir / "aliases.yaml").get("aliases") or {}).items():
        can = (spec or {}).get("canonical")
        if can:
            g.aliases[al] = str(can)
    return g
