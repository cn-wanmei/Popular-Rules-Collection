from __future__ import annotations

from scripts.source_provenance_gate import verify_binding


def test_provenance_gate_accepts_complete_v2_binding(monkeypatch):
    binding = {
        "status": "active",
        "source_id": "popular-rules-source",
        "source_ref": "a" * 40,
        "verified_input_commit": "b" * 40,
        "artifact_path": "generated/source/qqmail/domains.txt",
        "release_path": "releases/qqmail/snap-qqmail-test/release.json",
        "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64,
        "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64,
        "generator_digest": "f" * 64,
        "release_digest": "0" * 64,
        "release_identity_version": "2",
        "expected_sha256": "1" * 64,
    }

    release = {
        "service_id": "qqmail",
        "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64,
        "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64,
        "generator_digest": "f" * 64,
        "release_digest": "0" * 64,
        "release_identity_version": "2",
    }
    body = b"example.org\n"

    import scripts.source_provenance_gate as gate
    monkeypatch.setattr(gate, "get_json", lambda *args, **kwargs: release)
    monkeypatch.setattr(gate, "get_text", lambda *args, **kwargs: body)
    binding["expected_sha256"] = __import__("hashlib").sha256(body).hexdigest()

    result = verify_binding("qqmail", binding)
    assert result["status"] == "PASS"
    assert all(result["checks"].values())


def test_provenance_gate_rejects_release_identity_drift(monkeypatch):
    binding = {
        "status": "active",
        "source_id": "popular-rules-source",
        "source_ref": "a" * 40,
        "verified_input_commit": "b" * 40,
        "artifact_path": "generated/source/qqmail/domains.txt",
        "release_path": "releases/qqmail/snap-qqmail-test/release.json",
        "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64,
        "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64,
        "generator_digest": "f" * 64,
        "release_digest": "0" * 64,
        "release_identity_version": "2",
        "expected_sha256": "1" * 64,
    }

    import scripts.source_provenance_gate as gate
    monkeypatch.setattr(gate, "get_json", lambda *args, **kwargs: {
        "service_id": "qqmail",
        "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64,
        "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64,
        "generator_digest": "f" * 64,
        "release_digest": "9" * 64,
        "release_identity_version": "2",
    })
    monkeypatch.setattr(gate, "get_text", lambda *args, **kwargs: b"example.org\n")

    result = verify_binding("qqmail", binding)
    assert result["status"] == "FAIL"
    assert "release_digest" in result["failed_checks"]



def test_provenance_gate_verifies_exact_lifecycle_attestation(monkeypatch):
    import hashlib
    import json
    import scripts.source_provenance_gate as gate

    source_ref = "a" * 40
    body = b"example.org\\n"
    lifecycle = {
        "schema": "popular_rules_source_lifecycle_v1",
        "services": {"qqmail": {"state": "verified", "enabled": True}},
    }
    lifecycle_raw = json.dumps(lifecycle, sort_keys=True).encode("utf-8")
    binding = {
        "status": "active",
        "source_id": "popular-rules-source",
        "source_ref": source_ref,
        "verified_input_commit": "b" * 40,
        "artifact_path": "generated/source/qqmail/domains.txt",
        "release_path": "releases/qqmail/snap-qqmail-test/release.json",
        "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64,
        "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64,
        "generator_digest": "f" * 64,
        "release_digest": "0" * 64,
        "release_identity_version": "2",
        "expected_sha256": hashlib.sha256(body).hexdigest(),
        "lifecycle_ref": source_ref,
        "lifecycle_state": "verified",
        "lifecycle_config_sha256": hashlib.sha256(lifecycle_raw).hexdigest(),
    }
    release = {
        "validation": {"release_state": "CANDIDATE"},
        "service_id": "qqmail", "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": "0" * 64, "release_identity_version": "2",
    }
    phase2 = {
        "schema": "phase2_service_completion_derived_v1",
        "services": {"qqmail": {
            "blockers": [], "verified": True, "declared_state": "verified",
            "snapshot_id": "snap-qqmail-test", "release_digest": "0" * 64,
            "production_activated": False,
        }},
    }
    def fake_get_json(url, *args, **kwargs):
        return phase2 if url.endswith("phase2_service_completion.json") else release
    monkeypatch.setattr(gate, "get_json", fake_get_json)
    def fake_get_text(url, *args, **kwargs):
        if url.endswith("config/source_canary_state.yaml"):
            return lifecycle_raw
        return body
    monkeypatch.setattr(gate, "get_text", fake_get_text)

    result = gate.verify_binding("qqmail", binding)
    assert result["status"] == "PASS"
    assert result["lifecycle_attestation"] == "ATTESTED"
    assert result["checks"]["lifecycle_eligibility"] is True


