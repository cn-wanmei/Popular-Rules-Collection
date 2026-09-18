import json
from pathlib import Path
from src.engine.legacy_finalization.finalizer import finalize_legacy
def _write(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path
def test_legacy_finalization_requires_all_evidence(tmp_path: Path) -> None:
    regression = _write(tmp_path / "regression.json", {"all_pass": True, "unexplained_removed": []})
    equivalence = _write(tmp_path / "equivalence.json", {"passed": True, "at_100": True})
    reconciliation = _write(tmp_path / "reconciliation.json", {"summary": {
        "metadata_only_services": 0, "orphan_list_files": 0, "duplicate_domain_services": 0,
        "duplicate_ip_services": 0, "domain_count_delta_services": 0, "ip_count_delta_services": 0
    }, "promotion": {"blocked": True}})
    report = finalize_legacy(regression, equivalence_report=equivalence, reconciliation_report=reconciliation)
    assert report["all_pass"] is True
    assert report["migration_blocked"] is True
def test_legacy_finalization_blocks_unexplained_removal(tmp_path: Path) -> None:
    regression = _write(tmp_path / "regression.json", {"all_pass": False, "unexplained_removed": ["domain:lost.example"]})
    equivalence = _write(tmp_path / "equivalence.json", {"passed": True, "at_100": True})
    reconciliation = _write(tmp_path / "reconciliation.json", {"summary": {
        "metadata_only_services": 0, "orphan_list_files": 0, "duplicate_domain_services": 0,
        "duplicate_ip_services": 0, "domain_count_delta_services": 0, "ip_count_delta_services": 0
    }, "promotion": {"blocked": True}})
    report = finalize_legacy(regression, equivalence_report=equivalence, reconciliation_report=reconciliation)
    assert report["all_pass"] is False
    assert "legacy_regression_not_final" in report["blockers"]
def test_legacy_finalization_never_unblocks_promotion(tmp_path: Path) -> None:
    regression = _write(tmp_path / "regression.json", {"all_pass": True, "unexplained_removed": []})
    report = finalize_legacy(regression)
    assert report["migration_blocked"] is True
