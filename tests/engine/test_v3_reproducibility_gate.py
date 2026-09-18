from __future__ import annotations

from scripts.v3_reproducibility_gate import main


def test_reproducibility_gate_entrypoint_exists():
    assert callable(main)
