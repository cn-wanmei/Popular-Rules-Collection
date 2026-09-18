#!/usr/bin/env python3
"""Reproducible V1 Phase 2.3-2.7 audit engine."""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "reports" / "v1" / "phase2"


def git(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def load_yaml(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as fh:
        value = yaml.safe_load(fh)
    return default if value is None else value


def normalize_domain(value: str) -> str:
    return value.strip().lower().rstrip(".")


def normalize_cidr(value: str) -> str | None:
    try:
        return str(ipaddress.ip_network(value.strip(), strict=False))
    except ValueError:
        return None


def normalize_url(value: str) -> str | None:
    try:
        p = urlsplit(value.strip())
        if p.scheme.lower() not in {"http", "https"} or not p.hostname:
            return None
        host = p.hostname.lower().rstrip(".")
        port = p.port
        netloc = host
        if port is not None and not ((p.scheme.lower() == "http" and port == 80) or (p.scheme.lower() == "https" and port == 443)):
            netloc = f"{host}:{port}"
        return urlunsplit((p.scheme.lower(), netloc, p.path or "", p.query or "", ""))
    except Exception:
        return None


def looks_like_domain(value: str) -> bool:
    d = normalize_domain(value)
    return "/" not in d and " " not in d and "." in d and re.fullmatch(r"[a-z0-9*_-]+(?:\.[a-z0-9*_-]+)+", d) is not None


def parse_assets(text: str) -> dict[str, set[str]]:
    out = {k: set() for k in ("domains", "domain_suffixes", "domain_keywords", "ip_cidrs", "urls", "unknown")}
    for raw in text.splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        if value.startswith(("http://", "https://")):
            url = normalize_url(value)
            if url:
                out["urls"].add(url)
                continue
        cidr = normalize_cidr(value)
        if cidr:
            out["ip_cidrs"].add(cidr)
            continue
        d = normalize_domain(value)
        if d.startswith("*."):
            out["domain_suffixes"].add(d[2:])
        elif looks_like_domain(value):
            out["domains"].add(d)
        elif "*" in d and " " not in d:
            out["domain_suffixes"].add(d.lstrip("*."))
        else:
            out["unknown"].add(value)
    return out


def merge(dst, src):
    for key in dst:
        dst[key].update(src.get(key, set()))


def parse_metadata(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return load_yaml(path, {}) or {}
    except Exception:
        return {}


def flatten_index(index: dict) -> list[dict]:
    rows = []
    for category, block in (index.get("categories") or {}).items():
        if not isinstance(block, dict):
            continue
        for rule in block.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            row = dict(rule)
            row["category"] = str(category)
            rows.append(row)
    return rows


def entry_assets(entry_path: Path) -> dict[str, set[str]]:
    total = {k: set() for k in ("domains", "domain_suffixes", "domain_keywords", "ip_cidrs", "urls", "unknown")}
    if not entry_path.exists():
        return total
    for path in sorted(entry_path.iterdir()):
        if not path.is_file() or path.name == "metadata.yaml":
            continue
        if path.suffix.lower() not in {".list", ".txt", ".yaml"}:
            continue
        try:
            merge(total, parse_assets(path.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    return total


def confirmed_map(root: Path) -> dict[str, dict]:
    data = load_yaml(root / "reports" / "v1" / "LEGACY_MAPPING.yaml", {}) or {}
    return {
        str(x.get("legacy")): x
        for x in (data.get("mappings") or [])
        if isinstance(x, dict) and x.get("confidence") == "confirmed"
    }


def prior_conflicts(root: Path) -> list[dict]:
    data = load_yaml(root / "reports" / "v1" / "CONFLICTS.yaml", {}) or {}
    return [x for x in (data.get("conflicts") or []) if isinstance(x, dict)]


def scan(root: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    index_path = root / "rule" / "_index.yaml"
    index = load_yaml(index_path, {}) or {}
    entries = flatten_index(index)
    confirmed = confirmed_map(root)

    inventory = []
    aggregate_rows = []
    asset_index = defaultdict(list)

    indexed_paths = {str(x["path"]) for x in entries if x.get("path")}
    filesystem_paths = set()
    for meta in (root / "rule").glob("**/metadata.yaml"):
        rel = meta.parent.relative_to(root).as_posix()
        parts = meta.relative_to(root / "rule").parts
        if parts and parts[0] not in {"category", "service", "shared"}:
            filesystem_paths.add(rel)

    for entry in entries:
        legacy = str(entry.get("path"))
        entry_dir = root / legacy
        meta = parse_metadata(entry_dir / "metadata.yaml")
        assets = entry_assets(entry_dir)

        for kind, values in assets.items():
            for value in values:
                asset_index[f"{kind}:{value}"].append(legacy)

        if legacy in confirmed:
            identity_status = "confirmed"
            identity_type = confirmed[legacy].get("type")
            v1_id = confirmed[legacy].get("service")
        elif entry.get("service_type") == "service":
            identity_status = "candidate"
            identity_type = "service"
            v1_id = str(entry["id"])
        elif entry.get("service_type") == "aggregate":
            identity_status = "quarantine"
            identity_type = "aggregate-candidate"
            v1_id = None
        else:
            identity_status = "quarantine"
            identity_type = "legacy-unknown"
            v1_id = None

        categories = meta.get("categories") if isinstance(meta.get("categories"), list) else []
        children = meta.get("children") if isinstance(meta.get("children"), list) else []
        sources = meta.get("sources") if isinstance(meta.get("sources"), list) else []
        clients = meta.get("clients") if isinstance(meta.get("clients"), list) else []

        inventory.append({
            "legacy": legacy,
            "legacy_id": str(entry.get("id")),
            "name": str(entry.get("name") or entry.get("id")),
            "category": str(entry.get("category")),
            "index_service_type": str(entry.get("service_type")),
            "index_domains": int(entry.get("domains") or 0),
            "index_ips": int(entry.get("ips") or 0),
            "path_exists": entry_dir.exists(),
            "metadata_present": bool(meta),
            "metadata_service_type": str(meta.get("service_type") or ""),
            "metadata_parent": meta.get("parent"),
            "metadata_primary_category": meta.get("primary_category"),
            "metadata_categories": [str(x) for x in categories],
            "metadata_children": [str(x) for x in children],
            "metadata_sources": [str(x) for x in sources],
            "metadata_clients": [str(x) for x in clients],
            "asset_counts": {k: len(v) for k, v in assets.items()},
            "identity_status": identity_status,
            "identity_type": identity_type,
            "v1_service_id": v1_id,
        })

    category_members = defaultdict(set)
    for e in entries:
        category_members[str(e.get("category"))].add(str(e.get("id")))

    for item in inventory:
        if item["index_service_type"] != "aggregate":
            continue
        meta_children = set(item["metadata_children"])
        index_children = category_members[item["category"]] - {item["legacy_id"]}
        aggregate_rows.append({
            "legacy": item["legacy"],
            "aggregate_id": item["legacy_id"],
            "category": item["category"],
            "metadata_children": sorted(meta_children),
            "indexed_category_members": sorted(index_children),
            "metadata_only_children": sorted(meta_children - index_children),
            "index_only_children": sorted(index_children - meta_children),
            "relation_status": "aligned" if meta_children == index_children else "drift",
            "empty_children": not bool(meta_children or index_children),
        })

    duplicate_keys = [
        {"key": key, "legacy_paths": sorted(set(paths))}
        for key, paths in sorted(asset_index.items())
        if len(set(paths)) > 1
    ]
    orphan_paths = sorted(filesystem_paths - indexed_paths)
    indexed_missing_paths = sorted(x["legacy"] for x in inventory if not x["path_exists"])
    missing_metadata = sorted(x["legacy"] for x in inventory if not x["metadata_present"])
    unknown_count = sum(x["asset_counts"]["unknown"] for x in inventory)
    aggregate_drift = sorted(x["legacy"] for x in aggregate_rows if x["relation_status"] == "drift")

    conflicts = prior_conflicts(root)
    if orphan_paths:
        conflicts.append({
            "id": "ORPH-INDEX-001", "type": "filesystem-rule-directory-not-indexed",
            "severity": "high", "count": len(orphan_paths),
            "entries": orphan_paths[:100],
            "resolution": "Quarantine until mapped or explicitly deprecated.",
        })
    if indexed_missing_paths:
        conflicts.append({
            "id": "ORPH-INDEX-002", "type": "indexed-entry-path-missing",
            "severity": "blocking", "count": len(indexed_missing_paths),
            "entries": indexed_missing_paths[:100],
            "resolution": "Repair index or restore source before promotion.",
        })
    if missing_metadata:
        conflicts.append({
            "id": "META-001", "type": "missing-metadata",
            "severity": "high", "count": len(missing_metadata),
            "entries": missing_metadata[:100],
            "resolution": "Complete metadata evidence before V1 promotion.",
        })
    if unknown_count:
        conflicts.append({
            "id": "ASSET-UNKNOWN-001", "type": "unclassified-legacy-assets",
            "severity": "medium", "count": unknown_count,
            "resolution": "Review non-domain/non-CIDR/non-URL lines; never silently discard them.",
        })
    if aggregate_drift:
        conflicts.append({
            "id": "AGG-DRIFT-FINAL-001", "type": "aggregate-membership-drift",
            "severity": "high", "count": len(aggregate_drift),
            "entries": aggregate_drift,
            "resolution": "Require explicit hierarchy resolution before Parent Service promotion.",
        })

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": git(["git", "rev-parse", "HEAD"]),
        "git_branch": git(["git", "branch", "--show-current"]),
        "inventory_sha256": hashlib.sha256(index_path.read_bytes()).hexdigest(),
        "legacy_entries": len(entries),
        "service_candidates": sum(x["index_service_type"] == "service" for x in inventory),
        "aggregate_candidates": sum(x["index_service_type"] == "aggregate" for x in inventory),
        "metadata_present": sum(x["metadata_present"] for x in inventory),
        "metadata_missing": len(missing_metadata),
        "confirmed_identity": sum(x["identity_status"] == "confirmed" for x in inventory),
        "candidate_identity": sum(x["identity_status"] == "candidate" for x in inventory),
        "quarantined_identity": sum(x["identity_status"] == "quarantine" for x in inventory),
        "aggregate_relation_drift": len(aggregate_drift),
        "duplicate_asset_keys": len(duplicate_keys),
        "orphan_paths": len(orphan_paths),
        "indexed_missing_paths": len(indexed_missing_paths),
        "unclassified_asset_lines": unknown_count,
    }

    (out / "LEGACY_SEMANTIC_INVENTORY.json").write_text(
        json.dumps({"version": 1, "phase": "2.3", "summary": summary, "entries": inventory}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (out / "IDENTITY_RESOLUTION.yaml").write_text(
        yaml.safe_dump({
            "version": 1, "phase": "2.4", "status": "audit",
            "policy": "Only explicit prior evidence is confirmed; all other identities remain candidate/quarantine.",
            "entries": inventory,
        }, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (out / "AGGREGATE_RESOLUTION.yaml").write_text(
        yaml.safe_dump({
            "version": 1, "phase": "2.5", "status": "audit",
            "policy": "Metadata children and indexed membership are separate evidence sets.",
            "aggregates": aggregate_rows,
        }, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (out / "CANONICAL_ASSET_AUDIT.json").write_text(
        json.dumps({
            "version": 1, "phase": "2.6",
            "normalization": {
                "domains": "lowercase + trailing-dot removal",
                "cidr": "ipaddress canonical network form",
                "urls": "scheme/host normalization; fragments removed; default ports removed",
                "semantic_pruning": False,
            },
            "summary": summary,
            "duplicate_keys": duplicate_keys[:5000],
        }, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (out / "DUPLICATES.yaml").write_text(
        yaml.safe_dump({
            "version": 1, "phase": "2.7",
            "duplicate_asset_keys": len(duplicate_keys),
            "duplicates": duplicate_keys[:5000],
            "policy": "Exact canonical asset equality only; no semantic parent-domain pruning.",
        }, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (out / "ORPHANS.yaml").write_text(
        yaml.safe_dump({
            "version": 1, "phase": "2.7",
            "filesystem_rule_dirs_not_in_index": orphan_paths,
            "indexed_entries_missing_path": indexed_missing_paths,
            "indexed_entries_missing_metadata": missing_metadata,
        }, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (out / "CONFLICTS_FINAL.yaml").write_text(
        yaml.safe_dump({
            "version": 1, "phase": "2.7",
            "severity_definitions": {
                "blocking": "Must resolve before V1 promotion.",
                "high": "Requires explicit mapping/evidence.",
                "medium": "Review required; may not block unrelated entries.",
                "info": "Observational.",
            },
            "conflicts": conflicts,
        }, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    blocking = any(x.get("severity") == "blocking" for x in conflicts)
    high = any(x.get("severity") == "high" for x in conflicts)
    gate = {
        "version": 1, "phase": "2.2-2.7",
        "status": "blocked" if (blocking or high) else "audit-complete",
        "promotion_ready": False,
        "summary": summary,
        "gates": {
            "2.2_baseline": summary["git_commit"] != "unknown",
            "2.3_184_entries_indexed": len(entries) == 184,
            "2.4_identity_all_confirmed": summary["quarantined_identity"] == 0,
            "2.5_aggregate_relations_clean": summary["aggregate_relation_drift"] == 0,
            "2.6_no_unclassified_assets": summary["unclassified_asset_lines"] == 0,
            "2.7_no_blocking_or_high": not blocking and not high,
        },
    }
    (out / "PHASE2_GATE.yaml").write_text(
        yaml.safe_dump(gate, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (out / "PHASE2_SUMMARY.md").write_text(
        "# V1 Phase 2.2–2.7 Audit Summary\n\n"
        f"- Commit: {summary['git_commit']}\n"
        f"- Legacy entries: {summary['legacy_entries']}\n"
        f"- Service candidates: {summary['service_candidates']}\n"
        f"- Aggregate candidates: {summary['aggregate_candidates']}\n"
        f"- Metadata present: {summary['metadata_present']}\n"
        f"- Metadata missing: {summary['metadata_missing']}\n"
        f"- Confirmed identities: {summary['confirmed_identity']}\n"
        f"- Candidate identities: {summary['candidate_identity']}\n"
        f"- Quarantined identities: {summary['quarantined_identity']}\n"
        f"- Aggregate relation drift: {summary['aggregate_relation_drift']}\n"
        f"- Duplicate canonical asset keys: {summary['duplicate_asset_keys']}\n"
        f"- Orphan paths: {summary['orphan_paths']}\n"
        f"- Indexed missing paths: {summary['indexed_missing_paths']}\n"
        f"- Unclassified asset lines: {summary['unclassified_asset_lines']}\n\n"
        "V1 promotion remains blocked until all blocking/high findings are resolved and V3 regression gates pass.\n",
        encoding="utf-8",
    )
    return gate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    result = scan(args.root, args.out)
    print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
    return 1 if result["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
