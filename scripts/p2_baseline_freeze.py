#!/usr/bin/env python3
"""P2.0 Baseline Freeze — write-only reports/baseline/. Does not change pipeline."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "baseline"


def sha256_file(p: Path):
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    n = 0
    with p.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                n += 1
    return n


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    commit = git_sha()
    services = sorted(
        p.stem for p in (ROOT / "database" / "services").glob("*.yaml") if not p.name.startswith("example")
    )
    service_stats = {}
    total_rules = 0
    for sid in services:
        p = ROOT / "database" / "services" / f"{sid}.yaml"
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            doc = {}
        n = len(doc.get("rules") or [])
        if n == 0:
            n = count_lines(ROOT / "database" / "domains" / f"{sid}.txt")
            n += count_lines(ROOT / "database" / "domains" / f"{sid}.exact.txt")
        service_stats[sid] = {"rules_or_sidecar_lines": n, "category": doc.get("category"), "sha256": sha256_file(p)}
        total_rules += n

    reg = {}
    rp = ROOT / "sources" / "registry.yaml"
    if rp.exists():
        reg_doc = yaml.safe_load(rp.read_text(encoding="utf-8")) or {}
        srcs = reg_doc.get("sources") or []
        reg = {"count": len(srcs), "ids": [s.get("id") for s in srcs if isinstance(s, dict)], "registry_sha256": sha256_file(rp)}

    large = {}
    for rel in (
        "database/geosite/direct.txt",
        "database/geosite/proxy.txt",
        "generated/geosite/direct.txt",
        "generated/geosite/proxy.txt",
        "generated/routing/decisions.jsonl",
        "generated/ir/rules.jsonl",
    ):
        p = ROOT / rel
        if p.exists():
            large[rel] = {"bytes": p.stat().st_size, "lines": count_lines(p) if p.suffix in (".txt", ".jsonl", ".list") else None, "sha256": sha256_file(p)}

    clients = {}
    gen = ROOT / "generated"
    if gen.exists():
        for d in sorted(gen.iterdir()):
            if not d.is_dir() or d.name.startswith("_"):
                continue
            files = [f for f in d.rglob("*") if f.is_file()]
            clients[d.name] = {"files": len(files), "bytes": sum(f.stat().st_size for f in files)}

    decision = None
    dm = ROOT / "generated" / "routing" / "decisions.meta.json"
    if dm.exists():
        try:
            decision = json.loads(dm.read_text(encoding="utf-8"))
        except Exception:
            decision = {"error": "parse"}
    ir = None
    im = ROOT / "generated" / "ir" / "manifest.json"
    if im.exists():
        try:
            ir = json.loads(im.read_text(encoding="utf-8"))
        except Exception:
            ir = {"error": "parse"}

    manifest = {
        "freeze_id": f"p2-baseline-{commit[:12]}",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "services": len(services),
        "total_rules_or_sidecar_lines": total_rules,
        "sources": reg.get("count"),
        "decision": decision,
        "universal_ir": ir,
        "client_dirs": clients,
        "large_paths": {k: {"bytes": v["bytes"], "lines": v.get("lines")} for k, v in large.items()},
        "known": {
            "service_builders_use_rule_loader": True,
            "decision_ssot_exists": dm.exists(),
            "universal_ir_exists": im.exists(),
            "note": "Baseline before V2.1; pipeline not modified",
        },
    }
    (OUT / "baseline_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "baseline_services.json").write_text(json.dumps(service_stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "baseline_sources.json").write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "baseline_artifacts.json").write_text(json.dumps({"large": large, "clients": clients}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "baseline_metrics.json").write_text(
        json.dumps(
            {
                "git_commit": commit,
                "services": len(services),
                "total_rules_or_sidecar_lines": total_rules,
                "client_file_count": sum(c["files"] for c in clients.values()),
                "client_bytes": sum(c["bytes"] for c in clients.values()),
                "large_bytes": sum(v["bytes"] for v in large.values()),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[p2_baseline_freeze] commit={commit[:12]} services={len(services)} rules~={total_rules}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
