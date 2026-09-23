from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

from scripts import p0_service_production_gate as gate


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
