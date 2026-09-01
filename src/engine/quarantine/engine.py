"""Source quarantine observe mode."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
VALID_STATES = ("fetched", "quarantined", "validated", "accepted", "rejected")

def load_state(path: Path) -> dict:
    if not path.exists(): return {"sources": {}}
    return json.loads(path.read_text(encoding="utf-8"))

def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n")

def set_status(state_path: Path, source_id: str, status: str, reason: str = "", meta: dict | None = None) -> dict:
    if status not in VALID_STATES: raise ValueError(status)
    state = load_state(state_path)
    sources = state.setdefault("sources", {})
    entry = sources.get(source_id) or {}
    entry.update({"status": status, "reason": reason, "updated_at": datetime.now(timezone.utc).isoformat(), "meta": meta or entry.get("meta") or {}})
    sources[source_id] = entry
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_state(state_path, state)
    return entry

def evaluate_health_yaml(root: Path, state_path: Path) -> dict:
    health = root / "sources" / "health.yaml"
    report = {"evaluated": 0, "quarantined": 0, "accepted": 0}
    if not health.exists(): return report
    try:
        import yaml
        doc = yaml.safe_load(health.read_text(encoding="utf-8")) or {}
    except Exception:
        return report
    items = doc if isinstance(doc, list) else (doc.get("sources") or doc.get("health") or [])
    if isinstance(items, dict):
        items = [{"id": k, **(v or {})} for k, v in items.items()]
    for item in items:
        if not isinstance(item, dict): continue
        sid = str(item.get("id") or item.get("name") or item.get("source") or "")
        if not sid: continue
        report["evaluated"] += 1
        ok = item.get("ok", item.get("healthy", item.get("status") == "ok"))
        if ok is False or item.get("status") in ("error", "fail", "blocked"):
            set_status(state_path, sid, "quarantined", reason=str(item.get("error") or "health_fail")); report["quarantined"] += 1
        else:
            set_status(state_path, sid, "accepted", reason="health_ok"); report["accepted"] += 1
    return report
