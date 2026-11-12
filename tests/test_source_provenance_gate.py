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
        "service_id": "qqmail", "snapshot_id": "snap-qqmail-test",
        "content_digest": "c" * 64, "evidence_digest": "d" * 64,
        "policy_digest": "e" * 64, "generator_digest": "f" * 64,
        "release_digest": "0" * 64, "release_identity_version": "2",
    }
    monkeypatch.setattr(gate, "get_json", lambda *args, **kwargs: release)
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
    }
    monkeypatch.setattr(gate, "get_json", lambda *args, **kwargs: release)
    monkeypatch.setattr(gate, "get_text", lambda url, *args, **kwargs: lifecycle_raw if url.endswith("config/source_canary_state.yaml") else body)

    result = gate.verify_binding("qqmail", binding)
    assert result["status"] == "FAIL"
    assert "lifecycle_eligibility" in result["failed_checks"]
