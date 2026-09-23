#!/usr/bin/env python3
"""Fail-closed validation of collected PRS artifacts and immutable Source lineage."""
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
IDENTITY_KEYS = ("source_ref", "release_path", "snapshot_id", "content_digest", "expected_sha256")


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
    source = next(
        (
            s for s in obj.get("sources", [])
            if isinstance(s, dict) and s.get("id") == "popular-rules-source"
        ),
        None,
    )
    if not source:
        raise SystemExit("popular-rules-source missing from registry.yaml")
    return {
        str(entry.get("service") or entry.get("name")): entry
        for entry in (source.get("rules") or source.get("files") or [])
        if isinstance(entry, dict) and (entry.get("service") or entry.get("name"))
    }


def _historical_lineage_is_internal_consistent(
    service: str,
    item: dict[str, Any],
    path: Path,
    actual: str,
) -> tuple[bool, str]:
    immutable = item.get("immutable") or {}
    if not isinstance(immutable, dict):
        return False, "collected manifest has no immutable lineage metadata"

    missing = [key for key in IDENTITY_KEYS if not str(immutable.get(key) or "").strip()]
    if missing:
        return False, f"historical immutable lineage missing {missing}"

    historical_sha = str(immutable.get("expected_sha256") or "")
    if actual != historical_sha:
        return False, f"historical collected file sha mismatch expected={historical_sha} actual={actual}"

    item_sha = str(item.get("sha256") or item.get("cas_sha256") or "")
    if item_sha and actual != item_sha:
        return False, f"manifest sha mismatch actual={actual} manifest={item_sha}"

    if str(item.get("path") or "") != f"generated/source/{service}/domains.txt":
        return False, "artifact path mismatch"

    url = str(item.get("url") or "")
    historical_ref = str(immutable["source_ref"])
    if url and ("/main/" in url or f"/{historical_ref}/" not in url):
        return False, "historical acquisition url is not pinned to its recorded source_ref"

    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection-root", required=True, help="backup/YYYY-MM-DD")
    parser.add_argument("--json-out", default="")
    parser.add_argument("--allow-missing-current", action="store_true", help="PR mode: permit active bindings absent from this historical collection manifest")
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
    by_service = {
        str(item.get("service")): item
        for item in files
        if isinstance(item, dict) and item.get("service")
    }

    failures: list[str] = []
    verified: dict[str, Any] = {}
    historical: list[str] = []

    for service, binding in sorted(bindings.items()):
        rule = rules.get(service)
        if not rule or rule.get("enabled") is not True:
            failures.append(f"{service}: immutable binding active but registry rule is not enabled")
            continue

        item = by_service.get(service)
        if not item:
            if args.allow_missing_current:
                verified[service] = {
                    "status": "pending_collection_snapshot",
                    "lineage_mode": "current_binding_not_in_collection_backup",
                    "source_ref": binding.get("source_ref"),
                    "release_path": binding.get("release_path"),
                    "snapshot_id": binding.get("snapshot_id"),
                    "content_digest": binding.get("content_digest"),
                    "expected_sha256": binding.get("expected_sha256"),
                }
                continue
            failures.append(f"{service}: missing PRS collection manifest entry")
            continue

        local = item.get("local")
        if not local:
            failures.append(f"{service}: local path missing from manifest")
            continue
        path = root / str(local)
        if not path.is_file():
            failures.append(f"{service}: collected artifact missing at {path}")
            continue
        actual = sha256(path)

        immutable = item.get("immutable") or {}
        current_match = (
            isinstance(immutable, dict)
            and all(str(immutable.get(key) or "") == str(binding.get(key) or "") for key in IDENTITY_KEYS)
        )

        if not current_match:
            ok, reason = _historical_lineage_is_internal_consistent(service, item, path, actual)
            if not ok:
                failures.append(f"{service}: {reason}")
                continue
            historical.append(service)
            verified[service] = {
                "status": "verified_historical",
                "lineage_mode": "historical",
                "source_ref": immutable.get("source_ref"),
                "release_path": immutable.get("release_path"),
                "snapshot_id": immutable.get("snapshot_id"),
                "content_digest": immutable.get("content_digest"),
                "expected_sha256": immutable.get("expected_sha256"),
                "actual_sha256": actual,
                "current_binding_source_ref": binding.get("source_ref"),
                "local": str(path.relative_to(ROOT)),
            }
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
        if actual != expected:
            failures.append(f"{service}: collected file sha mismatch expected={expected} actual={actual}")
            continue

        verified[service] = {
            "status": "verified",
            "lineage_mode": "current",
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
        "schema": "immutable_source_lineage_gate_v2",
        "collection_root": args.collection_root,
        "binding_count": len(bindings),
        "verified_count": len(verified),
        "historical_count": len(historical),
        "historical_services": historical,
        "status": "PASS" if not failures and len(verified) == len(bindings) else "FAIL",
        "failures": failures,
        "services": verified,
        "note": (
            "Historical collection backups are validated for their own immutable integrity but "
            "are not required to equal a newer active Source binding. Current Source provenance "
            "is validated separately by source_provenance_gate.py."
        ),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if args.json_out:
        out = ROOT / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
