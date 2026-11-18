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
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
PROVENANCE_FIELDS = (
    "evidence_digest", "policy_digest", "generator_digest",
    "release_digest", "release_identity_version",
)

# Exact immutable legacy-LKG tuples. These preserve only existing bindings and
# never qualify replacement snapshots or permit automatic handoff.
PHASE2_LKG_EXCEPTIONS = {
    # Original pinned Source revision.
    ("1688", "f5a3291c5020368f886064bcca026c836801ba3d"): ("snap-1688-222302f3a20ecb7c08c72ed0", "222302f3a20ecb7c08c72ed09a2942e0ae41aa83c1a0086b47ddd9c0679ac776"),
    ("cainiao", "f5a3291c5020368f886064bcca026c836801ba3d"): ("snap-cainiao-a8a898392298ebaa644a783e", "a8a898392298ebaa644a783ed30f4f5dc994c4245e175974ad71a3552b9293d8"),
    ("dingding", "f5a3291c5020368f886064bcca026c836801ba3d"): ("snap-dingding-09ae1ecd000f1688f61e99a0", "09ae1ecd000f1688f61e99a07f7c36fae8ad0dbd7c9287f8857344ec6e3a70ad"),
    ("taobao", "f5a3291c5020368f886064bcca026c836801ba3d"): ("snap-taobao-834d549e8982036ce1438963", "834d549e8982036ce1438963983527791e70997603616758bac4fb8f7c29d38b"),
    ("tencentcloud", "f5a3291c5020368f886064bcca026c836801ba3d"): ("snap-tencentcloud-e55bc8c508e839813ae20cd0", "e55bc8c508e839813ae20cd04f7af034fd4b76745c5ee1efc49b14b3ca57a7b8"),
    ("tiktok", "f5a3291c5020368f886064bcca026c836801ba3d"): ("snap-tiktok-d7c408670d9f72fda616937c", "d7c408670d9f72fda616937c2419e8311119b1827bdb34848a2d6748e3a934e6"),
    ("tmall", "f5a3291c5020368f886064bcca026c836801ba3d"): ("snap-tmall-17de7049e2f7bf67cb88c785", "17de7049e2f7bf67cb88c7859d6d071375e89173e148cbceee484925843f8a90"),
    # Durable bridge commit used by Collection PR #331. The same seven
    # historical releases were verified at this immutable ref; their newer
    # Phase-2 report entries must not silently replace these LKG identities.
    ("1688", "4452ae321d306efef7cd45e67310adbd749195f9"): ("snap-1688-222302f3a20ecb7c08c72ed0", "222302f3a20ecb7c08c72ed09a2942e0ae41aa83c1a0086b47ddd9c0679ac776"),
    ("cainiao", "4452ae321d306efef7cd45e67310adbd749195f9"): ("snap-cainiao-a8a898392298ebaa644a783e", "a8a898392298ebaa644a783ed30f4f5dc994c4245e175974ad71a3552b9293d8"),
    ("dingding", "4452ae321d306efef7cd45e67310adbd749195f9"): ("snap-dingding-09ae1ecd000f1688f61e99a0", "09ae1ecd000f1688f61e99a07f7c36fae8ad0dbd7c9287f8857344ec6e3a70ad"),
    ("taobao", "4452ae321d306efef7cd45e67310adbd749195f9"): ("snap-taobao-834d549e8982036ce1438963", "834d549e8982036ce1438963983527791e70997603616758bac4fb8f7c29d38b"),
    ("tencentcloud", "4452ae321d306ef7cd45e67310adbd749195f9"): ("snap-tencentcloud-e55bc8c508e839813ae20cd0", "e55bc8c508e839813ae20cd04f7af034fd4b76745c5ee1efc49b14b3ca57a7b8"),
    ("tiktok", "4452ae321d306efef7cd45e67310adbd749195f9"): ("snap-tiktok-d7c408670d9f72fda616937c", "d7c408670d9f72fda616937c2419e8311119b1827bdb34848a2d6748e3a934e6"),
    ("tmall", "4452ae321d306efef7cd45e67310adbd749195f9"): ("snap-tmall-17de7049e2f7bf67cb88c785", "17de7049e2f7bf67cb88c7859d6d071375e89173e148cbceee484925843f8a90"),
}


def is_exact_phase2_lkg(service_id: str, source_ref: str, binding: dict) -> bool:
    expected = PHASE2_LKG_EXCEPTIONS.get((service_id, source_ref))
    return bool(expected and str(binding.get("snapshot_id") or "") == expected[0]
                and str(binding.get("release_digest") or "") == expected[1])


