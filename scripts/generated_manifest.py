#!/usr/bin/env python3
"""Build one deterministic inventory for every generated distribution artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT_DIRS = ("mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon")
NETWORK_DIRS = ("network", "geosite", "geoip", "provider", "asn", "ip", "policies", "mmdb")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rule_count(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    count = 0
    for line in text.splitlines():
        value = line.strip()
        if not value or value.startswith(("#", "---", "payload")):
            continue
        if value.startswith("- ") or any(token in value for token in ("DOMAIN", "IP-CIDR", "DOMAIN-SUFFIX")):
            count += 1
        elif path.suffix == ".list":
            count += 1
    return count


def classify(top: str) -> str:
    if top in CLIENT_DIRS:
        return "client_rules"
    if top in NETWORK_DIRS:
        return "network_dataset"
    if top == "_promotion":
        return "promotion_metadata"
    return "other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT / "generated")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()

    generated = args.root if args.root.is_absolute() else ROOT / args.root
    generated.mkdir(parents=True, exist_ok=True)
    out = args.output or (generated / "manifest.json")
    if not out.is_absolute():
        out = ROOT / out

    now = datetime.now(timezone.utc).isoformat()
    files = []
    for path in sorted(p for p in generated.rglob("*") if p.is_file()):
        rel = path.relative_to(generated).as_posix()
        if rel in {"manifest.json", "network_manifest.json"}:
            continue
        top = rel.split("/", 1)[0]
        kind = classify(top)
        item = {
            "kind": kind,
            "scope": top,
            "file": rel,
            "sha256": sha256_file(path),
            "size": path.stat().st_size,
        }
        if kind in {"client_rules", "network_dataset"}:
            item["rule_count"] = rule_count(path)
        files.append(item)

    clients = sorted({item["scope"] for item in files if item["kind"] == "client_rules"})
    network_scopes = sorted({item["scope"] for item in files if item["kind"] == "network_dataset"})
    manifest = {
        "schema": "generated_distribution_manifest_v2",
        "generated_at": now,
        "collection_date": args.date,
        "generated_root": str(generated),
        "client_rule_directories": clients,
        "network_dataset_directories": network_scopes,
        "semantics": {
            "client_rules": "generated/<client>/... are compiled V3 projections",
            "network_datasets": "generated/<scope>/... are companion routing datasets",
            "human_rule_tree": "rule/ is a generated human browsing and selection distribution derived from the same Semantic IR Run",
            "forbidden_alternate_rule_tree": "rules/ must not exist; there is no third rule directory",
        },
        "file_count": len(files),
        "files": files,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    report_dir = ROOT / "reports" / args.date
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "generated_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"[generated_manifest] files={len(files)} clients={clients} network={network_scopes} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
