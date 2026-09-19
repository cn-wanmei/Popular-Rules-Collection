from src.engine.pipeline.run import DAG_NODES, STAGES


def test_closure_stages_are_in_production_dag_order() -> None:
    assert STAGES.index("semantic_contract") > STAGES.index("ir")
    assert STAGES.index("observation") > STAGES.index("release")

    deps = {node.name: node.deps for node in DAG_NODES}
    assert deps["semantic_contract"] == ("ir",)
    assert deps["observation"] == ("release",)
