from __future__ import annotations

from pathlib import Path

from src.engine import __version__
from src.engine.v1.phase8 import IntentionalEntry, compute_coverage


def test_phase8_coverage_does_not_double_count_materialized_intentional():
    report = compute_coverage(
        {"a", "b", "c"},
        {"a", "b"},
        {
            "b": IntentionalEntry("b", "DEFERRED_PROFILE", "materialized but retained in registry"),
            "c": IntentionalEntry("c", "NO_UPSTREAM", "no upstream"),
        },
    )
    assert report.registered == 3
    assert report.materialized == 2
    assert report.intentional == 1
    assert report.details["intentional_only"] == ["c"]
    assert report.details["materialized_and_intentional"] == ["b"]
    assert report.coverage_pct == 100.0


def test_version_is_single_engine_ssot():
    root = Path(__file__).resolve().parents[2]
    assert (root / "VERSION").read_text(encoding="utf-8").strip() == __version__


def test_publish_status_manifest_lookup_uses_collection_manifest_path():
    script = (Path(__file__).resolve().parents[2] / "scripts" / "generate_publish_status.py").read_text(encoding="utf-8")
    assert 'directory / "manifests" / "_collection.json"' in script


def test_release_manifest_declares_baseline_evidence():
    script = (Path(__file__).resolve().parents[2] / "src" / "engine" / "release" / "state_machine.py").read_text(encoding="utf-8")
    assert '"baseline_evidence_digest"' in script


def test_promotion_cli_has_no_dead_force_flag():
    cli = (Path(__file__).resolve().parents[2] / "src" / "engine" / "cli" / "__main__.py").read_text(encoding="utf-8")
    assert "--force" not in cli
    assert "force=" not in cli


def test_ir_uses_engine_version_ssot():
    path = Path(__file__).resolve().parents[2] / "src" / "engine" / "ir" / "builder.py"
    text = path.read_text(encoding="utf-8")
    assert '"engine_version": __version__' in text


def test_phase0_doc_exists():
    path = Path(__file__).resolve().parents[2] / "docs" / "PHASE0_CONTROL_PLANE.md"
    data = path.read_text(encoding="utf-8")
    assert "V1 runtime cutover" in data


def test_version_file_is_valid_semver():
    value = (Path(__file__).resolve().parents[2] / "VERSION").read_text(encoding="utf-8").strip()
    parts = value.split(".")
    assert len(parts) == 3 and all(part.isdigit() for part in parts)
