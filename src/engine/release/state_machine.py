"""Release State Machine — hard gates before promotion."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from src.engine.cas.run_store import verify_run


class ReleaseState(str, Enum):
    BUILDING = "BUILDING"
    VALIDATING = "VALIDATING"
    GOLDEN = "GOLDEN"
    RC_READY = "RC_READY"
    RELEASE_ARTIFACT = "RELEASE_ARTIFACT"
    PUBLISH = "PUBLISH"
    PRODUCTION = "PRODUCTION"
    BLOCKED = "BLOCKED"


def _sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _dir_sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_dir():
        return None
    items: list[tuple[str, str]] = []
    for file in sorted(path.rglob("*")):
        if file.is_file() and file.suffix in {".yaml", ".json", ".list"}:
            items.append((str(file.relative_to(path)), _sha256(file) or ""))
    return hashlib.sha256(json.dumps(items, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest() if items else None


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def evaluate_release(run_dir: Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    gates: dict[str, bool] = {}
    run_manifest = _load_json(run_dir / "run_manifest.json")
    v2_ok = run_manifest.get("v2_runtime_dependency") == 0
    snapshot_id = run_manifest.get("snapshot_id")
    if not snapshot_id:
        sid_path = run_dir / "snapshot_id.txt"
        snapshot_id = sid_path.read_text(encoding="utf-8").strip() if sid_path.exists() else None
    gates["v2_runtime_dependency_zero"] = v2_ok
    gates["snapshot_present"] = bool(snapshot_id)

    golden = _load_json(run_dir / "golden" / "report.json")
    gates["golden_all_pass"] = golden.get("all_pass") is True
    canonical_rules = run_dir / "canonical" / "rules.jsonl"
    gates["canonical_present"] = (run_dir / "canonical" / "manifest.json").exists() and canonical_rules.exists() and canonical_rules.stat().st_size > 0
    gates["ir_present"] = (run_dir / "ir" / "manifest.json").exists() and (run_dir / "ir" / "ir.json").exists()
    gates["artifacts_present"] = (run_dir / "artifacts").exists()
    gates["diff_present"] = (run_dir / "reports" / "diff" / "latest.json").exists()

    quality = _load_json(run_dir / "quality.json")
    gates["quality_all_hard_pass"] = quality.get("all_hard_pass") is True and quality.get("decision") == "PASS"
    metrics = _load_json(run_dir / "metrics" / "metrics.json")
    gates["parser_coverage_present"] = bool(metrics.get("parser_coverage"))
    gates["source_health_present"] = bool(metrics.get("source_health"))

    required_clients = {"mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon"}
    artifacts_root = run_dir / "artifacts"
    actual_clients = {p.name for p in artifacts_root.iterdir() if p.is_dir()} if artifacts_root.exists() else set()
    gates["seven_clients_present"] = required_clients.issubset(actual_clients)

    cas_verified = False
    cas_manifest = run_dir / "cas-manifest.json"
    if cas_manifest.exists():
        try:
            cas_verified = verify_run(run_dir, run_dir.parents[1] / "cas" / "objects")["verified"]
        except Exception:
            cas_verified = False
    gates["cas_integrity"] = cas_verified

    all_hard = all(gates.values())
    state = ReleaseState.RC_READY if all_hard else ReleaseState.BLOCKED
    now = datetime.now(timezone.utc).isoformat()
    report = {
        "schema": "release_state_v4",
        "generated_at": now,
        "state": state.value,
        "gates": gates,
        "all_hard_pass": all_hard,
        "v2_runtime_dependency": 0,
        "snapshot_id": snapshot_id,
        "quality_score": quality.get("score"),
        "cas_verified": cas_verified,
        "can_publish": state == ReleaseState.RC_READY,
    }
    release_dir = run_dir / "release"
    release_dir.mkdir(parents=True, exist_ok=True)
    (release_dir / "state.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    release_manifest = {
        "schema": "release_manifest_v3",
        "release_id": run_dir.name,
        "run_id": run_dir.name,
        "snapshot_id": snapshot_id,
        "release_state": state.value,
        "generated_at": now,
        "canonical_digest": _sha256(canonical_rules),
        "ir_digest": _sha256(run_dir / "ir" / "ir.json"),
        "golden_digest": _sha256(run_dir / "golden" / "report.json"),
        "diff_digest": _sha256(run_dir / "reports" / "diff" / "latest.json"),
        "quality_digest": _sha256(run_dir / "quality.json"),
        "metrics_digest": _sha256(run_dir / "metrics" / "metrics.json"),
        "client_digests": {client: _dir_sha256(artifacts_root / client) for client in sorted(required_clients)},
        "v2_runtime_dependency": 0,
    }
    (release_dir / "manifest.json").write_text(json.dumps(release_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
