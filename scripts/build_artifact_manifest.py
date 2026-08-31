#!/usr/bin/env python3
"""V2.1 Artifact Manifest — truth layer (digests)."""
from __future__ import annotations

import fnmatch
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "config" / "artifact_layout.yaml"
OUT = ROOT / "reports" / "artifact_manifest.json"
DEC = ROOT / "generated" / "routing" / "decisions.meta.json"
IR = ROOT / "generated" / "ir" / "manifest.json"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    layout = yaml.safe_load(LAYOUT.read_text(encoding="utf-8")) if LAYOUT.exists() else {}
    globs = layout.get("release_globs") or []
    max_mb = float(((layout.get("policy") or {}).get("git") or {}).get("max_file_mb") or 5)
    artifacts = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        size = p.stat().st_size
        matched = any(fnmatch.fnmatch(rel, g) for g in globs)
        over = size >= max_mb * 1024 * 1024
        if not matched and not over:
            continue
        if size > 80 * 1024 * 1024:
            continue
        try:
            digest = sha256_file(p)
        except OSError:
            continue
        artifacts.append({"path": rel, "bytes": size, "sha256": digest, "channel": "release_preferred" if matched or over else "git"})
    meta = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "truth_layer": "artifact_manifest",
        "distribution_note": "Release is carrier only",
        "layout_version": layout.get("version"),
        "artifact_count": len(artifacts),
        "artifacts": sorted(artifacts, key=lambda x: -x["bytes"])[:500],
    }
    if DEC.exists():
        try:
            meta["decision_meta"] = json.loads(DEC.read_text(encoding="utf-8"))
        except Exception:
            pass
    if IR.exists():
        try:
            meta["ir_meta"] = json.loads(IR.read_text(encoding="utf-8"))
        except Exception:
            pass
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[artifact_manifest] count={len(artifacts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
