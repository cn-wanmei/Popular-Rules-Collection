"""Capability matrix gap-code contract."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_matrix_runs_and_has_version():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "client_capability_matrix.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    report = ROOT / "reports" / "latest_client_capability.json"
    assert report.exists()
    doc = json.loads(report.read_text(encoding="utf-8"))
    ids = [m["dataset"] for m in doc["matrix"]]
    assert "geosite_policy" in ids, f"expected geosite_policy in {ids}"
    assert "asn_metadata" in ids, f"expected asn_metadata in {ids}"
    cfg = yaml.safe_load(
        (ROOT / "config" / "client_capabilities.yaml").read_text(encoding="utf-8")
    )
    cfg_ver = int(cfg.get("version") or 0)
    assert cfg_ver >= 2, f"config client_capabilities version must be >=2, got {cfg_ver}"
    report_ver = int(doc.get("version") or 0)
    assert report_ver == cfg_ver, f"report version {report_ver} != config {cfg_ver}"


def test_no_capability_for_mmdb_on_surge():
    doc = json.loads((ROOT / "reports" / "latest_client_capability.json").read_text())
    row = next(m for m in doc["matrix"] if m["dataset"] == "geoip_mmdb")
    assert row["clients"]["surge"]["gap"] == "no_capability"
