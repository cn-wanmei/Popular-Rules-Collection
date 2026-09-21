#!/usr/bin/env python3
"""Materialize the current Popular-Rules-Source durable seal into Collection's immutable registry."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source"
SERVICES = (
    "1688", "cainiao", "dingding", "qqmail",
    "qqmusic", "taobao", "tencentcloud", "tmall",
)
PROVENANCE_FIELDS = (
    "evidence_digest", "policy_digest", "generator_digest",
    "release_digest", "release_identity_version",
)


def get_text(url: str, timeout: int = 45) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": "Popular-Rules-Collection/source-auto-handoff-v2"},
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def get_json(url: str, timeout: int = 45) -> dict:
    value = json.loads(get_text(url, timeout).decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {url}")
    return value


def load_registry(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"invalid registry object: {path}")
    return data


def load_seal(url: str) -> dict:
    data = get_json(url)
    if data.get("schema") != "popular_rules_source_durable_bridge_v2":
        raise ValueError(f"unexpected Source durable seal schema: {data.get('schema')!r}")
    source_ref = str(data.get("persistence_commit") or "")
    verified_input = str(data.get("verified_input_commit") or "")
    if len(source_ref) != 40 or len(verified_input) != 40:
        raise ValueError("Source durable seal requires exact 40-char persistence and verified input commits")
    services = data.get("services") or {}
    if set(services) != set(SERVICES):
        raise ValueError(f"Source durable seal service set mismatch: {sorted(services)}")
    for sid in SERVICES:
        item = services[sid]
        if item.get("status") != "PERSISTED":
            raise ValueError(f"{sid}: Source durable seal is not PERSISTED")
        for field in ("snapshot_id", "content_digest", *PROVENANCE_FIELDS, "release_path"):
            if not str(item.get(field) or "").strip():
                raise ValueError(f"{sid}: durable seal missing {field}")
    return data


def update_registry(registry_path: Path, seal: dict) -> tuple[dict, bool]:
    registry = load_registry(registry_path)
    bindings = registry.setdefault("bindings", {})
    changed = False

    source_ref = str(seal["persistence_commit"])
    verified_input = str(seal["verified_input_commit"])
    for sid in SERVICES:
        item = seal["services"][sid]
        release_path = str(item["release_path"])
        if not release_path.startswith(f"releases/{sid}/"):
            raise ValueError(f"{sid}: unsafe release path {release_path}")
        release = get_json(f"{SOURCE_ROOT}/{source_ref}/{release_path}")
        expected = {
            "service_id": sid,
            "snapshot_id": str(item["snapshot_id"]),
            "content_digest": str(item["content_digest"]),
            **{field: str(item[field]) for field in PROVENANCE_FIELDS},
        }
        for field, value in expected.items():
            if str(release.get(field)) != value:
                raise ValueError(f"{sid}: Source release {field} mismatch")
        domains = get_text(f"{SOURCE_ROOT}/{source_ref}/generated/source/{sid}/domains.txt")
        expected_sha = hashlib.sha256(domains).hexdigest()
        if expected_sha != str(item.get("expected_sha256") or expected_sha):
            raise ValueError(f"{sid}: Source seal expected_sha256 mismatch")
        new_binding = {
            "status": "active",
            "source_id": "popular-rules-source",
            "source_ref": source_ref,
            "verified_input_commit": verified_input,
            "artifact_path": f"generated/source/{sid}/domains.txt",
            "release_path": release_path,
            "snapshot_id": str(item["snapshot_id"]),
            "content_digest": str(item["content_digest"]),
            "evidence_digest": str(item["evidence_digest"]),
            "policy_digest": str(item["policy_digest"]),
            "generator_digest": str(item["generator_digest"]),
            "release_digest": str(item["release_digest"]),
            "release_identity_version": str(item["release_identity_version"]),
            "expected_sha256": expected_sha,
        }
        if bindings.get(sid) != new_binding:
            bindings[sid] = new_binding
            changed = True

    new_schema = "popular_rules_collection_immutable_source_registry_v2"
    if registry.get("schema") != new_schema or registry.get("version") != 2:
        registry["schema"] = new_schema
        registry["version"] = 2
        changed = True
    return registry, changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-url", default=f"{SOURCE_ROOT}/main/reports/durable-bridge/latest.json")
    parser.add_argument("--registry", type=Path, default=ROOT / "sources" / "immutable_registry.yaml")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    seal = load_seal(args.seal_url)
    registry, changed = update_registry(args.registry, seal)
    output = args.output or args.registry
    output.write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(json.dumps({
        "schema": "source_auto_handoff_v2",
        "changed": changed,
        "source_ref": seal["persistence_commit"],
        "verified_input_commit": seal["verified_input_commit"],
        "services": list(SERVICES),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
