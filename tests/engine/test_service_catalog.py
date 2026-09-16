from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load(name: str):
    return yaml.safe_load((ROOT / "config" / name).read_text(encoding="utf-8"))


def test_candidate_pool_has_expected_scale_and_unique_ids():
    doc = _load("service_candidates.yaml")
    candidates = doc["candidates"]
    ids = [item["id"] for item in candidates]

    assert 100 <= len(candidates) <= 200
    assert len(ids) == len(set(ids))
    assert all(item["priority"] in {"P0", "P1", "P2"} for item in candidates)
    assert all(item["status"] in {"existing", "split", "planned", "deferred"} for item in candidates)


def test_p0_materialization_queue_has_exactly_fifty_services():
    doc = _load("p0_materialization.yaml")
    services = doc["services"]
    ids = [item["id"] for item in services]

    assert len(services) == 50
    assert len(ids) == len(set(ids))
    assert all(item.get("source_hints") for item in services)
