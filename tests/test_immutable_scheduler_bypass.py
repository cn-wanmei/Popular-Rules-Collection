from __future__ import annotations

from pathlib import Path
import scripts.collect as collect


def test_immutable_binding_is_active(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "immutable.yaml"
    path.write_text(
        "bindings:\n  1688:\n    status: active\n    expected_sha256: %s\n" % ("a" * 64),
        encoding="utf-8",
    )
    monkeypatch.setattr(collect, "IMMUTABLE_REGISTRY_PATH", path)
    binding = collect.immutable_binding_for("1688")
    assert binding is not None
    assert binding["status"] == "active"
    assert binding["expected_sha256"] == "a" * 64
