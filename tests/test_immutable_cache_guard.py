from __future__ import annotations

import hashlib
from pathlib import Path

import scripts.collect as collect


def test_load_cached_rejects_immutable_digest_drift(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(collect, "ROOT", tmp_path)
    body = b"stale.example.org\\n"
    stale = tmp_path / "cached.txt"
    stale.write_bytes(body)
    actual = hashlib.sha256(body).hexdigest()
    expected = "a" * 64

    previous = {"local": "cached.txt", "sha256": actual}
    assert collect._load_cached(previous, expected_sha256=expected) is None
    assert collect._load_cached(previous, expected_sha256=actual) == (body, actual)


def test_immutable_binding_accepts_numeric_yaml_service_key(tmp_path: Path, monkeypatch) -> None:
    registry = tmp_path / "immutable_registry.yaml"
    registry.write_text(
        "bindings:\\n  1688:\\n    status: active\\n    expected_sha256: " + "a" * 64 + "\\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(collect, "IMMUTABLE_REGISTRY_PATH", registry)
    binding = collect.immutable_binding_for("1688")
    assert binding is not None
    assert binding["expected_sha256"] == "a" * 64
