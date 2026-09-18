from scripts import validate_registry


def test_validate_registry_passes_current_identity_model():
    assert validate_registry.main() == 0
