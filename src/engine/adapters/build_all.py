"""Parallel native client projections from Semantic IR / Canonical."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from src.engine.adapters.registry import CLIENTS, get_adapter
from src.engine.canonical.store import load_rules, load_memberships


def _build_client(client: str, meta: dict[str, str], rules: list[dict[str, Any]], memberships: dict[str, list[str]], artifacts_dir: Path) -> tuple[str, dict[str, Any]]:
    cdir = artifacts_dir / client
    cdir.mkdir(parents=True, exist_ok=True)
    render = get_adapter(client)
    rules_by_id = {r["id"]: r for r in rules}
    render(rules, cdir / f"aggregate{meta['ext']}")
    for entity in sorted(memberships):
        entity_rules = [rules_by_id[rid] for rid in memberships[entity] if rid in rules_by_id]
        if entity_rules:
            render(entity_rules, cdir / f"{entity}{meta['ext']}")
    return client, {"ext": meta["ext"], "files": len(list(cdir.glob(f"*{meta['ext']}")))}


def build_all_clients(canonical_dir: Path, artifacts_dir: Path, *, views: list[str] | None = None) -> dict[str, Any]:
    canonical_dir = Path(canonical_dir)
    artifacts_dir = Path(artifacts_dir)
    rules = sorted(load_rules(canonical_dir).values(), key=lambda r: r["id"])
    memberships = load_memberships(canonical_dir)
    report: dict[str, Any] = {"clients": {}, "views": {}, "v2_runtime_dependency": 0, "parallel": True}
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(CLIENTS))), thread_name_prefix="adapter") as pool:
        futures = [pool.submit(_build_client, client, meta, rules, memberships, artifacts_dir) for client, meta in CLIENTS.items()]
        for future in as_completed(futures):
            client, details = future.result()
            report["clients"][client] = details
    report["clients"] = {k: report["clients"][k] for k in sorted(report["clients"])}
    report["views"]["services"] = sorted(memberships.keys())
    report["views"]["aggregate"] = True
    (artifacts_dir / "build_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
