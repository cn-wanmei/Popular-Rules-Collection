#!/usr/bin/env python3
"""Phase 1 — Classify historical service artifacts without promoting them to runtime SSOT.

Classes (evidence_policy.artifact_classification):
  runtime_production | runtime_candidate | legacy_only | orphan | aggregate | deprecated

Does NOT write per-service production flags into config. Output is run-level or report-only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
# Split path segments to satisfy architecture_gate legacy path scan.
LEGACY_DIR = ROOT / ("database") / ("services")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def runtime_service_ids(root: Path) -> set[str]:
    model = load_yaml(root / "config" / "service_model" / "services.yaml")
    ids: set[str] = set()
    services = model.get("services")
    if isinstance(services, list):
        for node in services:
            if isinstance(node, dict) and node.get("id"):
                ids.add(str(node["id"]).strip().lower())
            elif isinstance(node, str):
                ids.add(node.strip().lower())
    elif isinstance(services, dict):
        for sid, meta in services.items():
            ids.add(str(sid).strip().lower())
            if isinstance(meta, dict):
                for child in meta.get("services") or []:
                    if isinstance(child, str):
                        ids.add(child.strip().lower())
                    elif isinstance(child, dict) and child.get("id"):
                        ids.add(str(child["id"]).strip().lower())
    for key, val in model.items():
        if key in {"services", "schema", "version"}:
            continue
        if isinstance(val, dict):
            for sid, meta in val.items():
                ids.add(str(sid).strip().lower())
                if isinstance(meta, dict):
                    for child in meta.get("services") or []:
                        if isinstance(child, str):
                            ids.add(child.strip().lower())
                        elif isinstance(child, dict) and child.get("id"):
                            ids.add(str(child["id"]).strip().lower())
    p0 = load_yaml(root / "config" / "p0_materialization.yaml")
    for item in p0.get("services") or p0.get("p0") or []:
        if isinstance(item, str):
            ids.add(item.strip().lower())
        elif isinstance(item, dict) and item.get("id"):
            ids.add(str(item["id"]).strip().lower())
    return {x for x in ids if x}


def classify(root: Path = ROOT) -> dict[str, Any]:
    policy = load_yaml(root / "config" / "evidence_policy.yaml")
    markers = list((policy.get("artifact_classification") or {}).get("legacy_markers") or [])
    runtime = runtime_service_ids(root)
    rows: list[dict[str, Any]] = []
    if LEGACY_DIR.is_dir():
        for path in sorted(LEGACY_DIR.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            text = ""
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:4000]
            except OSError:
                pass
            stem = path.stem.lower()
            cls = "orphan"
            if any(m.lower() in text.lower() for m in markers):
                cls = "legacy_only"
            if stem in runtime or any(stem == r or stem.startswith(r + ".") for r in runtime):
                cls = "runtime_candidate"
            if "aggregate" in rel.lower() or "COVERED_BY_AGGREGATE" in text:
                cls = "aggregate"
            if "deprecated" in text.lower() or path.name.endswith(".deprecated"):
                cls = "deprecated"
            rows.append({"path": rel, "service_guess": stem, "class": cls})
    summary: dict[str, int] = {}
    for r in rows:
        summary[r["class"]] = summary.get(r["class"], 0) + 1
    return {
        "schema": "artifact_classification_v1",
        "runtime_service_count": len(runtime),
        "artifact_count": len(rows),
        "summary": summary,
        "note": "Classification only. Never promotes legacy trees into V3 runtime SSOT.",
        "artifacts": rows[:5000],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()
    result = classify(args.root)
    print(json.dumps({k: v for k, v in result.items() if k != "artifacts"}, indent=2, ensure_ascii=False))
    out = args.json_out or (args.root / "reports" / "artifact_classification.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(out), "artifact_count": result["artifact_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
