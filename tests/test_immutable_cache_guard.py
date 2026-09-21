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
