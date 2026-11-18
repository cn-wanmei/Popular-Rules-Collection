from __future__ import annotations

from scripts.source_provenance_gate import release_handoff_eligible, verify_binding


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
        "validation": {"release_state": "CANDIDATE"},
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
        "validation": {"release_state": "CANDIDATE"},
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
        "service_id": "qqmail", "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": "0" * 64, "release_identity_version": "2",
        "validation": {"release_state": "CANDIDATE"},
    }
    phase2 = {
        "schema": "phase2_service_completion_derived_v1",
        "services": {"qqmail": {
            "verified": True, "blockers": [], "declared_state": "verified",
            "production_activated": False, "snapshot_id": "snap-qqmail-test",
            "release_digest": "0" * 64,
        }},
    }
    monkeypatch.setattr(
        gate, "get_json",
        lambda url, *args, **kwargs: phase2 if "phase2_service_completion.json" in url else release,
    )
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
        "service_id": "qqmail", "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": "0" * 64, "release_identity_version": "2",
        "validation": {"release_state": "CANDIDATE"},
    }
    phase2 = {
        "schema": "phase2_service_completion_derived_v1",
        "services": {"qqmail": {
            "verified": False, "blockers": ["release_state:REVIEW"],
            "declared_state": "review", "production_activated": False,
            "snapshot_id": "snap-qqmail-test", "release_digest": "0" * 64,
        }},
    }
    monkeypatch.setattr(
        gate, "get_json",
        lambda url, *args, **kwargs: phase2 if "phase2_service_completion.json" in url else release,
    )
    monkeypatch.setattr(gate, "get_text", lambda url, *args, **kwargs: lifecycle_raw if url.endswith("config/source_canary_state.yaml") else body)

    result = gate.verify_binding("qqmail", binding)
    assert result["status"] == "FAIL"
    assert "lifecycle_eligibility" in result["failed_checks"]



def test_provenance_gate_rejects_phase2_state_drift_even_when_lifecycle_says_production(monkeypatch):
    import hashlib
    import json
    import scripts.source_provenance_gate as gate

    source_ref = "a" * 40
    body = b"example.org\\n"
    lifecycle = {
        "schema": "popular_rules_source_lifecycle_v1",
        "services": {"taobao": {"state": "production", "enabled": True}},
    }
    lifecycle_raw = json.dumps(lifecycle, sort_keys=True).encode("utf-8")
    binding = {
        "status": "active", "source_id": "popular-rules-source",
        "source_ref": source_ref, "verified_input_commit": "b" * 40,
        "artifact_path": "generated/source/taobao/domains.txt",
        "release_path": "releases/taobao/snap-taobao-test/release.json",
        "snapshot_id": "snap-taobao-test", "content_digest": "c" * 64,
        "evidence_digest": "d" * 64, "policy_digest": "e" * 64,
        "generator_digest": "f" * 64, "release_digest": "0" * 64,
        "release_identity_version": "2",
        "expected_sha256": hashlib.sha256(body).hexdigest(),
        "lifecycle_ref": source_ref, "lifecycle_state": "production",
        "lifecycle_config_sha256": hashlib.sha256(lifecycle_raw).hexdigest(),
    }
    release = {
        "service_id": "taobao", "snapshot_id": "snap-taobao-test",
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": "0" * 64, "release_identity_version": "2",
        "validation": {"release_state": "CANDIDATE"},
    }
    phase2 = {
        "schema": "phase2_service_completion_derived_v1",
        "services": {"taobao": {
            "verified": False,
            "blockers": ["release_state:REVIEW", "declared_production_without_verified_evidence"],
            "declared_state": "production", "production_activated": False,
            "snapshot_id": "snap-taobao-test", "release_digest": "0" * 64,
        }},
    }
    monkeypatch.setattr(
        gate, "get_json",
        lambda url, *args, **kwargs: phase2 if "phase2_service_completion.json" in url else release,
    )
    monkeypatch.setattr(
        gate, "get_text",
        lambda url, *args, **kwargs: lifecycle_raw if url.endswith("config/source_canary_state.yaml") else body,
    )

    result = gate.verify_binding("taobao", binding)
    assert result["status"] == "FAIL"
    assert result["checks"]["lifecycle_eligibility"] is True
    assert result["checks"]["phase2_eligibility"] is False
    assert "phase2_eligibility" in result["failed_checks"]



def test_provenance_gate_preserves_only_exact_pinned_taobao_lkg_tuple(monkeypatch):
    import hashlib
    import json
    import scripts.source_provenance_gate as gate

    source_ref = "f5a3291c5020368f886064bcca026c836801ba3d"
    body = b"taobao.example.org\\n"
    lifecycle = {
        "schema": "popular_rules_source_lifecycle_v1",
        "services": {"taobao": {"state": "production", "enabled": True}},
    }
    lifecycle_raw = json.dumps(lifecycle, sort_keys=True).encode("utf-8")
    binding = {
        "status": "active", "source_id": "popular-rules-source",
        "source_ref": source_ref, "verified_input_commit": "338ef57418768779aeb712f03ddb387545e375a2",
        "artifact_path": "generated/source/taobao/domains.txt",
        "release_path": "releases/taobao/snap-taobao-834d549e8982036ce1438963/release.json",
        "snapshot_id": "snap-taobao-834d549e8982036ce1438963",
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": "834d549e8982036ce1438963983527791e70997603616758bac4fb8f7c29d38b",
        "release_identity_version": "2",
        "expected_sha256": hashlib.sha256(body).hexdigest(),
        "lifecycle_ref": source_ref, "lifecycle_state": "production",
        "lifecycle_config_sha256": hashlib.sha256(lifecycle_raw).hexdigest(),
    }
    release = {
        "service_id": "taobao", "snapshot_id": binding["snapshot_id"],
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": binding["release_digest"], "release_identity_version": "2",
        "validation": {"release_state": "CANDIDATE"},
    }
    monkeypatch.setattr(gate, "get_json", lambda *args, **kwargs: release)
    monkeypatch.setattr(
        gate, "get_text",
        lambda url, *args, **kwargs: lifecycle_raw if url.endswith("config/source_canary_state.yaml") else body,
    )

    result = gate.verify_binding("taobao", binding)
    assert result["status"] == "PASS"
    assert result["lifecycle_attestation"] == "LEGACY_LKG_PHASE2_HOLD"
    assert result["checks"]["phase2_eligibility"] is True

    # The same service on a new Source ref must not inherit the LKG exception.
    binding["source_ref"] = "a" * 40
    binding["lifecycle_ref"] = "a" * 40
    result = gate.verify_binding("taobao", binding)
    assert result["status"] == "FAIL"
    assert result["checks"]["phase2_eligibility"] is False



def test_release_handoff_eligibility_accepts_candidate_and_rejects_review() -> None:
    assert release_handoff_eligible({"validation": {"release_state": "CANDIDATE"}})
    assert release_handoff_eligible({"validation": {"release_state": "CANDIDATE", "handoff_eligible": True}})
    assert not release_handoff_eligible({"validation": {"release_state": "REVIEW", "handoff_eligible": False}})
    assert not release_handoff_eligible({"validation": {"release_state": "CANDIDATE", "handoff_eligible": False}})
    assert not release_handoff_eligible({})
