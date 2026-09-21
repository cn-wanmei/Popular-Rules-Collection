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
