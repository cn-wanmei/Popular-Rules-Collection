from __future__ import annotations

from scripts.phase2_exit_preflight import evaluate


def _production(service: str) -> dict:
    attestation = {
        "status": "passed",
        "source_release": f"releases/{service}/release.json",
        "snapshot_id": f"snap-{service}",
        "content_digest": "a" * 64,
        "reconciliation_run_id": f"reconcile-{service}",
        "v3_run_id": f"canary-{service}-release-2",
        "semantic_run_id": f"canary-{service}-release-2",
        "rollback_run_id": f"rollback-{service}",
        "observation_run_id": f"observe-{service}",
        "observation_started_at": "2026-09-21T00:00:00+00:00",
        "production_unlock_run_id": "123",
        "reconciliation_pass": True,
        "seven_client_semantic_pass": True,
        "rollback_pass": True,
        "observation_pass": True,
        "source_official_evidence_only": True,
        "seed_only_count": 0,
        "conflict_count": 0,
    }
    return {"state": "production", "enabled": True, "attestation": attestation}


def test_phase2_exit_preflight_blocks_nonproduction_service():
    state = {"services": {service: _production(service) for service in (
        "1688", "cainiao", "dingding", "qqmail", "qqmusic", "taobao", "tencentcloud", "tmall"
    )}}
    state["services"]["taobao"]["state"] = "canary"
    immutable = {"bindings": {service: {
        "status": "active",
        "source_ref": "a" * 40,
        "snapshot_id": f"snap-{service}",
        "content_digest": "b" * 64,
        "artifact_path": f"generated/source/{service}/domains.txt",
        "release_path": f"releases/{service}/release.json",
    } for service in state["services"]}}
    result = evaluate(state, immutable)
    assert result["status"] == "BLOCKED"
    assert "taobao" in result["blockers"]
    assert result["population"]["production_services"] == 7


def test_phase2_exit_preflight_passes_all_evidence_bound_production_services():
    services = ("1688", "cainiao", "dingding", "qqmail", "qqmusic", "taobao", "tencentcloud", "tmall")
    state = {"services": {service: _production(service) for service in services}}
    immutable = {"bindings": {service: {
        "status": "active",
        "source_ref": "a" * 40,
        "snapshot_id": f"snap-{service}",
        "content_digest": "b" * 64,
        "artifact_path": f"generated/source/{service}/domains.txt",
        "release_path": f"releases/{service}/release.json",
    } for service in services}}
    result = evaluate(state, immutable)
    assert result["status"] == "PASS"
    assert result["exit_ready"] is True
