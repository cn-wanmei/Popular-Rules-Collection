"""RC + Cutover + publish to generated/ (public projection)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ARTIFACT_GLOBS = ("*.list", "*.yaml", "*.yml", "*.json", "*.conf", "*.txt")


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
    gates = {
        "golden_l1_l7": bool(golden.get("pass")),
        "differential_rules_match": bool(diff.get("all_rules_match")),
        "differential_sha_match": bool(diff.get("all_sha_match", diff.get("all_rules_match"))),
        "canonical_rules": int(canon.get("unique_rules") or 0) > 0,
        "ir_rules": int(ir.get("rules") or 0) > 0,
        "clients_ge_7": len(clients) >= 7,
        "clients": clients,
    }
    hard_ok = all([gates["golden_l1_l7"], gates["differential_rules_match"], gates["canonical_rules"], gates["ir_rules"], gates["clients_ge_7"]])
    status = "RC_READY" if hard_ok else "BLOCKED"
    doc = {
        "product_version": version,
        "engine_codename": "v3",
        "schema": "cutover_manifest_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "release_channel": "rc" if status == "RC_READY" else "blocked",
        "rc_announced": status == "RC_READY",
        "production_cutover": False,
        "engine_outputs": "data/generated/",
        "production_tree": "generated/",
        "gates": gates,
        "cutover_checklist": [
            "G0-G18 layout/naming/import gates",
            "golden_l1_l7 pass",
            "differential rules+sha match",
            "full IR built",
            "7 client artifacts non-empty",
            "publish dry-run all extensions",
            "subscription smoke test",
            "human approval → production_cutover=true",
        ],
        "rollback": "Point production manifest to previous release_id artifacts; do not rebuild",
    }
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "CUTOVER_MANIFEST.json").write_text(json.dumps(doc, indent=2) + "\n")
    rel = root / "reports" / "release"
    rel.mkdir(parents=True, exist_ok=True)
    (rel / "CUTOVER_MANIFEST.json").write_text(json.dumps(doc, indent=2) + "\n")
    return doc


def publish_artifacts_to_production(root: Path, dry_run: bool = False) -> dict:
    src_root = root / "data" / "generated" / "artifacts"
    prod = root / "generated"
    copied: dict[str, int] = {}
    skipped_empty: list[str] = []
    if not src_root.is_dir():
        return {"copied": copied, "ok": False, "error": "missing data/generated/artifacts"}
    for client_dir in sorted(src_root.iterdir()):
        if not client_dir.is_dir():
            continue
        dest = prod / client_dir.name
        if not dry_run:
            dest.mkdir(parents=True, exist_ok=True)
        n = 0
        seen: set[str] = set()
        for pattern in ARTIFACT_GLOBS:
            for f in client_dir.glob(pattern):
                if f.name in seen:
                    continue
                seen.add(f.name)
                text = f.read_text(encoding="utf-8")
                out = dest / f.name
                if not text.strip():
                    if out.exists() and out.stat().st_size > 0:
                        skipped_empty.append(f"{client_dir.name}/{f.name}")
                        continue
                if not dry_run:
                    out.write_text(text, encoding="utf-8")
                n += 1
        copied[client_dir.name] = n
    return {"copied": copied, "skipped_empty_preserved_prod": skipped_empty, "ok": True, "dry_run": dry_run}
