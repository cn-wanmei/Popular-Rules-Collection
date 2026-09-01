"""V3 Collection DAG: upstream acquisition before the V3 Engine DAG.

The collector keeps existing acquisition implementations as bounded leaf jobs,
but moves orchestration, retries, dependency tracking and a unified immutable
Collection Manifest into the V3 engine boundary.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.engine.dag.executor import Node, execute

ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class CollectionSpec:
    name: str
    command: tuple[str, ...]
    deps: tuple[str, ...] = ()
    critical: bool = True
    timeout_seconds: int = 3600
    retries: int = 2


COLLECTION_SPECS = (
    CollectionSpec(
        "validate_registry",
        (sys.executable, "scripts/validate_registry.py"),
    ),
    CollectionSpec(
        "service_rules",
        (sys.executable, "scripts/collect.py"),
        deps=("validate_registry",),
        critical=True,
    ),
    CollectionSpec(
        "validate_ip_registry",
        (sys.executable, "scripts/validate_ip_registry.py"),
        critical=True,
    ),
    CollectionSpec(
        "ip_rules",
        (sys.executable, "scripts/collect_ip.py"),
        deps=("validate_ip_registry",),
        critical=False,
    ),
    CollectionSpec(
        "validate_dataset_registry",
        (sys.executable, "scripts/validate_dataset_registry.py"),
        critical=True,
    ),
    CollectionSpec(
        "network_lan",
        (sys.executable, "scripts/build_network_lan.py"),
        deps=("validate_dataset_registry",),
        critical=True,
    ),
    CollectionSpec(
        "datasets",
        (sys.executable, "scripts/collect_datasets.py"),
        deps=("validate_dataset_registry", "network_lan"),
        critical=False,
    ),
    CollectionSpec(
        "network_datasets",
        (sys.executable, "scripts/build_network_datasets.py"),
        deps=("datasets",),
        critical=False,
    ),
    CollectionSpec(
        "providers",
        (sys.executable, "scripts/collect_providers.py"),
        deps=("validate_dataset_registry",),
        critical=False,
    ),
    CollectionSpec(
        "provider_datasets",
        (sys.executable, "scripts/build_provider_datasets.py"),
        deps=("providers",),
        critical=False,
    ),
)

COLLECTION_NODES = [Node(spec.name, spec.deps) for spec in COLLECTION_SPECS]
_SPEC_BY_NAME = {spec.name: spec for spec in COLLECTION_SPECS}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _tail(text: str, limit: int = 4000) -> str:
    return text[-limit:]


def _run_leaf(spec: CollectionSpec, *, date: str, skip_large: bool) -> dict[str, Any]:
    cmd = list(spec.command)
    env = None
    if spec.name == "service_rules":
        cmd.extend(("--date", date))
    if skip_large and spec.name == "service_rules":
        # collect.py itself has no semantic skip-large flag; Engine handles
        # mega-list filtering later. Keep the flag visible in the manifest.
        pass

    started = time.monotonic()
    attempts: list[dict[str, Any]] = []
    for attempt in range(1, spec.retries + 2):
        attempt_started = _utc_now()
        try:
            completed = subprocess.run(
                cmd,
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=spec.timeout_seconds,
                check=False,
            )
            record = {
                "attempt": attempt,
                "started_at": attempt_started,
                "returncode": completed.returncode,
                "stdout_tail": _tail(completed.stdout),
                "stderr_tail": _tail(completed.stderr),
            }
            attempts.append(record)
            if completed.returncode == 0:
                return {
                    "status": "ok",
                    "critical": spec.critical,
                    "attempts": attempts,
                    "duration_seconds": round(time.monotonic() - started, 3),
                }
        except subprocess.TimeoutExpired as exc:
            attempts.append(
                {
                    "attempt": attempt,
                    "started_at": attempt_started,
                    "returncode": None,
                    "timeout": spec.timeout_seconds,
                    "stdout_tail": _tail(exc.stdout or ""),
                    "stderr_tail": _tail(exc.stderr or ""),
                }
            )
        except OSError as exc:
            attempts.append(
                {
                    "attempt": attempt,
                    "started_at": attempt_started,
                    "returncode": None,
                    "error": str(exc),
                }
            )

    return {
        "status": "failed",
        "critical": spec.critical,
        "attempts": attempts,
        "duration_seconds": round(time.monotonic() - started, 3),
    }


def _collection_id(date: str, results: dict[str, Any]) -> str:
    stable = {
        "date": date,
        "nodes": {
            name: {
                "status": value.get("status"),
                "critical": value.get("critical"),
                "attempts": len(value.get("attempts", [])),
            }
            for name, value in sorted(results.items())
        },
    }
    digest = hashlib.sha256(json.dumps(stable, sort_keys=True).encode("utf-8")).hexdigest()[:20]
    return f"{date}-{digest}"


def run_collection(
    data_root: Path,
    *,
    date: str | None = None,
    skip_large: bool = False,
) -> dict[str, Any]:
    """Run the Collection DAG and write one day-level immutable manifest."""
    data_root = Path(data_root)
    date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_dir = ROOT / "backup" / date
    day_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir = day_dir / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    context: dict[str, Any] = {}

    def handler_for(spec: CollectionSpec):
        def _handler() -> dict[str, Any]:
            result = _run_leaf(spec, date=date, skip_large=skip_large)
            context[spec.name] = result
            return result
        return _handler

    handlers = {spec.name: handler_for(spec) for spec in COLLECTION_SPECS}
    result_map = execute(
        COLLECTION_NODES,
        handlers,
        max_workers=min(8, len(COLLECTION_NODES)),
        fail_fast=False,
        on_layer_complete=None,
    )

    critical_failures = [
        name for name, value in result_map.items()
        if _SPEC_BY_NAME[name].critical and value.get("status") != "ok"
    ]
    successful = [name for name, value in result_map.items() if value.get("status") == "ok"]
    degraded = [
        name for name, value in result_map.items()
        if not _SPEC_BY_NAME[name].critical and value.get("status") != "ok"
    ]
    collection_id = _collection_id(date, result_map)
    manifest = {
        "schema": "collection_manifest_v1",
        "collection_id": collection_id,
        "date": date,
        "created_at": _utc_now(),
        "root": str(day_dir.relative_to(ROOT)),
        "execution": {"mode": "dag", "max_workers": min(8, len(COLLECTION_NODES))},
        "status": "blocked" if critical_failures else ("degraded" if degraded else "ok"),
        "critical_failures": sorted(critical_failures),
        "degraded_nodes": sorted(degraded),
        "successful_nodes": sorted(successful),
        "skip_large": skip_large,
        "nodes": {
            name: {
                **value,
                "deps": list(_SPEC_BY_NAME[name].deps),
                "critical": _SPEC_BY_NAME[name].critical,
            }
            for name, value in sorted(result_map.items())
        },
    }
    payload = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    manifest_path = manifest_dir / "_collection.json"
    temp = manifest_path.with_name("._collection.json.tmp")
    temp.write_text(payload, encoding="utf-8")
    temp.replace(manifest_path)

    manifest["manifest_sha256"] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return manifest
