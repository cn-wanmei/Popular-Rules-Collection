"""P0-3 … P0-10 core assertions plus V3 adapter contract."""
from __future__ import annotations

import tempfile
from pathlib import Path

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
        "  - type: DOMAIN\n    value: mail.google.com\n", encoding="utf-8")
    (src / "google-drive.yaml").write_text(
        "id: google-drive\ncategory: storage\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: drive.google.com\n", encoding="utf-8")
    return tmp / "sources"


def test_full_p0_flow():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        sources = _sources(tmp)
        data = tmp / "data"
        result = run_pipeline(sources, data)
        assert result["v2_runtime_dependency"] == 0
        assert result["status"] == "ok"
        run_id = result["run_id"]
        run_dir = data / "runs" / run_id
        ir_dir = run_dir / "ir"
        art = run_dir / "artifacts"

        report = build_all_clients(ir_dir, art)
        assert report["v2_runtime_dependency"] == 0
        assert report["source_contract"] == "semantic_ir_v2"
        for client, meta in CLIENTS.items():
            cdir = art / client
            assert cdir.exists()
            assert list(cdir.glob(f"*{meta['ext']}"))

        assert "google-gmail" in report["views"]["services"]
        assert (art / "mihomo" / "google-gmail.yaml").exists()
        assert (art / "singbox" / "google-gmail.json").exists()
        assert (art / "egern" / "google-gmail.yaml").exists()

        diff_dir = run_dir / "reports" / "diff"
        baseline = data / "runs" / run_id / "reports" / "diff" / "baseline.json"
        d1 = run_diff(run_dir / "canonical", None, diff_dir)
        assert (diff_dir / "latest.json").exists()
        assert (diff_dir / "differential.json").exists()
        assert d1["added"] == 3
        promote_baseline(run_dir / "canonical", baseline)
        d2 = run_diff(run_dir / "canonical", baseline, diff_dir)
        assert d2["added"] == d2["removed"] == d2["changed"] == 0


def test_rule_id_full_sha256():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        result = run_pipeline(_sources(tmp), tmp / "data")
        rules = load_rules(tmp / "data" / "runs" / result["run_id"] / "canonical")
        assert all(len(rid) == 64 for rid in rules)
