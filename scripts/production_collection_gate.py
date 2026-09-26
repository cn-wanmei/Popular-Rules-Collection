#!/usr/bin/env python3
"""Fail-closed gate for production builds backed by a complete Collection snapshot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"{label} missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{label} is invalid JSON: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{label} must be a JSON object: {path}")
    return payload


def validate_collection_root(collection_root: Path) -> dict[str, Any]:
    root = collection_root.expanduser().resolve()
    manifest = _load_json(root / "manifests" / "_collection.json", "collection manifest")
    day_manifest = _load_json(root / "manifests" / "_day.json", "service collection day manifest")
    errors: list[str] = []

    if manifest.get("schema") != "collection_manifest_v1":
        errors.append(f"unsupported collection manifest schema: {manifest.get('schema')!r}")
    if not manifest.get("collection_id"):
        errors.append("collection_id is missing")
    if manifest.get("status") == "blocked":
        errors.append(
            "collection status is blocked: "
            + ", ".join(str(x) for x in (manifest.get("critical_failures") or ["unknown"]))
        )

    date = str(manifest.get("date") or "")
    expected_root = Path("backup") / date
    if manifest.get("root") != str(expected_root):
        errors.append(
            f"collection manifest root mismatch: expected {str(expected_root)!r}, "
            f"got {manifest.get('root')!r}"
        )
    if manifest.get("skip_large") is not False:
        errors.append(
            "production build requires a complete collection snapshot: "
            "manifest.skip_large must be false"
        )

    service_node = ((manifest.get("nodes") or {}).get("service_rules") or {})
    if service_node.get("status") != "ok":
        errors.append(
            f"service_rules collection node is not healthy: {service_node.get('status')!r}"
        )

    if day_manifest.get("schema") != "collection_manifest_v2":
        errors.append(
            f"unsupported service day manifest schema: {day_manifest.get('schema')!r}"
        )
    if date != str(day_manifest.get("date") or ""):
        errors.append(
            f"collection/day date mismatch: {date!r} != {day_manifest.get('date')!r}"
        )

    required_failures: list[dict[str, Any]] = []
    for source in day_manifest.get("sources") or []:
        if not isinstance(source, dict):
            errors.append("service day manifest contains a non-object source summary")
            continue
        failures = int(source.get("required_failures") or 0)
        if failures:
            required_failures.append(
                {"source": source.get("source"), "required_failures": failures}
            )
    if required_failures:
        errors.append(f"required source failures present: {required_failures}")

    report = {
        "schema": "production_collection_gate_v1",
        "collection_root": str(root),
        "collection_id": manifest.get("collection_id"),
        "date": manifest.get("date"),
        "skip_large": manifest.get("skip_large"),
        "service_rules_status": service_node.get("status"),
        "required_failures": required_failures,
        "pass": not errors,
        "errors": errors,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed production Collection completeness gate")
    parser.add_argument("--collection-root", required=True)
    args = parser.parse_args()

    report = validate_collection_root(Path(args.collection_root))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["pass"]:
        print("PRODUCTION COLLECTION GATE: BLOCKED")
        return 1
    print("PRODUCTION COLLECTION GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
