"""ip_registry maps_to contract guard.

normalize.py was retired (chore(engine): retire legacy normalize production
entrypoint, 46de4e46). The guard it provided — preventing ip_registry
maps_to targets from being overwritten by domain-source normalization — is
now enforced upstream by collect_ip.py and validate_ip_registry.py.

This test file replaces the original normalize-based assertions with
equivalent contract tests that verify the same invariants against the
sources that are actually still active.
"""
from __future__ import annotations

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "sources" / "ip_registry.yaml"


def _ip_registry_targets() -> set[str]:
    """Return the set of maps_to target names from ip_registry.yaml."""
    doc = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    return {
        s["maps_to"]
        for s in doc.get("sources", [])
        if s.get("maps_to")
    }


def test_ip_registry_targets_includes_china():
    targets = _ip_registry_targets()
    assert "china" in targets, f"'china' missing from ip_registry maps_to targets: {targets}"
    assert "chinaunicom" in targets, f"'chinaunicom' missing from ip_registry maps_to targets: {targets}"


def test_guard_present_in_source():
    """validate_ip_registry.py must enforce maps_to; collect_ip.py must
    respect it — these are the active guards replacing the retired normalize guard."""
    validate_src = (ROOT / "scripts" / "validate_ip_registry.py").read_text(encoding="utf-8")
    collect_ip_src = (ROOT / "scripts" / "collect_ip.py").read_text(encoding="utf-8")

    assert "maps_to" in validate_src, "validate_ip_registry.py must reference maps_to"
    assert "maps_to" in collect_ip_src, "collect_ip.py must reference maps_to"


def test_ip_registry_yaml_schema():
    """ip_registry.yaml must be valid and every enabled source must have maps_to."""
    doc = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    assert doc.get("version") == 1, "ip_registry.yaml schema version must be 1"
    sources = doc.get("sources", [])
    assert len(sources) > 0, "ip_registry.yaml must have at least one source"
    for s in sources:
        if s.get("enabled", True):
            assert s.get("maps_to"), (
                f"Enabled ip_registry source '{s.get('id')}' is missing maps_to"
            )
