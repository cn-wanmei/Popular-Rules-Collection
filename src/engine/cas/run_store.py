"""Content-addressable registration and integrity verification for immutable Run evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from src.engine.cas.store import put_file, read_bytes

MUTABLE_RUN_FILES = {"run_manifest.json", "cas-manifest.json"}


def register_run(run_dir: Path, cas_root: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    cas_root = Path(cas_root)
    objects: dict[str, str] = {}
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file() or path.name.endswith(".tmp"):
            continue
        rel = path.relative_to(run_dir).as_posix()
        if rel in MUTABLE_RUN_FILES:
            continue
        digest = put_file(path, cas_root)
        objects[rel] = digest
    manifest = {
        "schema": "run_cas_manifest_v2",
        "run_id": run_dir.name,
        "mutable_files_excluded": sorted(MUTABLE_RUN_FILES),
        "object_count": len(objects),
        "objects": objects,
    }
    out = run_dir / "cas-manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest["manifest_sha256"] = hashlib.sha256(out.read_bytes()).hexdigest()
    return manifest


def verify_run(run_dir: Path, cas_root: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    manifest_path = run_dir / "cas-manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("Missing cas-manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest.get("objects"), dict) or not manifest.get("objects"):
        raise RuntimeError("CAS manifest contains no immutable objects")
    mismatches: list[str] = []
    missing: list[str] = []
    for rel, digest in manifest["objects"].items():
        local = run_dir / rel
        if not local.is_file():
            missing.append(rel)
            continue
        actual = hashlib.sha256(local.read_bytes()).hexdigest()
        if actual != digest:
            mismatches.append(rel)
            continue
        read_bytes(digest, cas_root)
    return {
        "verified": not missing and not mismatches,
        "missing": missing,
        "mismatches": mismatches,
        "object_count": len(manifest["objects"]),
    }
