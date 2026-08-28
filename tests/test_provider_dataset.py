"""Provider dataset isolation: must not write database/ips/."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_provider_yaml_paths_not_ips():
    reg = ROOT / "sources" / "datasets" / "provider.yaml"
    assert reg.exists()
    doc = yaml.safe_load(reg.read_text(encoding="utf-8"))
    assert doc.get("kind") == "provider"
    for ds in doc.get("datasets") or []:
        path = str(ds.get("path") or "")
        assert not path.startswith("database/ips/"), path
        assert path.startswith("database/provider/") or not path


def test_collect_providers_hard_skip_logic():
    src = (ROOT / "scripts" / "collect_providers.py").read_text(encoding="utf-8")
    assert "database/ips/" in src
