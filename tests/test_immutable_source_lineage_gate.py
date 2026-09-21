from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from scripts.immutable_source_lineage_gate import main


def test_lineage_gate_accepts_exact_immutable_artifact(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    (repo / "sources").mkdir(parents=True)
    (repo / "backup/2026-09-21/manifests").mkdir(parents=True)
    (repo / "backup/2026-09-21/sources/popular-rules-source").mkdir(parents=True)

    body = b"example.org\n"
    digest = hashlib.sha256(body).hexdigest()
    (repo / "backup/2026-09-21/sources/popular-rules-source/PRS_qqmail.domains.txt").write_bytes(body)

    (repo / "sources/immutable_registry.yaml").write_text(
        yaml.safe_dump({
            "bindings": {"qqmail": {
                "status": "active",
                "source_ref": "a" * 40,
                "release_path": "releases/qqmail/snap/release.json",
                "snapshot_id": "snap-qqmail-test",
                "content_digest": "b" * 64,
                "expected_sha256": digest,
            }}
        }, sort_keys=False),
        encoding="utf-8",
    )
    (repo / "sources/registry.yaml").write_text(
        yaml.safe_dump({
            "sources": [{
                "id": "popular-rules-source",
                "rules": [{"service": "qqmail", "name": "qqmail", "path": "generated/source/qqmail/domains.txt", "enabled": True}],
            }]
        }, sort_keys=False),
        encoding="utf-8",
    )
    item = {
        "service": "qqmail",
        "path": "generated/source/qqmail/domains.txt",
        "status": "skipped",
        "sha256": digest,
        "cas_sha256": digest,
        "local": "sources/popular-rules-source/PRS_qqmail.domains.txt",
        "immutable": {
            "source_ref": "a" * 40,
            "release_path": "releases/qqmail/snap/release.json",
            "snapshot_id": "snap-qqmail-test",
            "content_digest": "b" * 64,
            "expected_sha256": digest,
        },
    }
    (repo / "backup/2026-09-21/manifests/popular-rules-source.json").write_text(
        json.dumps({"files": [item]}), encoding="utf-8"
    )
    (repo / "backup/2026-09-21/manifests/_collection.json").write_text(
        json.dumps({"status": "ok"}), encoding="utf-8"
    )

    import scripts.immutable_source_lineage_gate as gate
    monkeypatch.setattr(gate, "ROOT", repo)
    monkeypatch.setattr(gate, "REGISTRY", repo / "sources/registry.yaml")
    monkeypatch.setattr(gate, "IMMUTABLE", repo / "sources/immutable_registry.yaml")
    monkeypatch.setattr("sys.argv", ["gate", "--collection-root", "backup/2026-09-21"])
    assert main() == 0


def test_lineage_gate_rejects_digest_drift(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    (repo / "sources").mkdir(parents=True)
    (repo / "backup/2026-09-21/manifests").mkdir(parents=True)
    (repo / "backup/2026-09-21/sources/popular-rules-source").mkdir(parents=True)
    body = b"stale.example.org\n"
    actual = hashlib.sha256(body).hexdigest()
    expected = "a" * 64
    (repo / "backup/2026-09-21/sources/popular-rules-source/PRS_qqmail.domains.txt").write_bytes(body)

    (repo / "sources/immutable_registry.yaml").write_text(
        yaml.safe_dump({"bindings": {"qqmail": {
            "status": "active", "source_ref": "a"*40, "release_path": "r",
            "snapshot_id": "s", "content_digest": "b"*64, "expected_sha256": expected
        }}}, sort_keys=False), encoding="utf-8"
    )
    (repo / "sources/registry.yaml").write_text(
        yaml.safe_dump({"sources": [{"id":"popular-rules-source","rules":[{"service":"qqmail","name":"qqmail","path":"generated/source/qqmail/domains.txt","enabled":True}]}]}, sort_keys=False), encoding="utf-8"
    )
    (repo / "backup/2026-09-21/manifests/popular-rules-source.json").write_text(
        json.dumps({"files": [{"service":"qqmail","path":"generated/source/qqmail/domains.txt","status":"skipped","sha256":actual,"local":"sources/popular-rules-source/PRS_qqmail.domains.txt"}]}),
        encoding="utf-8"
    )
    (repo / "backup/2026-09-21/manifests/_collection.json").write_text(json.dumps({"status":"ok"}), encoding="utf-8")
    import scripts.immutable_source_lineage_gate as gate
    monkeypatch.setattr(gate, "ROOT", repo)
    monkeypatch.setattr(gate, "REGISTRY", repo / "sources/registry.yaml")
    monkeypatch.setattr(gate, "IMMUTABLE", repo / "sources/immutable_registry.yaml")
    monkeypatch.setattr("sys.argv", ["gate", "--collection-root", "backup/2026-09-21"])
    assert main() == 1
