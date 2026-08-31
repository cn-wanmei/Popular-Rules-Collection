"""RC + Cutover Manifest."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def write_cutover_manifest(root: Path, version: str = "1.0.0") -> dict:
    data = root / "data" / "v3"
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
    clients = sorted([p.name for p in (data / "artifacts").iterdir() if p.is_dir()]) if (data / "artifacts").is_dir() else []
    ready = bool(golden.get("pass")) and bool(diff.get("all_rules_match", diff.get("compared")))
    doc = {
        "version": version,
        "schema": "cutover_manifest_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "RC_READY" if ready else "RC_BLOCKED",
        "production_cutover": False,
        "v2_role": "legacy_oracle_until_cutover_approved",
        "v3_outputs": "data/v3/",
        "gates": {
            "golden_l1_l7": golden.get("pass"),
            "differential_rules_match": diff.get("all_rules_match"),
            "canonical_rules": canon.get("unique_rules"),
            "ir_rules": ir.get("rules"),
            "ir_scope": ir.get("scope"),
            "clients": clients,
        },
        "cutover_checklist": [
            "golden_l1_l7 pass",
            "differential all_rules_match",
            "full IR built",
            "7 client artifacts present",
            "human approval for production_cutover=true",
            "compat URLs retained for one release cycle",
        ],
        "rollback": "Artifact rollback to last V2 generated/ release; do not rebuild from V3",
    }
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "CUTOVER_MANIFEST.json").write_text(json.dumps(doc, indent=2) + "\n")
    (root / "reports" / "v3").mkdir(parents=True, exist_ok=True)
    (root / "reports" / "v3" / "CUTOVER_MANIFEST.json").write_text(json.dumps(doc, indent=2) + "\n")
    return doc
