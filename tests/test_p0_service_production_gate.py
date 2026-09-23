import hashlib
import subprocess
import sys
from pathlib import Path

from scripts import p0_service_production_gate as gate

ROOT = Path(__file__).resolve().parents[1]


def test_report_only_accepts_blocked_but_structurally_valid_queue():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "p0_service_production_gate.py"), "--report-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "p0=50" in result.stdout
    assert "blocked=50" in result.stdout


def test_release_gate_rejects_current_blocked_matrix():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "p0_service_production_gate.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode != 0
    assert "production=0" in result.stdout


def test_missing_independent_evidence_is_not_passable():
    errors = gate.evidence_errors_for_service("not_a_real_p0_service", {})
    assert any("no independent source/canonical/semantic/overlap evidence bundle" in e for e in errors)


def test_canonical_identity_is_recomputed_from_engine_function():
    identity_key = "host|apps.apple.com"
    expected = hashlib.sha256(identity_key.encode("utf-8")).hexdigest()
    assert expected == "1e98d9e8aa660f53d3c671acb5c8e3fa0555edf9686cb316ec07dd5248fbf9fe"


def test_complete_evidence_requires_real_snapshot_file_and_hash():
    bundle = {
        "1": {
            "source": {
                "services": {
                    "synthetic": {
                        "immutable_snapshot": {
                            "status": "complete",
                            "path": "config/does-not-exist.list",
                            "sha256": "0" * 64,
                        }
                    }
                }
            },
            "canonical": {"services": {"synthetic": {"status": "complete", "memberships": []}}},
            "semantic": {"services": {"synthetic": {"status": "pass", "snapshot": "config/does-not-exist.list", "probes": [{"kind": "positive_exact"}]}}},
            "overlap": {"status": "pass", "scope": {"services": ["synthetic"]}},
        }
    }
    errors = gate.evidence_errors_for_service("synthetic", bundle)
    assert any("snapshot file is missing" in e for e in errors)


def test_evidence_linkage_and_overlap_scope_are_required():
    bundle = {
        "1": {
            "source": {
                "services": {
                    "synthetic": {
                        "immutable_snapshot": {
                            "status": "complete",
                            "path": "config/p0_batch01_snapshots/2026-09-17/appstore.list",
                            "sha256": "f24026d879b22174d76aeddd89c0636740155d35",
                        }
                    }
                }
            },
            "canonical": {"services": {"synthetic": {"status": "complete", "snapshot": "wrong.list", "memberships": []}}},
            "semantic": {"services": {"synthetic": {"status": "pass", "snapshot": "wrong.list", "probes": [{"kind": "positive_exact"}]}}},
            "overlap": {"status": "pass", "scope": {"services": ["other"]}},
        }
    }
    errors = gate.evidence_errors_for_service("synthetic", bundle)
    assert any("canonical snapshot linkage mismatch" in e for e in errors)
    assert any("semantic snapshot linkage mismatch" in e for e in errors)
    assert any("overlap audit scope does not include service" in e for e in errors)


def test_service_client_artifact_prefers_hierarchical_layout(tmp_path: Path):
    hierarchical = tmp_path / "artifacts" / "mihomo" / "apple" / "appstore" / "appstore.yaml"
    hierarchical.parent.mkdir(parents=True)
    hierarchical.write_text("payload\n", encoding="utf-8")
    flat = tmp_path / "artifacts" / "mihomo" / "appstore.yaml"
    flat.write_text("legacy\n", encoding="utf-8")
    found = gate.service_client_artifact(tmp_path, "mihomo", ".yaml", "appstore", "apple")
    assert found == hierarchical


def test_service_client_artifact_falls_back_to_flat_layout(tmp_path: Path):
    flat = tmp_path / "artifacts" / "surge" / "appstore.list"
    flat.parent.mkdir(parents=True)
    flat.write_text("HOST,apps.apple.com\n", encoding="utf-8")
    found = gate.service_client_artifact(tmp_path, "surge", ".list", "appstore", "apple")
    assert found == flat


def test_service_client_artifact_discovers_nested_provider_path(tmp_path: Path):
    nested = tmp_path / "artifacts" / "loon" / "apple" / "appstore" / "appstore.list"
    nested.parent.mkdir(parents=True)
    nested.write_text("DOMAIN,apps.apple.com\n", encoding="utf-8")
    found = gate.service_client_artifact(tmp_path, "loon", ".list", "appstore", "")
    assert found == nested


def test_resolve_run_pins_explicit_run_id(tmp_path: Path, monkeypatch):
    older = tmp_path / "20260917T010000000000Z-run"
    newer = tmp_path / "20260917T120000000000Z-run"
    older.mkdir()
    newer.mkdir()
    monkeypatch.setattr(gate, "RUNS_DIR", tmp_path)
    assert gate.resolve_run("20260917T010000000000Z-run") == older
    assert gate.resolve_run(None) == newer


def test_report_only_with_pinned_missing_run_is_structural_failure():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p0_service_production_gate.py"),
            "--report-only",
            "--run-id",
            "does-not-exist-run",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode != 0
    assert "run not found" in result.stdout
