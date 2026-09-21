#!/usr/bin/env python3
"""Fail-closed equality gate for immutable Popular-Rules-Source provenance v2."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source"
SERVICES = (
    "1688", "cainiao", "dingding", "qqmail",
    "qqmusic", "taobao", "tencentcloud", "tmall",
)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
PROVENANCE_FIELDS = (
    "evidence_digest", "policy_digest", "generator_digest",
    "release_digest", "release_identity_version",
)


def load_registry(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def get_text(url: str, timeout: int = 45) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": "Popular-Rules-Collection/immutable-provenance-gate-v2",
            "Accept": "application/json,text/plain,*/*",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def get_json(url: str, timeout: int = 45) -> dict:
    value = json.loads(get_text(url, timeout).decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {url}")
    return value


def verify_binding(service_id: str, binding: dict) -> dict:
    errors: list[str] = []
    source_ref = str(binding.get("source_ref") or "")
    verified_input = str(binding.get("verified_input_commit") or "")
    if not SHA40.fullmatch(source_ref):
        errors.append("source_ref must be a 40-char commit SHA")
    if not SHA40.fullmatch(verified_input):
        errors.append("verified_input_commit must be a 40-char commit SHA")
    if binding.get("source_id") != "popular-rules-source":
        errors.append("source_id mismatch")
    if binding.get("status") != "active":
        errors.append("binding must be active")

    release_path = str(binding.get("release_path") or "").lstrip("/")
    artifact_path = str(binding.get("artifact_path") or "").lstrip("/")
    if not release_path.startswith(f"releases/{service_id}/"):
        errors.append("release_path is outside the service release namespace")
    if artifact_path != f"generated/source/{service_id}/domains.txt":
        errors.append("artifact_path mismatch")

    for field in ("snapshot_id", "content_digest", "expected_sha256", *PROVENANCE_FIELDS):
        value = str(binding.get(field) or "")
        if field == "release_identity_version":
            if value != "2":
                errors.append("release_identity_version must be 2")
        elif field.endswith("_digest") or field == "expected_sha256":
            if not SHA64.fullmatch(value):
                errors.append(f"{field} must be a 64-char SHA256")
        elif not value:
            errors.append(f"{field} is required")

    if errors:
        return {"service_id": service_id, "status": "FAIL", "errors": errors}

    release_url = f"{SOURCE_ROOT}/{source_ref}/{release_path}"
    artifact_url = f"{SOURCE_ROOT}/{source_ref}/{artifact_path}"
    try:
        release = get_json(release_url)
        body = get_text(artifact_url)
    except Exception as exc:
        return {
            "service_id": service_id,
            "status": "FAIL",
            "errors": [f"upstream immutable artifact fetch failed: {type(exc).__name__}: {exc}"],
        }

    checks: dict[str, bool] = {}
    checks["release_service"] = release.get("service_id") == service_id
    checks["release_snapshot"] = str(release.get("snapshot_id")) == str(binding["snapshot_id"])
    checks["release_content"] = str(release.get("content_digest")) == str(binding["content_digest"])
    for field in PROVENANCE_FIELDS:
        checks[field] = str(release.get(field)) == str(binding[field])
    checks["artifact_sha256"] = hashlib.sha256(body).hexdigest() == str(binding["expected_sha256"])

    failed = [key for key, passed in checks.items() if not passed]
    return {
        "service_id": service_id,
        "status": "PASS" if not failed else "FAIL",
        "source_ref": source_ref,
        "verified_input_commit": verified_input,
        "snapshot_id": binding["snapshot_id"],
        "checks": checks,
        "failed_checks": failed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=ROOT / "sources" / "immutable_registry.yaml")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    schema = str(registry.get("schema") or "")
    if schema != "popular_rules_collection_immutable_source_registry_v2":
        print(json.dumps({"schema": "source_provenance_gate_v2", "status": "FAIL", "errors": [f"expected registry v2, got {schema!r}"]}, ensure_ascii=False, indent=2))
        return 1

    bindings = registry.get("bindings") or {}
    results = {sid: verify_binding(sid, bindings.get(sid) or {}) for sid in SERVICES}
    errors = {
        sid: item.get("errors") or item.get("failed_checks") or []
        for sid, item in results.items()
        if item.get("status") != "PASS"
    }
    result = {
        "schema": "source_provenance_gate_v2",
        "status": "PASS" if not errors else "FAIL",
        "services": results,
        "error_count": sum(len(items) for items in errors.values()),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
