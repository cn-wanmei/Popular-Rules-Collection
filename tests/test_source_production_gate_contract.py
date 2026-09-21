from __future__ import annotations

from scripts.source_production_gate import PRODUCTION_REQUIRED


def test_production_gate_requires_observation_start_not_completion():
    assert "observation_started_at" in PRODUCTION_REQUIRED
    assert "observation_completed_at" not in PRODUCTION_REQUIRED
