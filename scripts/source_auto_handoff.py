from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

SOURCE_REPORT_URL = (
    "https://raw.githubusercontent.com/cn-wanmei/"
    "Popular-Rules-Source/main/reports/durable-bridge/latest.json"
)
SOURCE_ROOT = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source"
REGISTRY_PATH = Path("sources/immutable_registry.yaml")
SERVICES = (
    "1688", "cainiao", "dingding", "qqmail",
    "qqmusic", "taobao", "tencentcloud", "tmall",
)
PROVENANCE_FIELDS = (
    "evidence_digest",
    "policy_digest",
    "generator_digest",
    "release_digest",
    "release_identity_version",
)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")


def _get_bytes(url: str, timeout: int = 45) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": "Popular-Rules-Collection/source-auto-handoff-v2"},
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def _get_json(url: str, timeout: int = 45) -> dict:
    value = json.loads(_get_bytes(url, timeout).decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {url}")
    return value


def _get_source_seal() -> dict:
    report = _get_json(SOURCE_REPORT_URL)
    if report.get("schema") != "popular_rules_source_durable_bridge_v2":
        raise RuntimeError(
            f"unsupported Source durable report schema: {report.get('schema')!r}"
        )
    source_ref = str(report.get("persistence_commit") or "")
    verified_input = str(report.get("verified_input_commit") or "")
    if not SHA40.fullmatch(source_ref) or not SHA40.fullmatch(verified_input):
        raise RuntimeError("Source durable report must contain exact SHA40 persistence and verified input commits")
    services = report.get("services") or {}
    if set(services) != set(SERVICES):
        raise RuntimeError(f"Source durable service set mismatch: {sorted(services)}")
    for sid in SERVICES:
        item = services[sid]
        if item.get("status") != "PERSISTED":
            raise RuntimeError(f"{sid}: Source durable status is not PERSISTED")
        for field in ("snapshot_id", "content_digest", *PROVENANCE_FIELDS, "release_path", "expected_sha256"):
            value = str(item.get(field) or "")
            if not value:
                raise RuntimeError(f"{sid}: Source durable report missing {field}")
        if str(item.get("release_identity_version")) != "2":
            raise RuntimeError(f"{sid}: release_identity_version must be 2")
    return report


def _load_registry() -> dict:
    value = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise RuntimeError("immutable registry must be a YAML mapping")
    return value


def _build_binding(source_ref: str, verified_input: str, sid: str, item: dict) -> dict:
    release_path = str(item["release_path"])
    if not release_path.startswith(f"releases/{sid}/"):
        raise RuntimeError(f"{sid}: unsafe release_path {release_path}")

    release = _get_json(f"{SOURCE_ROOT}/{source_ref}/{release_path}")
    expected_release = {
        "service_id": sid,
        "snapshot_id": str(item["snapshot_id"]),
        "content_digest": str(item["content_digest"]),
        **{field: str(item[field]) for field in PROVENANCE_FIELDS},
    }
    for field, value in expected_release.items():
        if str(release.get(field)) != value:
            raise RuntimeError(f"{sid}: Source release {field} mismatch")

    domains = _get_bytes(
        f"{SOURCE_ROOT}/{source_ref}/generated/source/{sid}/domains.txt"
    )
    actual_sha = hashlib.sha256(domains).hexdigest()
    if actual_sha != str(item["expected_sha256"]):
        raise RuntimeError(
            f"{sid}: Source domains checksum mismatch: "
            f"expected={item['expected_sha256']} actual={actual_sha}"
        )

    return {
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
        "expected_sha256": actual_sha,
    }


def main() -> None:
    report = _get_source_seal()
    source_ref = str(report["persistence_commit"])
    verified_input = str(report["verified_input_commit"])

    registry = _load_registry()
    bindings = registry.setdefault("bindings", {})
    if not isinstance(bindings, dict):
        raise RuntimeError("immutable registry bindings must be a mapping")

    changed_services: list[str] = []
    for sid in SERVICES:
        binding = _build_binding(source_ref, verified_input, sid, report["services"][sid])
        if bindings.get(sid) != binding:
            bindings[sid] = binding
            changed_services.append(sid)

    if registry.get("schema") != "popular_rules_collection_immutable_source_registry_v2":
        registry["schema"] = "popular_rules_collection_immutable_source_registry_v2"
    if registry.get("version") != 2:
        registry["version"] = 2

    REGISTRY_PATH.write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(json.dumps({
        "schema": "source_auto_handoff_v2",
        "source_ref": source_ref,
        "verified_input_commit": verified_input,
        "changed": bool(changed_services),
        "changed_services": changed_services,
        "services": list(SERVICES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
