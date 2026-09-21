from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from scripts.phase2_collection_reconciliation import reconcile_service


def test_reconcile_service_binds_source_registry_input_and_ir(tmp_path: Path):
    source = tmp_path / "source"
    snap = source / "snapshots" / "snap-dingding"
    snap.mkdir(parents=True)
    domains = ["dingtalk.com", "oapi.dingtalk.com", "www.dingtalk.com"]
    manifest = {
        "schema": "source_snapshot_v2",
        "service_id": "dingding",
        "snapshot_id": "snap-dingding",
        "content_digest": "digest-123",
        "evidence_digest": "e" * 64,
        "policy_digest": "p" * 64,
        "generator_digest": "g" * 64,
        "release_digest": "r" * 64,
        "release_identity_version": "2",
        "domain_count": len(domains),
        "domains": domains,
        "release_state": "CANDIDATE",
        "created_at": "2026-09-21T00:00:00Z",
    }
    (snap / "domains.txt").write_text("\n".join(domains) + "\n", encoding="utf-8")
    (snap / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    release = source / "releases" / "dingding" / "snap-dingding"
    release.mkdir(parents=True)
    (release / "release.json").write_text(
        json.dumps({
            "snapshot_id": "snap-dingding", "content_digest": "digest-123",
            "evidence_digest": "e" * 64, "policy_digest": "p" * 64,
            "generator_digest": "g" * 64, "release_digest": "r" * 64,
            "release_identity_version": "2",
        }),
        encoding="utf-8",
    )

    root = tmp_path / "collection"
    (root / "sources").mkdir(parents=True)
    (root / "sources" / "registry.yaml").write_text(
        yaml.safe_dump(
            {
                "sources": [{
                    "id": "popular-rules-source",
                    "enabled": False,
                    "rules": [{
                        "service": "dingding",
                        "path": "generated/source/dingding/domains.txt",
                        "enabled": True,
                    }],
                }]
            }
        ),
        encoding="utf-8",
    )

    canary = tmp_path / "canary" / "dingding"
    (canary / "input" / "services").mkdir(parents=True)
    (canary / "data" / "runs" / "canary-dingding-release-2" / "ir").mkdir(parents=True)
    (canary / "input" / "source-binding.json").write_text(
        json.dumps({
            "repository": "cn-wanmei/Popular-Rules-Source",
            "source_commit": "abc",
            "service_id": "dingding",
            "snapshot_id": "snap-dingding",
            "content_digest": "digest-123",
            "evidence_digest": "e" * 64,
            "policy_digest": "p" * 64,
            "generator_digest": "g" * 64,
            "release_digest": "r" * 64,
            "release_identity_version": "2",
            "domain_count": 3,
            "seed_only_count": 0,
        }),
        encoding="utf-8",
    )
    (canary / "input" / "services" / "dingding.yaml").write_text(
        yaml.safe_dump(
            {"id": "dingding", "rules": [{"type": "domain", "value": value} for value in domains]}
        ),
        encoding="utf-8",
    )
    (canary / "data" / "runs" / "canary-dingding-release-2" / "ir" / "ir.json").write_text(
        json.dumps({"rules": [{"type": "domain", "value": value} for value in domains]}),
        encoding="utf-8",
    )

    # Monkeypatch repository root used by the module.
    import scripts.phase2_collection_reconciliation as mod
    monkey = {"ROOT": root}
    original = mod.ROOT
    mod.ROOT = root
    try:
        report = reconcile_service(
            "dingding", source, canary, "abc", "canary-dingding-release-2", "snap-dingding"
        )
    finally:
        mod.ROOT = original

    assert report["status"] == "PASS"
    assert report["run_id"].startswith("reconcile-dingding-")
    assert report["checks"]["v3_ir_exact"] is True
    expected_domain_digest = hashlib.sha256(
        json.dumps(domains, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    assert report["domain_digest"] == expected_domain_digest
