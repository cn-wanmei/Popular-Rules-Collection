"""Phase 8 — ordered migration gates."""
from __future__ import annotations

from pathlib import Path

import yaml

from src.engine.v1.phase8 import (
    INTENTIONAL_CODES,
    IntentionalEntry,
    compute_coverage,
    evaluate_phase8_gates,
    load_intentional_registry,
    request_legacy_delete,
    switch_sot_to_v1,
    validate_intentional_registry,
)


def test_intentional_codes_match_docs():
    assert "NO_UPSTREAM" in INTENTIONAL_CODES
    assert "COVERED_BY_AGGREGATE" in INTENTIONAL_CODES
    assert "MAPS_TO" in INTENTIONAL_CODES
    assert "DEFERRED_PROFILE" in INTENTIONAL_CODES
    assert "KEYWORD_ONLY" in INTENTIONAL_CODES
    assert "SOURCE_DRIFT" in INTENTIONAL_CODES


def test_validate_intentional_rejects_bad_code():
    reg = {"x": IntentionalEntry("x", "FAKE_CODE", "r")}
    errs = validate_intentional_registry(reg)
    assert errs


def test_coverage_100_when_all_covered():
    registered = {"a", "b", "c"}
    materialized = {"a", "b"}
    intentional = {
        "c": IntentionalEntry("c", "NO_UPSTREAM", "no upstream yet"),
    }
    report = compute_coverage(registered, materialized, intentional)
    assert report.at_100 is True
    assert report.missing == []
    assert report.coverage_pct == 100.0


def test_coverage_incomplete_lists_missing():
    registered = {"a", "b", "c"}
    materialized = {"a"}
    intentional = {}
    report = compute_coverage(registered, materialized, intentional)
    assert report.at_100 is False
    assert "b" in report.missing
    assert "c" in report.missing


def test_phase8_gates_block_when_coverage_low():
    cov = compute_coverage({"a", "b"}, {"a"}, {})
    report = evaluate_phase8_gates(cov)
    assert report.stage == "inventory"
    assert any(g.name == "coverage_100" and not g.passed for g in report.gates)
    assert report.legacy_delete_allowed is False


def test_phase8_ready_when_all_green():
    cov = compute_coverage(
        {"a", "b"},
        {"a"},
        {"b": IntentionalEntry("b", "NO_UPSTREAM", "pending")},
    )
    report = evaluate_phase8_gates(
        cov,
        unexplained_removed=[],
        intentional_valid=True,
        graph_ok=True,
        golden_ok=True,
        legacy_asset_equivalence_ok=True,
        client_regression_ok=True,
        deterministic_ok=True,
        production_run_ok=True,
        current_head_ok=True,
    )
    assert report.stage == "ready"
    assert report.to_dict()["all_pass"] is True
    assert report.sot == "legacy"


def test_switch_sot_requires_gates():
    cov = compute_coverage({"a"}, set(), {})
    report = evaluate_phase8_gates(cov)
    report = switch_sot_to_v1(report)
    assert report.sot == "legacy"
    assert any("refuse SoT switch" in e for e in report.errors)


def test_switch_sot_when_ready():
    cov = compute_coverage({"a"}, {"a"}, {})
    report = evaluate_phase8_gates(
        cov,
        golden_ok=True,
        graph_ok=True,
        legacy_asset_equivalence_ok=True,
        client_regression_ok=True,
        deterministic_ok=True,
        production_run_ok=True,
        current_head_ok=True,
    )
    assert report.stage == "ready"
    report = switch_sot_to_v1(report)
    assert report.sot == "v1_canonical"
    assert report.stage == "switched"
    assert report.legacy_delete_allowed is False


def test_legacy_delete_refuses_without_sot_switch():
    cov = compute_coverage({"a"}, {"a"}, {})
    report = evaluate_phase8_gates(cov)
    report = request_legacy_delete(report, allow_legacy_delete=True, final_gate_passed=True)
    assert report.legacy_deleted is False
    assert any("SoT is still" in e for e in report.errors)


def test_legacy_delete_refuses_without_flag():
    cov = compute_coverage({"a"}, {"a"}, {})
    report = evaluate_phase8_gates(cov)
    report = switch_sot_to_v1(report)
    report = request_legacy_delete(report, allow_legacy_delete=False)
    assert report.legacy_deleted is False
    assert any("allow_legacy_delete" in e for e in report.errors)


def test_legacy_delete_authorized_only_at_end():
    cov = compute_coverage({"a"}, {"a"}, {})
    report = evaluate_phase8_gates(cov)
    report = switch_sot_to_v1(report)
    report = request_legacy_delete(report, allow_legacy_delete=True)
    assert report.legacy_deleted is True
    assert report.stage == "legacy_deleted"


def test_load_intentional_from_yaml(tmp_path: Path):
    p = tmp_path / "intentional_unmaterialized.yaml"
    p.write_text(
        yaml.dump(
            {
                "version": 1,
                "services": {
                    "Foo": {"code": "NO_UPSTREAM", "reason": "test"},
                    "Bar": {"code": "MAPS_TO", "reason": "maps_to_baz"},
                },
            }
        ),
        encoding="utf-8",
    )
    reg = load_intentional_registry(p)
    assert "foo" in reg
    assert reg["foo"].code == "NO_UPSTREAM"
    assert validate_intentional_registry(reg) == []


def test_real_config_intentional_codes_if_present():
    root = Path(__file__).resolve().parents[2]
    cfg = root / "config" / "intentional_unmaterialized.yaml"
    if not cfg.exists():
        return
    reg = load_intentional_registry(cfg)
    errs = validate_intentional_registry(reg)
    assert errs == [], errs



def test_legacy_delete_refuses_without_final_gate():
    cov = compute_coverage({"a"}, {"a"}, {})
    report = evaluate_phase8_gates(
        cov,
        golden_ok=True,
        graph_ok=True,
        legacy_asset_equivalence_ok=True,
        client_regression_ok=True,
        deterministic_ok=True,
        production_run_ok=True,
        current_head_ok=True,
    )
    report = switch_sot_to_v1(report)
    report = request_legacy_delete(report, allow_legacy_delete=True, final_gate_passed=False)
    assert report.legacy_deleted is False
    assert any("final migration gate" in e for e in report.errors)
