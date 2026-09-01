from src.engine.core.models.entity import AggregateView, EntityGraph, Group, Service
from src.engine.hierarchy.resolver import expand_members

def test_expand_group():
    g = EntityGraph(
        services={"a": Service(id="a"), "b": Service(id="b")},
        groups={"g1": Group(id="g1", members=["a", "b"])},
        aggregates={"agg": AggregateView(id="agg", members=["g1"])},
    )
    assert expand_members(g, ["g1"]) == ["a", "b"]

def test_exclude():
    g = EntityGraph(
        services={"a": Service(id="a"), "b": Service(id="b")},
        groups={},
        aggregates={},
    )
    assert expand_members(g, ["a", "b"], exclude=["b"]) == ["a"]
