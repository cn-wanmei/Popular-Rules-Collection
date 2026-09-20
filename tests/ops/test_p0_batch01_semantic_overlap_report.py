from __future__ import annotations

import sys
from pathlib import Path

import scripts.p0_batch01_semantic_overlap_report as report


def test_blocked_semantic_state_fails_closed(tmp_path: Path, monkeypatch) -> None:
    semantic = tmp_path / "semantic.yaml"
    overlap = tmp_path / "overlap.yaml"
    semantic.write_text("{}\n", encoding="utf-8")
    overlap.write_text("{}\n", encoding="utf-8")

    monkeypatch.setattr(report, "SEMANTIC", semantic)
    monkeypatch.setattr(report, "OVERLAP", overlap)
    monkeypatch.setattr(
        report,
        "run_semantic",
        lambda _doc: ({"overall_status": "blocked", "services": {}}, {}),
    )
    monkeypatch.setattr(
        report,
        "run_overlap",
        lambda _doc, _service_rules, _semantic: {
            "status": "pass",
            "runtime_probe_count": 0,
            "runtime_collisions": [],
        },
    )
    monkeypatch.setattr(sys, "argv", ["p0_batch01_semantic_overlap_report.py"])

    assert report.main() == 0
