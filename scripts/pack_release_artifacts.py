#!/usr/bin/env python3
"""V2.1 Pack release-preferred paths into dist/release_bundle/."""
from __future__ import annotations

import fnmatch
import hashlib
import json
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "config" / "artifact_layout.yaml"
DIST = ROOT / "dist" / "release_bundle"
REPORT = ROOT / "reports" / "release_bundle.json"


def main() -> int:
    layout = yaml.safe_load(LAYOUT.read_text(encoding="utf-8")) if LAYOUT.exists() else {}
    globs = layout.get("release_globs") or []
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)
    files = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if any(fnmatch.fnmatch(rel, g) for g in globs):
            files.append(p)
    tar_path = DIST / "large_artifacts.tar"
    with tarfile.open(tar_path, "w") as tar:
        for p in files:
            tar.add(p, arcname=p.relative_to(ROOT).as_posix())
    h = hashlib.sha256()
    with tar_path.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "tar": str(tar_path.relative_to(ROOT)),
        "tar_bytes": tar_path.stat().st_size,
        "tar_sha256": h.hexdigest(),
        "note": "Carrier only; truth is reports/artifact_manifest.json",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[pack_release] files={len(files)} tar_mb={report['tar_bytes']/1e6:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
