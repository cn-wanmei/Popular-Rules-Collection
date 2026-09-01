"""Canonical Rule Store — streaming under data/generated/canonical/."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from src.engine.core.models.rule import identity_key


def _rule_id(typ: str, value: str) -> str:
    return hashlib.sha256(identity_key(typ, value).encode()).hexdigest()[:16]


def build_from_v2_services(services_dir: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    n_rules = n_mem = 0
    with (out_dir / "rules.jsonl").open("w", encoding="utf-8") as fr, (out_dir / "service_rules.jsonl").open("w", encoding="utf-8") as fm:
        for p in sorted(services_dir.glob("*.yaml")):
            if p.name.startswith("example"):
                continue
            try:
                doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            sid = doc.get("id") or p.stem
            sources = doc.get("source") or []
            cat = doc.get("category") or "other"
            for r in doc.get("rules") or []:
                if not isinstance(r, dict):
                    continue
                typ, val = r.get("type"), r.get("value")
                if not typ or not val:
                    continue
                typ, val = str(typ), str(val)
                rid = _rule_id(typ, val)
                if rid not in seen:
                    seen.add(rid)
                    fr.write(json.dumps({"id": rid, "type": typ, "value": val, "identity_key": identity_key(typ, val), "provenance": {"sources": r.get("sources") or sources}, "classification": {"category": cat}}, ensure_ascii=False) + "\n")
                    n_rules += 1
                fm.write(json.dumps({"service": sid, "rule_id": rid}, ensure_ascii=False) + "\n")
                n_mem += 1
    manifest = {"schema": "canonical_store_v1", "generated_at": datetime.now(timezone.utc).isoformat(), "unique_rules": n_rules, "memberships": n_mem, "source": "v2_database_services_import"}
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def load_memberships(out_dir: Path) -> dict[str, list[str]]:
    path = out_dir / "service_rules.jsonl"
    out: dict[str, list[str]] = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = json.loads(line)
            out.setdefault(m["service"], []).append(m["rule_id"])
    return out


def load_rules(out_dir: Path) -> dict[str, dict]:
    path = out_dir / "rules.jsonl"
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out[r["id"]] = r
    return out
