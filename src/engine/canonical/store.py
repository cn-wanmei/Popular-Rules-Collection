"""Canonical Rule Store v1 — independent of database/services and V2 models.

Input: ingest result (from Source Snapshot)
Output: data/.../canonical/
    rules.jsonl
    memberships.jsonl
    errors.jsonl
    manifest.json

Never silently drop rules. Every invalid record goes to errors.jsonl.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.core.models.rule import Rule, full_rule_id, identity_key


def build_canonical(
    ingest_result: dict[str, Any],
    out_dir: Path,
    *,
    schema: str = "canonical_store_v1",
) -> dict[str, Any]:
    """
    Build Canonical SSOT from ingest payload.
    Raises nothing for individual bad rules — records them.
    Returns manifest.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    seen: set[str] = set()
    rules: list[Rule] = []
    memberships: list[dict[str, str]] = []
    errors: list[dict[str, Any]] = list(ingest_result.get("errors") or [])

    for rec in ingest_result.get("records") or []:
        typ = rec.get("type")
        val = rec.get("value")
        sid = rec.get("service")
        if not typ or not val:
            errors.append({
                "stage": "canonical",
                "error": "missing type or value",
                "record": rec,
            })
            continue
        try:
            rid = full_rule_id(str(typ), str(val))
            ik = identity_key(str(typ), str(val))
            if rid not in seen:
                seen.add(rid)
                rule = Rule(
                    id=rid,
                    type=str(typ),
                    value=str(val),
                    identity_key=ik,
                    provenance=rec.get("provenance") or {},
                    classification={"category": rec.get("category") or "other"},
                    memberships=[],
                )
                rules.append(rule)
            # always record membership
            if sid:
                memberships.append({
                    "rule_id": rid,
                    "entity": str(sid),
                    "relation": "member",  # future: exclusive / dependency / shared
                })
        except Exception as e:
            errors.append({
                "stage": "canonical",
                "error": str(e),
                "record": rec,
            })

    # write artifacts
    rules_path = out_dir / "rules.jsonl"
    mem_path = out_dir / "memberships.jsonl"
    err_path = out_dir / "errors.jsonl"

    with rules_path.open("w", encoding="utf-8") as fr:
        for r in rules:
            fr.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")

    with mem_path.open("w", encoding="utf-8") as fm:
        for m in memberships:
            fm.write(json.dumps(m, ensure_ascii=False) + "\n")

    with err_path.open("w", encoding="utf-8") as fe:
        for e in errors:
            fe.write(json.dumps(e, ensure_ascii=False) + "\n")

    manifest = {
        "schema": schema,
        "engine_version": "1.0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_id": ingest_result.get("snapshot_id"),
        "unique_rules": len(rules),
        "memberships": len(memberships),
        "errors": len(errors),
        "source": "engine_ingest_snapshot",  # never "v2_database_services_import"
        "v2_runtime_dependency": 0,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def load_rules(out_dir: Path) -> dict[str, dict]:
    path = Path(out_dir) / "rules.jsonl"
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


def load_memberships(out_dir: Path) -> dict[str, list[str]]:
    """entity → list of rule_ids"""
    path = Path(out_dir) / "memberships.jsonl"
    out: dict[str, list[str]] = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = json.loads(line)
            out.setdefault(m["entity"], []).append(m["rule_id"])
    return out
