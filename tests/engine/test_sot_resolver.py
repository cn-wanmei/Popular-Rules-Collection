from pathlib import Path

import pytest

from src.engine.sot.resolver import SoTResolver


def test_rule_tree_is_v1_source_of_truth(tmp_path: Path) -> None:
    service = tmp_path / "rule" / "Example"
    service.mkdir(parents=True)
    (service / "domain.yaml").write_text("example.com\n", encoding="utf-8")
    (tmp_path / "generated").mkdir()
    (tmp_path / "generated" / "Example.txt").write_text("projection", encoding="utf-8")

    result = SoTResolver(tmp_path).resolve("Example")

    assert result.source == "v1_rule"
    assert result.root == service
    assert result.files == (service / "domain.yaml",)


def test_generated_is_never_used_as_source(tmp_path: Path) -> None:
    generated = tmp_path / "generated" / "Example"
    generated.mkdir(parents=True)
    (generated / "rules.yaml").write_text("example.com\n", encoding="utf-8")

    result = SoTResolver(tmp_path).resolve("Example")

    assert result.source == "unresolved"
    assert not result.found


def test_service_name_cannot_escape_repository(tmp_path: Path) -> None:
    resolver = SoTResolver(tmp_path)
    with pytest.raises(ValueError):
        resolver.resolve("../database")
    with pytest.raises(ValueError):
        resolver.resolve("a/b")
