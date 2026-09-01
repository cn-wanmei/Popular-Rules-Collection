"""P0-1: V2 Runtime Dependency = 0 — Canonical builds only from Snapshot ingest."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from src.engine.ingest.source_ingest import ingest_snapshot, IngestError
from src.engine.canonical.store import build_canonical, load_rules, load_memberships


def _make_snapshot(tmp: Path, with_bad: bool = False) -> Path:
    snap = tmp / "snap-20260901T120000Z"
    sources = snap / "sources" / "services"
    sources.mkdir(parents=True)
    (snap / "manifest.json").write_text(json.dumps({
        "snapshot_id": "snap-20260901T120000Z",
        "created_at": "2026-09-01T12:00:00Z",
    }), encoding="utf-8")

    good = {
        "id": "google-gmail",
        "category": "mail",
        "source": ["upstream-a"],
        "rules": [
            {"type": "DOMAIN", "value": "mail.google.com"},
            {"type": "DOMAIN-SUFFIX", "value": "gmail.com"},
        ],
    }
    (sources / "google-gmail.yaml").write_text(
        "id: google-gmail\ncategory: mail\nsource: [upstream-a]\nrules:\n"
        "  - type: DOMAIN\n    value: mail.google.com\n"
        "  - type: DOMAIN-SUFFIX\n    value: gmail.com\n",
        encoding="utf-8",
    )

    if with_bad:
        (sources / "bad.yaml").write_text(
            "id: bad\nrules:\n  - type: DOMAIN\n    # missing value\n  - not_a_dict\n",
            encoding="utf-8",
        )
    return snap


def test_ingest_and_canonical_no_v2():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        snap = _make_snapshot(tmp)
        result = ingest_snapshot(snap)
        assert result["stats"]["records"] == 2
        assert result["stats"]["errors"] == 0
        assert "v2" not in str(result).lower() or "v2_runtime" not in str(result)

        out = tmp / "canonical"
        manifest = build_canonical(result, out)
        assert manifest["v2_runtime_dependency"] == 0
        assert manifest["source"] == "engine_ingest_snapshot"
        assert manifest["unique_rules"] == 2
        assert manifest["errors"] == 0

        rules = load_rules(out)
        assert len(rules) == 2
        mem = load_memberships(out)
        assert "google-gmail" in mem
        assert len(mem["google-gmail"]) == 2


def test_canonical_never_silent_drop():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        snap = _make_snapshot(tmp, with_bad=True)
        result = ingest_snapshot(snap)
        # bad rules recorded as errors, not silently dropped
        assert result["stats"]["errors"] >= 1

        out = tmp / "canonical"
        manifest = build_canonical(result, out)
        assert manifest["errors"] >= 1
        err_path = out / "errors.jsonl"
        assert err_path.exists()
        lines = [l for l in err_path.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) >= 1


def test_missing_snapshot_raises():
    with tempfile.TemporaryDirectory() as td:
        with pytest.raises(IngestError):
            ingest_snapshot(Path(td) / "nonexistent")