def test_provenance_gate_rejects_review_lifecycle_attestation(monkeypatch):
    import hashlib
    import json
    import scripts.source_provenance_gate as gate

    source_ref = "a" * 40
    body = b"example.org\\n"
    lifecycle = {
        "schema": "popular_rules_source_lifecycle_v1",
        "services": {"qqmail": {"state": "review", "enabled": True}},
    }
    lifecycle_raw = json.dumps(lifecycle, sort_keys=True).encode("utf-8")
    binding = {
        "status": "active", "source_id": "popular-rules-source",
        "source_ref": source_ref, "verified_input_commit": "b" * 40,
        "artifact_path": "generated/source/qqmail/domains.txt",
        "release_path": "releases/qqmail/snap-qqmail-test/release.json",
        "snapshot_id": "snap-qqmail-test", "content_digest": "c" * 64,
        "evidence_digest": "d" * 64, "policy_digest": "e" * 64,
        "generator_digest": "f" * 64, "release_digest": "0" * 64,
        "release_identity_version": "2",
        "expected_sha256": hashlib.sha256(body).hexdigest(),
        "lifecycle_ref": source_ref, "lifecycle_state": "review",
        "lifecycle_config_sha256": hashlib.sha256(lifecycle_raw).hexdigest(),
    }
    release = {
        "validation": {"release_state": "CANDIDATE"},
        "service_id": "qqmail", "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": "0" * 64, "release_identity_version": "2",
    }
    phase2 = {
        "schema": "phase2_service_completion_derived_v1",
        "services": {"qqmail": {
            "blockers": [], "verified": True, "declared_state": "review",
            "snapshot_id": "snap-qqmail-test", "release_digest": "0" * 64,
            "production_activated": False,
        }},
    }
    def fake_get_json(url, *args, **kwargs):
        return phase2 if url.endswith("phase2_service_completion.json") else release
    monkeypatch.setattr(gate, "get_json", fake_get_json)
    monkeypatch.setattr(gate, "get_text", lambda url, *args, **kwargs: lifecycle_raw if url.endswith("config/source_canary_state.yaml") else body)

    result = gate.verify_binding("qqmail", binding)
    assert result["status"] == "FAIL"
    assert "lifecycle_eligibility" in result["failed_checks"]



def test_phase2_lkg_exceptions_are_exact_and_service_scoped():
    from scripts.source_provenance_gate import is_exact_phase2_lkg

    source_refs = [
        "f5a3291c5020368f886064bcca026c836801ba3d",
        "4452ae321d306efef7cd45e67310adbd749195f9",
    ]
    pinned = {
        "1688": ("snap-1688-222302f3a20ecb7c08c72ed0", "222302f3a20ecb7c08c72ed09a2942e0ae41aa83c1a0086b47ddd9c0679ac776"),
        "cainiao": ("snap-cainiao-a8a898392298ebaa644a783e", "a8a898392298ebaa644a783ed30f4f5dc994c4245e175974ad71a3552b9293d8"),
        "dingding": ("snap-dingding-09ae1ecd000f1688f61e99a0", "09ae1ecd000f1688f61e99a07f7c36fae8ad0dbd7c9287f8857344ec6e3a70ad"),
        "taobao": ("snap-taobao-834d549e8982036ce1438963", "834d549e8982036ce1438963983527791e70997603616758bac4fb8f7c29d38b"),
        "tencentcloud": ("snap-tencentcloud-e55bc8c508e839813ae20cd0", "e55bc8c508e839813ae20cd04f7af034fd4b76745c5ee1efc49b14b3ca57a7b8"),
        "tiktok": ("snap-tiktok-d7c408670d9f72fda616937c", "d7c408670d9f72fda616937c2419e8311119b1827bdb34848a2d6748e3a934e6"),
        "tmall": ("snap-tmall-17de7049e2f7bf67cb88c785", "17de7049e2f7bf67cb88c7859d6d071375e89173e148cbceee484925843f8a90"),
    }
    for sid, (snapshot_id, release_digest) in pinned.items():
        binding = {"snapshot_id": snapshot_id, "release_digest": release_digest}
        for source_ref in source_refs:
            assert is_exact_phase2_lkg(sid, source_ref, binding)
            assert not is_exact_phase2_lkg(sid, source_ref, {**binding, "snapshot_id": snapshot_id + "-changed"})
            assert not is_exact_phase2_lkg(sid, source_ref, {**binding, "release_digest": "0" * 64})
        assert not is_exact_phase2_lkg(sid, "a" * 40, binding)


def test_release_handoff_qualification_is_candidate_only():
    from scripts.source_provenance_gate import release_handoff_eligible

    assert release_handoff_eligible({"validation": {"release_state": "CANDIDATE"}})
    assert release_handoff_eligible({"validation": {"release_state": "CANDIDATE", "handoff_eligible": True}})
    assert not release_handoff_eligible({"validation": {"release_state": "REVIEW"}})
    assert not release_handoff_eligible({"validation": {"release_state": "CANDIDATE", "handoff_eligible": False}})
    assert not release_handoff_eligible({})