def release_handoff_eligible(release: dict) -> bool:
    validation = release.get("validation")
    if not isinstance(validation, dict) or validation.get("release_state") != "CANDIDATE":
        return False
    return "handoff_eligible" not in validation or validation.get("handoff_eligible") is True


def phase2_eligibility(source_ref: str, service_id: str, binding: dict, lifecycle_state: str) -> bool:
    report = get_json(f"{SOURCE_ROOT}/{source_ref}/reports/generated/phase2_service_completion.json")
    if report.get("schema") != "phase2_service_completion_derived_v1":
        return False
    services = report.get("services") or {}
    record = services.get(service_id) if isinstance(services, dict) else None
    if not isinstance(record, dict):
        return False
    blockers = record.get("blockers")
    if not isinstance(blockers, list) or blockers or record.get("verified") is not True:
        return False
    if str(record.get("declared_state") or "") != lifecycle_state:
        return False
    if str(record.get("snapshot_id") or "") != str(binding.get("snapshot_id") or ""):
        return False
    if str(record.get("release_digest") or "") != str(binding.get("release_digest") or ""):
        return False
    if lifecycle_state == "production" and record.get("production_activated") is not True:
        return False
    if lifecycle_state == "verified" and record.get("production_activated") is True:
        return False
    return True


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
    lifecycle_attestation = "LEGACY_LKG_UNATTESTED"
    lifecycle_fields = ("lifecycle_ref", "lifecycle_state", "lifecycle_config_sha256")
    if any(binding.get(field) for field in lifecycle_fields):
        if not all(binding.get(field) for field in lifecycle_fields):
            return {"service_id": service_id, "status": "FAIL", "errors": ["incomplete lifecycle attestation"]}
        lifecycle_ref = str(binding.get("lifecycle_ref") or "")
        if lifecycle_ref != source_ref:
            return {"service_id": service_id, "status": "FAIL", "errors": ["lifecycle_ref must equal immutable source_ref"]}
        try:
            lifecycle_raw = get_text(f"{SOURCE_ROOT}/{source_ref}/config/source_canary_state.yaml")
            lifecycle_digest = hashlib.sha256(lifecycle_raw).hexdigest()
            lifecycle_doc = yaml.safe_load(lifecycle_raw.decode("utf-8")) or {}
            lifecycle_record = (lifecycle_doc.get("services") or {}).get(service_id) or {}
        except Exception as exc:
            return {"service_id": service_id, "status": "FAIL", "errors": [f"lifecycle SSOT fetch/parse failed: {type(exc).__name__}: {exc}"]}
        lifecycle_state = str(lifecycle_record.get("state") or "")
        lifecycle_ok = (
            lifecycle_doc.get("schema") == "popular_rules_source_lifecycle_v1"
            and lifecycle_record.get("enabled") is True
            and lifecycle_state in {"production", "verified"}
            and lifecycle_state == str(binding.get("lifecycle_state"))
            and lifecycle_digest == str(binding.get("lifecycle_config_sha256"))
        )
        checks["lifecycle_eligibility"] = lifecycle_ok
        exact_lkg_hold = is_exact_phase2_lkg(service_id, source_ref, binding)
        checks["release_handoff_eligibility"] = release_handoff_eligible(release) or exact_lkg_hold
        if exact_lkg_hold:
            checks["phase2_eligibility"] = True
            lifecycle_attestation = "LEGACY_LKG_PHASE2_HOLD"
        else:
            try:
                checks["phase2_eligibility"] = phase2_eligibility(
                    source_ref, service_id, binding, lifecycle_state
                )
            except Exception:
                checks["phase2_eligibility"] = False
            lifecycle_attestation = "ATTESTED"
    else:
        # Historical bindings without lifecycle attestation remain readable as LKG.
        # Automatic handoff independently requires a qualified CANDIDATE release.
        checks["lifecycle_eligibility"] = True
        checks["release_handoff_eligibility"] = True
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
        "lifecycle_attestation": lifecycle_attestation,
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
    services = sorted(
        str(sid)
        for sid, binding in bindings.items()
        if isinstance(binding, dict) and binding.get("status") == "active"
    )
    if not services:
        print(json.dumps({
            "schema": "source_provenance_gate_v2",
            "status": "FAIL",
            "services": {},
            "error_count": 1,
            "errors": {"registry": ["no active immutable Source bindings"]},
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    results = {sid: verify_binding(sid, bindings.get(sid) or {}) for sid in services}
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
