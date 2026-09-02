"""Deterministic audit primitives used by the P3 rule compiler.

The module intentionally uses only the Python standard library so audit output can
be generated in CI before optional packaging/build dependencies are installed.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ACTION_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s]+)\s*$")
PIN_RE = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")


def _read_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if isinstance(obj, dict) and obj.get("id") is not None:
            rows[str(obj["id"])] = obj
    return rows


def _semantic_view(row: Mapping[str, Any]) -> dict[str, Any]:
    """Keep fields that affect rule meaning; ignore volatile metadata."""
    keys = ("value", "classification", "action", "match", "policy", "type", "tags")
    return {k: row.get(k) for k in keys if k in row}


def semantic_rule_diff(current: Path, baseline: Path | None) -> dict[str, Any]:
    """Return an audit-friendly semantic diff between two canonical JSONL files."""
    cur = _read_jsonl(Path(current))
    old = _read_jsonl(Path(baseline)) if baseline else {}
    added = sorted(set(cur) - set(old))
    removed = sorted(set(old) - set(cur))
    changed = sorted(k for k in set(cur) & set(old) if _semantic_view(cur[k]) != _semantic_view(old[k]))
    return {
        "schema": "rule_semantic_diff_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {"added": len(added), "removed": len(removed), "changed": len(changed)},
        "added_ids": added,
        "removed_ids": removed,
        "changed_ids": changed,
        "baseline_present": bool(old),
    }


def adapter_capability_matrix(adapters: Mapping[str, Mapping[str, Any]], required: Iterable[str]) -> dict[str, Any]:
    """Evaluate adapter feature coverage without a second compatibility schema."""
    req = sorted(set(required))
    result: dict[str, Any] = {"schema": "adapter_capability_matrix_v1", "required": req, "adapters": {}}
    for name, info in sorted(adapters.items()):
        supported = set(info.get("capabilities", []))
        missing = sorted(set(req) - supported)
        result["adapters"][name] = {
            "capabilities": sorted(supported),
            "missing": missing,
            "ready": not missing,
            "version": info.get("version"),
        }
    return result


def source_health_score(source: Mapping[str, Any], now: datetime | None = None) -> dict[str, Any]:
    """Score a source from explicit health signals; missing signals do not invent failures."""
    now = now or datetime.now(timezone.utc)
    score = 100.0
    status = int(source.get("http_status", 200))
    latency = float(source.get("latency_ms", 0) or 0)
    errors = int(source.get("error_count", 0) or 0)
    freshness = source.get("fetched_at")
    if not 200 <= status < 400:
        score -= 40
    if latency > 2000:
        score -= min(20, (latency - 2000) / 250)
    score -= min(25, errors * 5)
    age_hours = None
    if freshness:
        dt = datetime.fromisoformat(str(freshness).replace("Z", "+00:00"))
        age_hours = max(0.0, (now - dt).total_seconds() / 3600)
        if age_hours > 168:
            score -= min(20, (age_hours - 168) / 24)
    score = round(max(0.0, min(100.0, score)), 2)
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D"
    return {"schema": "source_health_v1", "score": score, "grade": grade, "age_hours": age_hours,
            "signals": {"http_status": status, "latency_ms": latency, "error_count": errors}}


def build_provenance_graph(events: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Build a small DAG suitable for audit inspection and reverse tracing."""
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []
    for event in events:
        source = event.get("source")
        artifact = event.get("artifact")
        stage = event.get("stage", "transform")
        if source:
            nodes.setdefault(f"source:{source}", {"type": "source", "name": source})
        if artifact:
            nodes.setdefault(f"artifact:{artifact}", {"type": "artifact", "name": artifact})
        if source and artifact:
            edges.append({"from": f"source:{source}", "to": f"artifact:{artifact}", "stage": str(stage)})
        parent = event.get("parent")
        if parent and artifact:
            nodes.setdefault(f"artifact:{parent}", {"type": "artifact", "name": parent})
            edges.append({"from": f"artifact:{parent}", "to": f"artifact:{artifact}", "stage": str(stage)})
    return {"schema": "provenance_graph_v1", "nodes": list(nodes.values()), "edges": edges}


def write_checksum_manifest(root: Path, output: Path) -> dict[str, Any]:
    """Write reproducible SHA-256 checksums for files below root."""
    root = Path(root)
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.resolve() == Path(output).resolve():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append({"path": str(path.relative_to(root)), "sha256": digest, "bytes": path.stat().st_size})
    data = {"schema": "artifact_checksum_v1", "algorithm": "sha256", "files": rows}
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data


def generate_sbom(lockfile: Path, output: Path) -> dict[str, Any]:
    """Generate a compact CycloneDX JSON SBOM from an exact-pinned lock file."""
    components = []
    for raw in Path(lockfile).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            raise ValueError(f"Unlocked dependency in {lockfile}: {line}")
        name, version = line.split("==", 1)
        components.append({
            "type": "library", "name": name, "version": version,
            "purl": f"pkg:pypi/{name}@{version}",
        })
    doc = {"bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
           "metadata": {"timestamp": datetime.now(timezone.utc).isoformat()}, "components": components}
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc


def dependency_lock_report(lockfile: Path) -> dict[str, Any]:
    """Reject non-pinned entries and duplicate package names in the repository lock."""
    entries = []
    for raw in Path(lockfile).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line or line.count("==") != 1:
            entries.append({"line": line, "valid": False})
            continue
        name, version = line.split("==", 1)
        entries.append({"name": name, "version": version, "valid": bool(name and version)})
    names = [e["name"].lower() for e in entries if e.get("valid")]
    duplicates = sorted({n for n in names if names.count(n) > 1})
    invalid = [e for e in entries if not e.get("valid")]
    return {"schema": "dependency_lock_v1", "locked": not invalid and not duplicates,
            "entry_count": len(entries), "invalid": invalid, "duplicates": duplicates}


def verify_action_shas(workflow_root: Path) -> dict[str, Any]:
    """Enforce immutable 40-hex SHA pins for every GitHub Action reference."""
    violations = []
    references = []
    for path in sorted(Path(workflow_root).rglob("*.yml")) + sorted(Path(workflow_root).rglob("*.yaml")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = ACTION_RE.match(line)
            if not match:
                continue
            ref = match.group(1)
            references.append({"file": str(path), "line": lineno, "uses": ref})
            if not PIN_RE.match(ref):
                violations.append({"file": str(path), "line": lineno, "uses": ref})
    return {"schema": "action_sha_verification_v1", "pass": not violations,
            "reference_count": len(references), "violations": violations}


def write_release_manifest(output: Path, *, version: str, commit: str, artifacts: Path,
                           sbom: Path, checksums: Path, semantic_diff: Mapping[str, Any] | None = None,
                           provenance: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Create an auditable release manifest linking all verifiable release inputs."""
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
    manifest = {
        "schema": "release_manifest_v1",
        "version": version,
        "commit": commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": str(artifacts),
        "sbom": {"path": str(sbom), "sha256": digest(sbom)},
        "checksums": {"path": str(checksums), "sha256": digest(checksums)},
        "semantic_diff": semantic_diff or {},
        "provenance": provenance or {},
        "rollback": {"strategy": "checkout_commit", "commit": commit},
    }
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest
