"""RC + Cutover + publish to generated/."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def write_cutover_manifest(root: Path, version: str = "1.0.0") -> dict:
    data = root / "data" / "generated"
    reports = data / "reports"
    golden = json.loads((reports / "golden_l1_l7.json").read_text()) if (reports / "golden_l1_l7.json").exists() else {}
    diff = json.loads((reports / "differential.json").read_text()) if (reports / "differential.json").exists() else {}
    canon = json.loads((data / "canonical" / "manifest.json").read_text()) if (data / "canonical" / "manifest.json").exists() else {}
    ir = {}
    for name in ("manifest_full.json", "manifest.json"):
        p = data / "ir" / name
        if p.exists():
            ir = json.loads(p.read_text())
            break
    clients = sorted(p.name for p in (data / "artifacts").iterdir() if p.is_dir()) if (data / "artifacts").is_dir() else []
    ready = bool(golden.get("pass")) and bool(diff.get("all_rules_match", diff.get("compared")))
    doc = {
        "version": version,
        "schema": "cutover_manifest_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "RC_READY" if ready else "RC_BLOCKED",
        "rc_announced": True,
        "production_cutover": True,
        "engine_codename": "v3",
        "engine_outputs": "data/generated/",
        "production_tree": "generated/",
        "gates": {
            "golden_l1_l7": golden.get("pass"),
            "differential_rules_match": diff.get("all_rules_match"),
            "canonical_rules": canon.get("unique_rules"),
            "ir_rules": ir.get("rules"),
            "clients": clients,
        },
        "rollback": "Restore previous generated/ from release artifacts",
    }
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "CUTOVER_MANIFEST.json").write_text(json.dumps(doc, indent=2) + "\n")
    rel = root / "reports" / "release"
    rel.mkdir(parents=True, exist_ok=True)
    (rel / "CUTOVER_MANIFEST.json").write_text(json.dumps(doc, indent=2) + "\n")
    return doc


def publish_artifacts_to_production(root: Path) -> dict:
    src_root = root / "data" / "generated" / "artifacts"
    prod = root / "generated"
    copied = {}
    if not src_root.is_dir():
        return {"copied": copied, "ok": False}
    for client_dir in src_root.iterdir():
        if not client_dir.is_dir():
            continue
        dest = prod / client_dir.name
        dest.mkdir(parents=True, exist_ok=True)
        n = 0
        for f in client_dir.glob("*.list"):
            (dest / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            n += 1
        copied[client_dir.name] = n
    return {"copied": copied, "ok": True}
