"""normalize must not clobber ip_registry maps_to sidecars."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import normalize  # noqa: E402


def test_ip_registry_targets_includes_china():
    targets = normalize._ip_registry_targets()
    assert "china" in targets
    assert "chinaunicom" in targets


def test_guard_present_in_source():
    src = (ROOT / "scripts" / "normalize.py").read_text(encoding="utf-8")
    assert "_ip_registry_targets" in src
    assert "skip ips overwrite" in src
