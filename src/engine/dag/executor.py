"""Deterministic dependency-aware DAG executor with fail-closed semantics."""
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
    known = set(by_name)
    for node in nodes:
        unknown = set(node.deps) - known
        if unknown:
            raise ValueError(f"unknown dependency for {node.name}: {', '.join(sorted(unknown))}")
    remaining = set(by_name)
    done: set[str] = set()
    layers: list[list[str]] = []
    while remaining:
        ready = sorted(n for n in remaining if set(by_name[n].deps) <= done)
        if not ready:
            raise ValueError("DAG contains a cycle")
        layers.append(ready)
        done.update(ready)
        remaining.difference_update(ready)
    return layers


def execute(
    nodes: list[Node],
    handlers: dict[str, Callable[[], Any]],
    *,
    max_workers: int = 8,
    fail_fast: bool = False,
    on_layer_complete: Callable[[list[str], dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Execute a DAG in deterministic layers, optionally in parallel within each layer.

    A node returning ``{"status": "blocked"}`` is treated as failed for dependency
    propagation. Exceptions become ``failed`` results unless fail_fast=True.
    """
    by_name = {n.name: n for n in nodes}
    layers = topological_layers(nodes)
    results: dict[str, Any] = {}
    failed: set[str] = set()

    for layer in layers:
        ready: list[str] = []
        for name in layer:
            if any(dep in failed for dep in by_name[name].deps):
                results[name] = {"status": "skipped", "reason": "dependency_failed"}
                failed.add(name)
            elif name not in handlers:
                raise KeyError(f"missing DAG handler: {name}")
            else:
                ready.append(name)

        if ready:
            with ThreadPoolExecutor(max_workers=min(max_workers, len(ready)), thread_name_prefix="engine-dag") as pool:
                futures = {pool.submit(handlers[name]): name for name in ready}
                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        value = future.result()
                        results[name] = value
                        if isinstance(value, dict) and value.get("status") in {"blocked", "failed", "skipped"}:
                            failed.add(name)
                    except Exception as exc:
                        results[name] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
                        failed.add(name)
                        if fail_fast:
                            raise
        if on_layer_complete is not None:
            on_layer_complete(layer, results)
    return results
