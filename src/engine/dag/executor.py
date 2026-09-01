"""Minimal deterministic DAG executor with dependency-aware parallel layers."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class Node:
    name: str
    deps: tuple[str, ...] = ()


def topological_layers(nodes: list[Node]) -> list[list[str]]:
    by_name = {n.name: n for n in nodes}
    if len(by_name) != len(nodes):
        raise ValueError("duplicate DAG node")
    remaining = set(by_name)
    done: set[str] = set()
    layers: list[list[str]] = []
    while remaining:
        ready = sorted(n for n in remaining if set(by_name[n].deps) <= done)
        if not ready:
            raise ValueError("DAG contains a cycle or unknown dependency")
        layers.append(ready)
        done.update(ready)
        remaining.difference_update(ready)
    return layers


def execute(nodes: list[Node], handlers: dict[str, Callable[[], Any]], max_workers: int = 8) -> dict[str, Any]:
    layers = topological_layers(nodes)
    results: dict[str, Any] = {}
    for layer in layers:
        missing = [name for name in layer if name not in handlers]
        if missing:
            raise KeyError(f"missing DAG handlers: {', '.join(missing)}")
        with ThreadPoolExecutor(max_workers=min(max_workers, len(layer)), thread_name_prefix="engine-dag") as pool:
            futures = {pool.submit(handlers[name]): name for name in layer}
            for future in as_completed(futures):
                name = futures[future]
                results[name] = future.result()
    return results
