import pytest

from src.engine.distribution.path_resolver import EntityPathResolver


def test_provider_paths():
    assert EntityPathResolver.human_provider("acfun", "acfun_aggregate").as_posix() == "rule/acfun/acfun_aggregate/acfun_aggregate.yaml"
    assert EntityPathResolver.human_provider("apple").as_posix() == "rule/apple/apple/apple.yaml"


def test_service_paths():
    assert EntityPathResolver.human_service("apple", "appletv").as_posix() == "rule/apple/appletv/appletv.yaml"


def test_generated_paths():
    assert EntityPathResolver.generated_provider("mihomo", "acfun", "acfun_aggregate").as_posix() == "generated/mihomo/acfun/acfun_aggregate/acfun_aggregate"
    assert EntityPathResolver.generated_service("mihomo", "apple", "appletv").as_posix() == "generated/mihomo/apple/appletv/appletv"


def test_validation():
    with pytest.raises(RuntimeError):
        EntityPathResolver.validate_paths(["rule/apple/apple.yaml"])
    with pytest.raises(RuntimeError):
        EntityPathResolver.validate_paths(["rule/apple/apple/apple.yaml", "rule/apple/apple/apple.yaml"])
    result = EntityPathResolver.validate_paths(["rule/apple/apple/apple.yaml"])
    assert result["duplicate_paths"] == 0
    assert result["legacy_layout"] == 0
