from __future__ import annotations

from scripts.v1_final_migration_gate import audit_legacy_equivalence


def test_legacy_asset_equivalence_passes_at_100_percent():
    legacy = [
        {"service": "a", "type": "domain", "value": "a.example.com"},
        {"service": "a", "type": "ip_cidr", "value": "10.0.0.0/8"},
    ]
    report = audit_legacy_equivalence(legacy, list(legacy), {"a": 2}, {"a": 2}, set())
    assert report["at_100"] is True
    assert report["passed"] is True


def test_legacy_asset_equivalence_detects_loss():
    legacy = [{"service": "a", "type": "domain", "value": "gone.example.com"}]
    report = audit_legacy_equivalence(legacy, [], {"a": 1}, {}, set())
    assert report["at_100"] is False
    assert report["passed"] is False
    assert "a" in report["missing_assets"]
