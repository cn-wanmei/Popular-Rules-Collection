"""P0-3 … P0-10 core assertions (independent V3)."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from src.engine.pipeline.run import run_pipeline
from src.engine.adapters.build_all import build_all_clients
from src.engine.adapters.registry import CLIENTS
from src.engine.diff.engine import run_diff, promote_baseline
from src.engine.canonical.store import load_rules


def _sources(tmp: Path) -> Path:
    src = tmp / "sources" / "services"
    src.mkdir(parents=True)
    (src / "google-gmail.yaml").write_text(
        "id: google-gmail\ncategory: mail\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: gmail.com\n"
        "  - type: DOMAIN\n    value: mail.google.com\n",
        encoding="utf-8",
    )
    (src / "google-drive.yaml").write_text(
        "id: google-drive\ncategory: storage\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: drive.google.com\n",
        encoding="utf-8",
    )
    return tmp / "sources"


def test_full_p0_flow():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        sources = _sources(tmp)
        data = tmp / "data"
        result = run_pipeline(sources, data)
        assert result["v2_runtime_dependency"] == 0
        run_id = result["run_id"]
        can_dir = data / "runs" / run_id / "canonical"

        # P0-6 native adapters + P0-7 service views
        art = data / "runs" / run_id / "artifacts"
        report = build_all_clients(can_dir, art)
        assert report["v2_runtime_dependency"] == 0
        for client, meta in CLIENTS.items():
            cdir = art / client
            assert cdir.exists()
            # correct extension present
            assert list(cdir.glob(f"*{meta['ext']}"))
            # no wrong universal .list for singbox / egern
            if meta["ext"] != ".list":
                assert not list(cdir.glob("*.list")) or client in ("surge", "shadowrocket", "quantumultx", "loon")

        # service views exist
        assert "google-gmail" in report["views"]["services"]
        assert (art / "mihomo" / "google-gmail.yaml").exists()
        assert (art / "singbox" / "google-gmail.json").exists()
        assert (art / "egern" / "google-gmail.yaml").exists()

        # P0-5 unified diff path + safe baseline
        diff_dir = data / "runs" / run_id / "reports" / "diff"
        d1 = run_diff(can_dir, None, diff_dir)
        assert (diff_dir / "latest.json").exists()
        assert (diff_dir / "differential.json").exists()  # compatibility
        assert d1["added"] == 3  # 3 unique rules

        # promote only after "release"
        baseline = data / "runs" / run_id / "reports" / "diff" / "baseline.json"
        promote_baseline(can_dir, baseline)
        assert baseline.exists()

        # second diff against promoted baseline → stable
        d2 = run_diff(can_dir, baseline, diff_dir)
        assert d2["added"] == 0
        assert d2["removed"] == 0
        assert d2["changed"] == 0


def test_rule_id_full_sha256():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        sources = _sources(tmp)
        data = tmp / "data"
        result = run_pipeline(sources, data)
        can_dir = data / "runs" / result["run_id"] / "canonical"
        rules = load_rules(can_dir)
        for rid in rules:
            assert len(rid) == 64  # full sha256 hex
