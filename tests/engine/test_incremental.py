from src.engine.dag.incremental import StageFingerprint, plan_incremental


def _complete():
    return {
        name: StageFingerprint(f"in-{name}", f"out-{name}", "v1")
        for name in ("snapshot", "ingest", "canonical", "hierarchy", "ir", "diff", "golden", "release", "promote")
    }


def _inputs():
    return {name: f"in-{name}" for name in _complete()}


def test_unchanged_pipeline_reuses_every_stage():
    assert plan_incremental(_complete(), _inputs(), contracts={name: "v1" for name in _complete()}) == ()


def test_canonical_change_rebuilds_only_its_transitive_dependents():
    inputs = _inputs()
    inputs["canonical"] = "changed"
    assert plan_incremental(_complete(), inputs) == ("canonical", "diff", "hierarchy", "ir", "golden", "release", "promote")


def test_contract_change_invalidates_stage_and_dependents():
    contracts = {name: "v1" for name in _complete()}
    contracts["ir"] = "v2"
    assert plan_incremental(_complete(), _inputs(), contracts=contracts) == ("ir", "golden", "release", "promote")


def test_missing_fingerprint_is_fail_closed():
    previous = _complete()
    del previous["golden"]
    assert "golden" in plan_incremental(previous, _inputs())
