"""Content-addressable registration and integrity verification for Run artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from src.engine.cas.store import put_file, read_bytes


def register_run(run_dir: Path, cas_root: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    cas_root = Path(cas_root)
    objects: dict[str, str] = {}
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file() or path.name.endswith(".tmp"):
            continue
        if path.relative_to(run_dir).as_posix() == "cas-manifest.json":
            continue
        digest = put_file(path, cas_root)
        objects[str(path.relative_to(run_dir))] = digest
    manifest = {
        "schema": "run_cas_manifest_v1",
        "run_id": run_dir.name,
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
    mismatches: list[str] = []
    missing: list[str] = []
    for rel, digest in manifest.get("objects", {}).items():
        local = run_dir / rel
        if not local.is_file():
            missing.append(rel)
            continue
        if hashlib.sha256(local.read_bytes()).hexdigest() != digest:
            mismatches.append(rel)
        else:
            read_bytes(digest, cas_root)
    return {"verified": not missing and not mismatches, "missing": missing, "mismatches": mismatches, "object_count": len(manifest.get("objects", {}))}
