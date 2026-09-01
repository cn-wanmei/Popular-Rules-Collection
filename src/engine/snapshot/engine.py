"""Immutable snapshots under data/generated/snapshots/."""
from __future__ import annotations
import hashlib, json, shutil
from datetime import datetime, timezone
from pathlib import Path

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def create_snapshot(root: Path, sources: list[Path], out_root: Path | None = None, label: str = "manual") -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snap_id = f"{ts}-{label}"
    out_root = out_root or (root / "data" / "generated" / "snapshots")
    dest = out_root / snap_id
    dest.mkdir(parents=True, exist_ok=True)
    entries = []
    for src in sources:
        if not src.exists() or not src.is_file(): continue
        target = dest / "files" / src.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        entries.append({"name": src.name, "sha256": _sha256_file(target), "bytes": target.stat().st_size})
    manifest = {"snapshot_id": snap_id, "created_at": datetime.now(timezone.utc).isoformat(), "label": label, "immutable": True, "files": entries, "file_count": len(entries)}
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (out_root / "LATEST").write_text(snap_id + "\n")
    return manifest

def snapshot_v2_oracle(root: Path) -> dict:
    candidates = [root / "reports" / "hierarchy" / "summary.json", root / "reports" / "hierarchy" / "golden.json", root / "generated" / "ir" / "manifest.json", root / "config" / "service_model" / "memberships.yaml", root / "config" / "service_model" / "services.yaml", root / "config" / "service_model" / "providers.yaml"]
    return create_snapshot(root, [p for p in candidates if p.exists()], label="v2-oracle")
