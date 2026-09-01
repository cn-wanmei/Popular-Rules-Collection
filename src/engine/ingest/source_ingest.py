"""Source Ingest from Snapshot — V2-runtime-free."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from src.engine.ingest.rule_parser import iter_rules


LARGE_SERVICES = {"adblock", "proxy", "china", "gfw"}


class IngestError(Exception):
    """Hard failure during ingest — never silently dropped."""


def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise IngestError(f"Failed to parse YAML {path}: {e}") from e


def _structured_service_files(sources_root: Path) -> list[Path]:
    """Accept both sources/services/*.yaml and a direct sources/*.yaml layout."""
    nested = sources_root / "services"
    files = list(nested.glob("*.yaml")) if nested.is_dir() else []
    files.extend(sources_root.glob("*.yaml"))
    return sorted(set(files))


def _ingest_structured_services(
    sources_root: Path,
    records: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    *,
    skip_large: bool = False,
) -> int:
    count = 0
    for p in _structured_service_files(sources_root):
        try:
            doc = _load_yaml(p)
            if not isinstance(doc, dict):
                errors.append({"path": str(p), "error": "not a mapping"})
                continue
            sid = str(doc.get("id") or p.stem)
            if skip_large and sid in LARGE_SERVICES:
                continue
            cat = str(doc.get("category") or "other")
            sources = doc.get("source") or []
            for r in doc.get("rules") or []:
                if not isinstance(r, dict):
                    errors.append({"path": str(p), "error": "rule not dict", "raw": r})
                    continue
                typ, val = r.get("type"), r.get("value")
                if not typ or not val:
                    errors.append({"path": str(p), "error": "missing type or value", "rule": r})
                    continue
                records.append({
                    "service": sid,
                    "type": str(typ),
                    "value": str(val),
                    "category": cat,
                    "provenance": {
                        "sources": r.get("sources") or sources,
                        "file": str(p.relative_to(sources_root.parent)),
                    },
                })
                count += 1
        except IngestError as e:
            errors.append({"path": str(p), "error": str(e)})
    return count


def _resolve_collected_path(snapshot_dir: Path, local_rel: str) -> Path:
    """Resolve collector paths after Snapshot adds its own sources/ boundary."""
    rel = Path(local_rel)
    stripped = str(rel).removeprefix("sources/") if str(rel).startswith("sources/") else str(rel)
    candidates = [
        snapshot_dir / str(rel),
        snapshot_dir / "sources" / str(rel),
        snapshot_dir / "sources" / stripped,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[-1]


def _ingest_collected_snapshot(
    snapshot_dir: Path,
    records: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    *,
    skip_large: bool = False,
) -> int:
    """Parse a frozen collected snapshot under sources/manifests + collected files."""
    sources_root = snapshot_dir / "sources"
    manifests_dir = sources_root / "manifests"
    if not manifests_dir.is_dir() or not sources_root.is_dir():
        return 0

    count = 0
    for manifest_path in sorted(manifests_dir.glob("*.json")):
        if manifest_path.name == "_day.json":
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append({"path": str(manifest_path), "error": f"invalid collection manifest: {e}"})
            continue
        source_id = str(manifest.get("source") or manifest_path.stem)
        for entry in manifest.get("files") or []:
            if entry.get("status") != "ok":
                continue
            name = str(entry.get("name") or "")
            service = str(entry.get("service") or Path(name).stem).lower()
            if skip_large and service in LARGE_SERVICES:
                continue
            local_rel = str(entry.get("local") or f"sources/{source_id}/{name}")
            path = _resolve_collected_path(snapshot_dir, local_rel)
            if not path.is_file():
                errors.append({"path": str(path), "error": "collected file missing from snapshot", "local": local_rel})
                continue
            try:
                parsed = list(iter_rules(path))
            except OSError as e:
                errors.append({"path": str(path), "error": str(e)})
                continue
            for typ, value in parsed:
                records.append({
                    "service": service,
                    "type": typ,
                    "value": value,
                    "category": "other",
                    "provenance": {
                        "sources": [{"id": source_id}],
                        "file": str(path.relative_to(snapshot_dir)),
                        **({"url": entry.get("url")} if entry.get("url") else {}),
                    },
                })
                count += 1
            if not parsed:
                errors.append({"path": str(path), "error": "no recognized rules", "service": service, "source": source_id})
    return count


def ingest_snapshot(snapshot_dir: Path, *, skip_large: bool = False) -> dict[str, Any]:
    """Ingest a frozen Source Snapshot into structured records."""
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
    structured_count = _ingest_structured_services(
        sources_root, records, errors, skip_large=skip_large
    )
    collected_count = _ingest_collected_snapshot(
        snapshot_dir, records, errors, skip_large=skip_large
    )
    if not records:
        raise IngestError("Snapshot contains no recognizable rule records")

    return {
        "snapshot_id": manifest.get("snapshot_id") or snapshot_dir.name,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "manifest": manifest,
        "records": records,
        "errors": errors,
        "stats": {
            "records": len(records),
            "errors": len(errors),
            "structured_service_records": structured_count,
            "collected_raw_records": collected_count,
        },
    }
