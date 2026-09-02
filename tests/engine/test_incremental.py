from src.engine.dag.incremental import StageFingerprint, plan_incremental


def _complete(contract: str = "v1") -> dict[str, StageFingerprint]:
    from src.engine.dag.incremental import DEPENDENCIES

    return {
        stage: StageFingerprint(f"in-{stage}", f"out-{stage}", contract)
        for stage in DEPENDENCIES
    }


def _inputs() -> dict[str, str]:
    from src.engine.dag.incremental import DEPENDENCIES

    return {stage: f"in-{stage}" for stage in DEPENDENCIES}


def _contracts() -> dict[str, str]:
    from src.engine.dag.incremental import DEPENDENCIES

    return {stage: "v1" for stage in DEPENDENCIES}


def test_matching_fingerprints_reuse_every_stage():
    assert plan_incremental(_complete(), _inputs(), contracts=_contracts()) == ()


def test_changed_canonical_invalidates_all_transitive_dependents():
    inputs = _inputs()
    inputs["canonical"] = "new-input"
    assert plan_incremental(_complete(), inputs, contracts=_contracts()) == (
        "canonical",
        "diff",
        "hierarchy",
        "ir",
        "adapters",
        "golden",
        "observability",
        "cas",
        "release",
    )


def test_missing_contract_fails_closed():
    contracts = _contracts()
    del contracts["snapshot"]
    result = plan_incremental(_complete(), _inputs(), contracts=contracts)
    assert result == (
        "snapshot",
        "ingest",
        "quarantine",
        "canonical",
        "diff",
        "hierarchy",
        "ir",
        "adapters",
        "golden",
        "observability",
        "cas",
        "release",
    )


def test_missing_fingerprint_fails_closed():
    previous = _complete()
    del previous["golden"]
    assert "golden" in plan_incremental(previous, _inputs(), contracts=_contracts())


def test_deterministic_order_is_stable():
    first = plan_incremental(_complete(), {**_inputs(), "canonical": "x"}, contracts=_contracts())
    second = plan_incremental(_complete(), {**_inputs(), "canonical": "x"}, contracts=_contracts())
    assert first == second
