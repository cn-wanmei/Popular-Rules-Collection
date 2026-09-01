from pathlib import Path

from src.engine.dag.executor import Node, execute


def test_resume_reuses_successful_nodes(tmp_path: Path):
    state = tmp_path / "dag.json"
    calls = []
    nodes = [Node("a"), Node("b", ("a",))]

    def a():
        calls.append("a")
        return {"status": "ok", "value": 1}

    def b():
        calls.append("b")
        return {"status": "ok", "value": 2}

    first = execute(nodes, {"a": a, "b": b}, state_path=state, input_digests={"a": "input-v1"})
    assert calls == ["a", "b"]
    calls.clear()
    second = execute(nodes, {"a": a, "b": b}, state_path=state, input_digests={"a": "input-v1"})
    assert calls == []
    assert second["a"]["resume"] == "reused"
    assert second["b"]["resume"] == "reused"
    assert first["a"]["output_digest"] == second["a"]["output_digest"]
    assert first["b"]["output_digest"] == second["b"]["output_digest"]


def test_resume_invalidates_downstream_when_input_changes(tmp_path: Path):
    state = tmp_path / "dag.json"
    calls = []
    nodes = [Node("a"), Node("b", ("a",))]
    execute(nodes, {"a": lambda: {"status": "ok", "value": 1}, "b": lambda: {"status": "ok", "value": 2}}, state_path=state, input_digests={"a": "input-v1"})

    def a():
        calls.append("a")
        return {"status": "ok", "value": 99}

    def b():
        calls.append("b")
        return {"status": "ok", "value": 2}

    result = execute(
        nodes,
        {"a": a, "b": b},
        state_path=state,
        input_digests={"a": "input-v2"},
    )
    assert calls == ["a", "b"]
    assert result["a"]["status"] == "ok"
    assert result["b"]["status"] == "ok"


def test_state_is_atomic_and_records_contract(tmp_path: Path):
    state = tmp_path / "nested" / "dag.json"
    execute([Node("a")], {"a": lambda: 3}, state_path=state)
    text = state.read_text(encoding="utf-8")
    assert "dag_resume_state_v1" in text
    assert "dag_node_v1" in text
    assert not state.with_suffix(".json.tmp").exists()
