#!/usr/bin/env python3
"""Fail-closed validation that collected PRS files match immutable Source bindings."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sources" / "registry.yaml"
IMMUTABLE = ROOT / "sources" / "immutable_registry.yaml"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    obj = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(obj, dict):
        raise SystemExit(f"invalid yaml object: {path}")
    return obj


def active_bindings() -> dict[str, dict[str, Any]]:
    obj = load_yaml(IMMUTABLE)
    bindings = obj.get("bindings") or {}
    return {
        str(service): binding
        for service, binding in bindings.items()
        if isinstance(binding, dict) and binding.get("status") == "active"
    }


def registry_rules() -> dict[str, dict[str, Any]]:
    obj = load_yaml(REGISTRY)
    source = next((s for s in obj.get("sources", []) if isinstance(s, dict) and s.get("id") == "popular-rules-source"), None)
    if not source:
        raise SystemExit("popular-rules-source missing from registry.yaml")
    return {
        str(entry.get("service") or entry.get("name")): entry
        for entry in (source.get("rules") or source.get("files") or [])
        if isinstance(entry, dict) and (entry.get("service") or entry.get("name"))
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection-root", required=True, help="backup/YYYY-MM-DD")
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    root = ROOT / args.collection_root
    collection_manifest_path = root / "manifests" / "_collection.json"
    source_manifest_path = root / "manifests" / "popular-rules-source.json"
    if not collection_manifest_path.is_file():
        raise SystemExit(f"missing collection manifest: {collection_manifest_path}")
    if not source_manifest_path.is_file():
        raise SystemExit(f"missing PRS source manifest: {source_manifest_path}")

    collection = json.loads(collection_manifest_path.read_text(encoding="utf-8"))
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    if collection.get("status") == "blocked":
        raise SystemExit("collection manifest is blocked")

    bindings = active_bindings()
    rules = registry_rules()
    files = source_manifest.get("files") or []
    by_service = {str(item.get("service")): item for item in files if isinstance(item, dict) and item.get("service")}

    failures: list[str] = []
    verified: dict[str, Any] = {}
    for service, binding in sorted(bindings.items()):
        rule = rules.get(service)
        if not rule or rule.get("enabled") is not True:
            failures.append(f"{service}: immutable binding active but registry rule is not enabled")
            continue

        item = by_service.get(service)
        if not item:
            failures.append(f"{service}: missing PRS collection manifest entry")
            continue

        expected = str(binding.get("expected_sha256") or "")
        actual_manifest_sha = str(item.get("sha256") or item.get("cas_sha256") or "")
        status = str(item.get("status") or "")
        if status not in {"ok", "not_modified", "skipped"}:
            failures.append(f"{service}: manifest status={status}")
            continue
        if actual_manifest_sha != expected:
            failures.append(f"{service}: manifest sha mismatch expected={expected} actual={actual_manifest_sha}")
        if str(item.get("path")) != str(binding.get("artifact_path")):
            failures.append(f"{service}: artifact path mismatch")
        url = str(item.get("url") or "")
        source_ref = str(binding.get("source_ref") or "")
        if url and ("/main/" in url or f"/{source_ref}/" not in url):
            failures.append(f"{service}: acquisition url is not pinned to immutable source_ref")
        immutable = item.get("immutable") or {}
        for key in ("source_ref", "release_path", "snapshot_id", "content_digest", "expected_sha256"):
            if str(immutable.get(key) or "") != str(binding.get(key) or ""):
                failures.append(f"{service}: immutable.{key} mismatch")
        local = item.get("local")
        if not local:
            failures.append(f"{service}: local path missing from manifest")
            continue
        path = root / str(local)
        if not path.is_file():
            failures.append(f"{service}: collected artifact missing at {path}")
            continue
        actual = sha256(path)
        if actual != expected:
            failures.append(f"{service}: collected file sha mismatch expected={expected} actual={actual}")
            continue

        verified[service] = {
            "status": "verified",
            "source_ref": binding.get("source_ref"),
            "release_path": binding.get("release_path"),
            "snapshot_id": binding.get("snapshot_id"),
            "content_digest": binding.get("content_digest"),
            "expected_sha256": expected,
            "actual_sha256": actual,
            "collection_manifest_status": status,
            "local": str(path.relative_to(ROOT)),
        }

    report = {
        "schema": "immutable_source_lineage_gate_v1",
        "collection_root": args.collection_root,
        "binding_count": len(bindings),
        "verified_count": len(verified),
        "status": "PASS" if not failures and len(verified) == len(bindings) else "FAIL",
        "failures": failures,
        "services": verified,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if args.json_out:
        out = ROOT / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
