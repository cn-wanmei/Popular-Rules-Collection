"""Semantic IR 2.0 — stable semantic contract between Canonical and adapters."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.canonical.store import load_rules, load_memberships
from src.engine.hierarchy.resolver import load_hierarchy
from src.engine.decision.engine import decide_batch


def build_ir(canonical_dir: Path, hierarchy_dir: Path, out_dir: Path) -> dict[str, Any]:
    canonical_dir = Path(canonical_dir)
    hierarchy_dir = Path(hierarchy_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rules = list(load_rules(canonical_dir).values())
    memberships = load_memberships(canonical_dir)
    hier = load_hierarchy(hierarchy_dir)
    decisions = decide_batch(rules, memberships)

    entities = {
        "services": sorted(hier.get("services", {}).keys()),
        "groups": sorted(hier.get("groups", {}).keys()),
        "aggregates": sorted(hier.get("aggregates", {}).keys()),
    }
    ir = {
        "schema": "semantic_ir_v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "engine_version": "1.0.1",
        "v2_runtime_dependency": 0,
        "entities": entities,
        "views": {
            "services": hier.get("services", {}),
            "groups": hier.get("groups", {}),
            "aggregates": hier.get("aggregates", {}),
        },
        "rules": [
            {
                "id": r["id"],
                "type": r["type"],
                "value": r["value"],
                "identity_key": r.get("identity_key"),
                "classification": r.get("classification"),
                "provenance": r.get("provenance"),
            }
            for r in sorted(rules, key=lambda x: x["id"])
        ],
        "decisions": decisions,
        "stats": {
            "rules": len(rules),
            "services": len(entities["services"]),
            "groups": len(entities["groups"]),
            "aggregates": len(entities["aggregates"]),
            "decisions": len(decisions),
        },
    }

    (out_dir / "ir.json").write_text(json.dumps(ir, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (out_dir / "decisions.jsonl").open("w", encoding="utf-8") as f:
        for d in decisions:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    manifest = {"schema": "semantic_ir_manifest_v2", "generated_at": ir["generated_at"], "stats": ir["stats"], "v2_runtime_dependency": 0}
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest
