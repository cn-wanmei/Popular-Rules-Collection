"""Contract smoke for V3 imports + optional artifacts."""
from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def test_v3_artifacts_or_skip():
    manifest = ROOT / "data" / "v3" / "canonical" / "manifest.json"
    if not manifest.exists() and os.environ.get("V3_FORCE_PIPELINE") != "1":
        return
    if manifest.exists():
        import json
        m = json.loads(manifest.read_text())
        assert m.get("unique_rules", 0) > 0

def test_v3_import_paths():
    from src.v3.core.models.rule import identity_key
    from src.v3.decision.engine import decide_for_service
    assert identity_key("domain", "X.COM") == "domain|x.com"
    assert decide_for_service("google").action == "PROXY"
    assert decide_for_service("china").action == "DIRECT"
