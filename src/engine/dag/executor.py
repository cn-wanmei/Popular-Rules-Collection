"""Deterministic dependency-aware DAG executor with resumable node state."""
from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from time import monotonic
from typing import Callable, Any

DAG_CONTRACT_VERSION = "dag_node_v1"

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
    remaining, done, layers = set(by_name), set(), []
    while remaining:
        ready = sorted(n for n in remaining if set(by_name[n].deps) <= done)
        if not ready:
            raise ValueError("DAG contains a cycle")
        layers.append(ready)
        done.update(ready)
        remaining.difference_update(ready)
    return layers

def _stable(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _stable(v) for k, v in sorted(value.items()) if k not in {"duration_ms", "resume", "output_digest"}}
    if isinstance(value, list):
        return [_stable(v) for v in value]
    return value

def _digest(value: Any) -> str:
    payload = json.dumps(_stable(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def _task_identity(node: Node) -> str:
    return _digest({"name": node.name, "deps": list(node.deps), "contract_version": DAG_CONTRACT_VERSION})

def _input_digest(node: Node, results: dict[str, Any], input_digests: dict[str, str] | None) -> str:
    return _digest({"task_identity": _task_identity(node), "deps": {dep: results[dep] for dep in node.deps}, "input": input_digests.get(node.name) if input_digests else None})

def _with_evidence(value: Any, started: float, node: Node, input_digest: str) -> Any:
    result = dict(value) if isinstance(value, dict) else {"status": "ok", "value": value}
    result.setdefault("duration_ms", round((monotonic() - started) * 1000, 3))
    result["task_identity"] = _task_identity(node)
    result["contract_version"] = DAG_CONTRACT_VERSION
    result["input_digest"] = input_digest
    result["output_digest"] = _digest(result)
    return result

def _load_state(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}

def _save_state(path: Path | None, results: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema": "dag_resume_state_v1", "contract_version": DAG_CONTRACT_VERSION, "nodes": results}
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)

def _resumable(previous: dict[str, Any], task_identity: str, input_digest: str) -> bool:
    return (
        isinstance(previous, dict) and previous.get("status") == "ok"
        and previous.get("task_identity") == task_identity
        and previous.get("contract_version") == DAG_CONTRACT_VERSION
        and previous.get("input_digest") == input_digest
        and isinstance(previous.get("output_digest"), str)
        and previous.get("output_digest") == _digest(previous)
    )

def execute(
    nodes: list[Node],
    handlers: dict[str, Callable[[], Any]],
    *,
    max_workers: int = 8,
    fail_fast: bool = False,
    on_layer_complete: Callable[[list[str], dict[str, Any]], None] | None = None,
    state_path: Path | None = None,
    input_digests: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Execute a DAG with atomic per-layer checkpoints and compatible resume."""
    by_name = {n.name: n for n in nodes}
    layers = topological_layers(nodes)
    state = _load_state(Path(state_path) if state_path else None)
    previous = state.get("nodes", {}) if isinstance(state.get("nodes", {}), dict) else {}
    results, failed = {}, set()
    for layer in layers:
        ready = []
        for name in layer:
            node = by_name[name]
            if any(dep in failed for dep in node.deps):
                results[name] = {"status": "skipped", "reason": "dependency_failed", "task_identity": _task_identity(node), "contract_version": DAG_CONTRACT_VERSION}
                failed.add(name)
                continue
            if name not in handlers:
                raise KeyError(f"missing DAG handler: {name}")
            inp = _input_digest(node, results, input_digests)
            cached = previous.get(name)
            if _resumable(cached, _task_identity(node), inp):
                results[name] = dict(cached)
                results[name]["resume"] = "reused"
                results[name]["duration_ms"] = 0.0
            else:
                ready.append(name)
        if ready:
            with ThreadPoolExecutor(max_workers=min(max_workers, len(ready)), thread_name_prefix="engine-dag") as pool:
                futures = {pool.submit(handlers[name]): (name, monotonic(), _input_digest(by_name[name], results, input_digests)) for name in ready}
                for future in as_completed(futures):
                    name, started, inp = futures[future]
                    try:
                        value = _with_evidence(future.result(), started, by_name[name], inp)
                        results[name] = value
                        if value.get("status") in {"blocked", "failed", "skipped"}:
                            failed.add(name)
                    except Exception as exc:
                        results[name] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}", "duration_ms": round((monotonic() - started) * 1000, 3), "task_identity": _task_identity(by_name[name]), "contract_version": DAG_CONTRACT_VERSION, "input_digest": inp}
                        failed.add(name)
                        if fail_fast:
                            raise
        _save_state(Path(state_path) if state_path else None, results)
        if on_layer_complete is not None:
            on_layer_complete(layer, results)
    return results
