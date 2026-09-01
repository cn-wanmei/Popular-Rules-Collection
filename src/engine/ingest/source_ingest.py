"""Source Ingest from Snapshot — V2-free.

Expected layout:
  data/snapshots/<snapshot_id>/
      ├── manifest.json
      └── sources/
          ├── services/          # optional structured service YAML
          ├── raw/               # optional raw upstream dumps
          └── registry.yaml      # optional registry snapshot
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


class IngestError(Exception):
    """Hard failure during ingest — never silently dropped."""


def _load_yaml(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
        return yaml.safe_load(text)
    except Exception as e:
        raise IngestError(f"Failed to parse YAML {path}: {e}") from e


def ingest_snapshot(snapshot_dir: Path) -> dict[str, Any]:
    """
    Ingest a frozen Source Snapshot.
    Returns a structured payload ready for Normalize / Canonical.
    Raises IngestError on any unrecoverable problem.
    """
    snapshot_dir = Path(snapshot_dir)
    if not snapshot_dir.is_dir():
        raise IngestError(f"Snapshot directory does not exist: {snapshot_dir}")

    manifest_path = snapshot_dir / "manifest.json"
    if not manifest_path.exists():
        raise IngestError(f"Missing manifest.json in {snapshot_dir}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise IngestError(f"Invalid manifest.json: {e}") from e

    sources_root = snapshot_dir / "sources"
    if not sources_root.is_dir():
        raise IngestError(f"Missing sources/ under {snapshot_dir}")

    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    # 1. Structured service YAMLs (if present)
    services_dir = sources_root / "services"
    if services_dir.is_dir():
        for p in sorted(services_dir.glob("*.yaml")):
            if p.name.startswith("example"):
                continue
            try:
                doc = _load_yaml(p)
                if not isinstance(doc, dict):
                    errors.append({"path": str(p), "error": "not a mapping"})
                    continue
                sid = doc.get("id") or p.stem
                cat = doc.get("category") or "other"
                sources = doc.get("source") or []
                for r in doc.get("rules") or []:
                    if not isinstance(r, dict):
                        errors.append({"path": str(p), "error": "rule not dict", "raw": r})
                        continue
                    typ = r.get("type")
                    val = r.get("value")
                    if not typ or not val:
                        errors.append({
                            "path": str(p),
                            "error": "missing type or value",
                            "rule": r,
                        })
                        continue
                    records.append({
                        "service": sid,
                        "type": str(typ),
                        "value": str(val),
                        "category": cat,
                        "provenance": {
                            "sources": r.get("sources") or sources,
                            "file": str(p.relative_to(snapshot_dir)),
                        },
                    })
            except IngestError as e:
                errors.append({"path": str(p), "error": str(e)})

    # 2. Registry snapshot (optional)
    registry_path = sources_root / "registry.yaml"
    if registry_path.exists():
        try:
            reg = _load_yaml(registry_path)
            # keep as metadata only for now
            manifest["registry_present"] = True
            manifest["registry_keys"] = list(reg.keys()) if isinstance(reg, dict) else []
        except IngestError as e:
            errors.append({"path": str(registry_path), "error": str(e)})

    result = {
        "snapshot_id": manifest.get("snapshot_id") or snapshot_dir.name,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "manifest": manifest,
        "records": records,
        "errors": errors,
        "stats": {
            "records": len(records),
            "errors": len(errors),
        },
    }
    return result
