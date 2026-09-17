from scripts.service_production_gate import validate


def test_service_production_gate_passes_current_identity_model():
    errors = validate()
    assert errors == [], "\n".join(errors)
