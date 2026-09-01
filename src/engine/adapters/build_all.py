"""Build all 7 native client artifacts from Canonical (P0-6 / P0-7)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.engine.adapters.registry import CLIENTS, get_adapter
from src.engine.canonical.store import load_rules, load_memberships


def build_all_clients(
    canonical_dir: Path,
    artifacts_dir: Path,
    *,
    views: list[str] | None = None,
) -> dict[str, Any]:
    """
    Produce native-format artifacts for every registered client.
    Also emits simple Service / Aggregate views when memberships exist.
    """
    canonical_dir = Path(canonical_dir)
    artifacts_dir = Path(artifacts_dir)
    rules = load_rules(canonical_dir)
    memberships = load_memberships(canonical_dir)

    # default view = all rules (aggregate)
    all_rules = list(rules.values())
    report = {"clients": {}, "views": {}, "v2_runtime_dependency": 0}

    for client, meta in CLIENTS.items():
        cdir = artifacts_dir / client
        cdir.mkdir(parents=True, exist_ok=True)
        render = get_adapter(client)
        # aggregate view
        out = cdir / f"aggregate{meta['ext']}"
        render(all_rules, out)
        # per-service views
        for entity, rids in memberships.items():
            entity_rules = [rules[rid] for rid in rids if rid in rules]
            if entity_rules:
                eout = cdir / f"{entity}{meta['ext']}"
                render(entity_rules, eout)
        report["clients"][client] = {
            "ext": meta["ext"],
            "files": len(list(cdir.glob(f"*{meta['ext']}")))
        }

    report["views"]["services"] = list(memberships.keys())
    report["views"]["aggregate"] = True
    (artifacts_dir / "build_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report
