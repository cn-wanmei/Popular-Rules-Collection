from __future__ import annotations

from scripts.source_canary_gate import validate_state


def _policy():
    return {"prs": {"enabled": False}, "canary": {"enabled": False}}


def _state(*rows):
    return {
        "services": {
            sid: {"state": state, "enabled": enabled, "attestation": {"status": "pending"}}
            for sid, state, enabled in rows
        }
    }


def test_single_canary_is_allowed():
    result = validate_state(
        _state(
            ("1688", "canary", True),
            ("cainiao", "verified", False),
        ),
        _policy(),
    )
    assert result["status"] == "PASS"
    assert result["canary_services"] == ["1688"]


def test_multiple_canaries_fail_closed():
    result = validate_state(
        _state(
            ("1688", "canary", True),
            ("cainiao", "canary", True),
        ),
        _policy(),
    )
    assert result["status"] == "FAIL"
    assert any(
        "at most one service may be state=canary at a time" in error
        for error in result["errors"]
    )


def test_verified_service_cannot_be_enabled():
    result = validate_state(
        _state(("1688", "verified", True)),
        _policy(),
    )
    assert result["status"] == "FAIL"
    assert "1688: verified must keep enabled=false" in result["errors"]
