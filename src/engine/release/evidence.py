"""Release evidence helpers: lightweight SBOM and artifact retention metadata."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_sbom(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    files = []
    for p in sorted(run_dir.rglob("*")):
        if not p.is_file() or p.name in {"sbom.json"}:
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        files.append({"path": str(p.relative_to(run_dir)), "sha256": h, "size": p.stat().st_size})
    sbom = {"schema": "engine_sbom_v1", "generated_at": datetime.now(timezone.utc).isoformat(), "run_id": run_dir.name, "files": files}
    out = run_dir / "release" / "sbom.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(sbom, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return sbom


def retention_plan(runs_root: Path, keep: int = 10) -> dict[str, Any]:
    runs_root = Path(runs_root)
    runs = sorted([p for p in runs_root.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True) if runs_root.exists() else []
    keep = max(1, int(keep))
    return {"schema": "artifact_retention_v1", "keep": keep, "retain": [p.name for p in runs[:keep]], "eligible_for_deletion": [p.name for p in runs[keep:]]}
