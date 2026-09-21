# Phase 2 canary runner
#!/usr/bin/env python3
"""Phase 2 per-service Source -> V3 canary and rollback rehearsal."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from src.engine.pipeline import STAGES, run_pipeline
from src.engine.promote.artifact import promote_run, rollback_to_run
from scripts.phase2_collection_reconciliation import reconcile_service
from scripts.phase2_observation import start_observation


ROOT = Path(__file__).resolve().parents[1]
SERVICES = (
    "1688",
    "cainiao",
    "dingding",
    "qqmail",
    "qqmusic",
    "taobao",
    "tencentcloud",
    "tmall",
)
GOLDEN_END = STAGES.index("golden") + 1
RELEASE_END = STAGES.index("release") + 1
EXPECTED_CLIENTS = {"mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon"}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_immutable_binding(service_id: str) -> dict[str, Any]:
    registry = _read_yaml(ROOT / "sources" / "immutable_registry.yaml")
    binding = (registry.get("bindings") or {}).get(service_id)
    if not isinstance(binding, dict) or binding.get("status") != "active":
        raise RuntimeError(f"{service_id}: no active immutable Source binding")
    if binding.get("source_id") != "popular-rules-source":
        raise RuntimeError(f"{service_id}: unexpected immutable source id")
    for key in ("source_ref", "snapshot_id", "content_digest", "artifact_path", "release_path"):
        if not str(binding.get(key) or "").strip():
            raise RuntimeError(f"{service_id}: immutable binding missing {key}")
    return binding


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data if isinstance(data, dict) else {}


def _latest_snapshot(source_root: Path, service_id: str) -> tuple[Path, dict[str, Any]]:
    snapshots = []
    for path in (source_root / "snapshots").glob("*/manifest.json"):
        try:
            manifest = _read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if manifest.get("schema") == "source_snapshot_v2" and manifest.get("service_id") == service_id:
            snapshots.append((path.parent, manifest))
    if not snapshots:
        raise RuntimeError(f"{service_id}: no source_snapshot_v2 found")
    return max(snapshots, key=lambda item: str(item[1].get("created_at", "")))


def _verify_source(service_id: str, snapshot_dir: Path, manifest: dict[str, Any]) -> None:
    if manifest.get("release_state") != "CANDIDATE":
        raise RuntimeError(f"{service_id}: source release state is {manifest.get('release_state')}")
    if int(manifest.get("seed_only_count", 0) or 0) != 0:
        raise RuntimeError(f"{service_id}: seed_only_count != 0")
    if int(manifest.get("unverified_candidate_count", 0) or 0) != 0:
        raise RuntimeError(f"{service_id}: unverified_candidate_count != 0")
    evidence = [x for x in (manifest.get("evidence") or []) if isinstance(x, dict)]
    if not evidence:
        raise RuntimeError(f"{service_id}: no evidence")
    if any(x.get("source_method") != "official_web" for x in evidence):
        raise RuntimeError(f"{service_id}: non-official evidence present")
    domains = [str(x).strip() for x in (manifest.get("domains") or []) if str(x).strip()]
    if int(manifest.get("domain_count", 0) or 0) != len(domains) or not domains:
        raise RuntimeError(f"{service_id}: invalid domain count/output")
    if not (snapshot_dir / "domains.txt").is_file():
        raise RuntimeError(f"{service_id}: domains.txt missing")


def _domain_rules(service_id: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    evidence_ids = [
        str(item["evidence_id"])
        for item in (snapshot.get("evidence") or [])
        if isinstance(item, dict) and item.get("evidence_id")
    ]
    rules = [
        {
            "type": "domain",
            "value": domain,
            "sources": evidence_ids,
            "classification": {"category": "service"},
        }
        for domain in sorted(set(snapshot.get("domains") or []))
        if str(domain).strip()
    ]
    return {
        "id": service_id,
        "category": "service",
        "source": [
            {
                "repository": "cn-wanmei/Popular-Rules-Source",
                "snapshot_id": snapshot.get("snapshot_id"),
                "content_digest": snapshot.get("content_digest"),
            }
        ],
        "rules": rules,
    }


def _prepare_input(
    service_id: str,
    snapshot: dict[str, Any],
    source_commit: str,
    verified_input_commit: str,
    root: Path,
) -> Path:
    if root.exists():
        shutil.rmtree(root)
    services_dir = root / "services"
    services_dir.mkdir(parents=True, exist_ok=True)
    (services_dir / f"{service_id}.yaml").write_text(
        yaml.safe_dump(_domain_rules(service_id, snapshot), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    binding = {
        "schema": "phase2_source_binding_v2",
        "repository": "cn-wanmei/Popular-Rules-Source",
        "source_commit": source_commit,
        "verified_input_commit": verified_input_commit,
        "service_id": service_id,
        "snapshot_id": snapshot.get("snapshot_id"),
        "content_digest": snapshot.get("content_digest"),
        "evidence_digest": snapshot.get("evidence_digest"),
        "policy_digest": snapshot.get("policy_digest"),
        "generator_digest": snapshot.get("generator_digest"),
        "release_digest": snapshot.get("release_digest"),
        "release_identity_version": snapshot.get("release_identity_version"),
        "domain_count": snapshot.get("domain_count"),
        "official_evidence_count": len(snapshot.get("evidence") or []),
        "seed_only_count": snapshot.get("seed_only_count", 0),
    }
    (root / "source-binding.json").write_text(
        json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return root


def _assert_clients(run_dir: Path) -> dict[str, Any]:
    report = _read_json(run_dir / "golden" / "report.json")
    if report.get("all_pass") is not True:
        raise RuntimeError(f"golden failed: {report}")
    artifact_root = run_dir / "artifacts"
    actual = {p.name for p in artifact_root.iterdir() if p.is_dir()} if artifact_root.exists() else set()
    missing = sorted(EXPECTED_CLIENTS - actual)
    if missing:
        raise RuntimeError(f"missing clients: {missing}")
    return {
        "golden_all_pass": True,
        "seven_clients": sorted(EXPECTED_CLIENTS),
        "client_count": len(EXPECTED_CLIENTS),
    }


def _run_semantic_check(run_dir: Path) -> tuple[dict[str, Any], str]:
    ir_path = run_dir / "ir" / "ir.json"
    generated_root = run_dir / "artifacts"
    semantic_dir = run_dir / "semantic"
    semantic_dir.mkdir(parents=True, exist_ok=True)
    semantic_report = semantic_dir / "cross_client_report.json"

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "cross_client_semantic_test.py"),
            "--ir",
            str(ir_path),
            "--generated",
            str(generated_root),
            "--matrix",
            str(ROOT / "config" / "client_capability_matrix.yaml"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    stdout = completed.stdout.strip()
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "seven-client semantic check returned non-JSON output: "
            f"returncode={completed.returncode}; "
            f"stdout={stdout[-2000:]!r}; stderr={completed.stderr[-4000:]!r}"
        ) from exc

    semantic_report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if completed.returncode != 0 or report.get("pass") is not True:
        raise RuntimeError(
            f"seven-client semantic check failed: {json.dumps(report, ensure_ascii=False)}"
        )
    return report, str(run_dir.name)

def _run_pipeline(sources: Path, data_root: Path, run_id: str, end: int) -> dict[str, Any]:
    return run_pipeline(
        sources,
        data_root,
        run_id=run_id,
        stages=STAGES[:end],
        skip_large=False,
    )


def canary_service(
    service_id: str,
    source_root: Path,
    source_commit: str,
    verified_input_commit: str,
    base_dir: Path,
) -> dict[str, Any]:
    binding = _load_immutable_binding(service_id)
    if str(binding["source_ref"]) != source_commit:
        raise RuntimeError(
            f"{service_id}: immutable binding source_ref {binding['source_ref']} "
            f"!= checked-out Source commit {source_commit}"
        )
    snapshot_id = str(binding["snapshot_id"])
    snapshot_dir = source_root / "snapshots" / snapshot_id
    snapshot_manifest = snapshot_dir / "manifest.json"
    release_root = source_root / str(Path(binding["release_path"]).parent)
    release_file = source_root / str(binding["release_path"])
    if not snapshot_manifest.is_file():
        raise RuntimeError(f"{service_id}: immutable snapshot manifest missing: {snapshot_manifest}")
    if not release_file.is_file():
        raise RuntimeError(f"{service_id}: immutable Source release artifact missing: {release_file}")
    snapshot = _read_json(snapshot_manifest)
    _verify_source(service_id, snapshot_dir, snapshot)
    if snapshot.get("snapshot_id") != snapshot_id:
        raise RuntimeError(f"{service_id}: immutable snapshot binding mismatch")
    if snapshot.get("content_digest") != binding["content_digest"]:
        raise RuntimeError(f"{service_id}: immutable content digest mismatch")
    release_doc = _read_json(release_file)
    if release_doc.get("snapshot_id") != snapshot_id:
        raise RuntimeError(f"{service_id}: Source release snapshot binding mismatch")
    if release_doc.get("content_digest") != binding["content_digest"]:
        raise RuntimeError(f"{service_id}: Source release content digest mismatch")
    for field in ("evidence_digest", "policy_digest", "generator_digest", "release_digest", "release_identity_version"):
        if release_doc.get(field) != binding.get(field):
            raise RuntimeError(f"{service_id}: Source release {field} mismatch")
    checksums_file = snapshot_dir / "checksums.json"
    if not checksums_file.is_file():
        raise RuntimeError(f"{service_id}: immutable snapshot checksums missing")
    checksums = _read_json(checksums_file)
    expected_domains_sha = str(checksums.get("domains.txt") or "")
    domains_sha = hashlib.sha256((snapshot_dir / "domains.txt").read_bytes()).hexdigest()
    if expected_domains_sha != domains_sha:
        raise RuntimeError(f"{service_id}: immutable domains checksum mismatch")
    if not release_file.is_file():
        raise RuntimeError(f"{service_id}: Source release artifact missing: {release_file}")
    release_doc = _read_json(release_file)
    if release_doc.get("snapshot_id") != snapshot.get("snapshot_id"):
        raise RuntimeError(f"{service_id}: Source release snapshot binding mismatch")

    service_dir = base_dir / service_id
    input_root = service_dir / "input"
    data_root = service_dir / "data"
    generated_root = service_dir / "generated"
    for p in (service_dir,):
        p.mkdir(parents=True, exist_ok=True)
    _prepare_input(service_id, snapshot, source_commit, verified_input_commit, input_root)

    golden_run = f"canary-{service_id}-golden"
    golden = _run_pipeline(input_root, data_root, golden_run, GOLDEN_END)
    if golden.get("status") != "ok":
        raise RuntimeError(f"{service_id}: V3 golden pipeline failed: {golden.get('failure_stages')}")
    golden_report = _assert_clients(data_root / "runs" / golden_run)

    run_one = f"canary-{service_id}-release-1"
    run_two = f"canary-{service_id}-release-2"
    first = _run_pipeline(input_root, data_root, run_one, RELEASE_END)
    second = _run_pipeline(input_root, data_root, run_two, RELEASE_END)
    if first.get("status") != "ok" or second.get("status") != "ok":
        raise RuntimeError(
            f"{service_id}: release rehearsal failed: "
            f"first={first.get('failure_stages')}, second={second.get('failure_stages')}"
        )

    runs_root = data_root / "runs"
    semantic_report, semantic_run_id = _run_semantic_check(runs_root / run_two)
    reconciliation = reconcile_service(
        service_id=service_id,
        source_root=source_root,
        canary_root=service_dir,
        source_commit=source_commit,
        v3_run_id=run_two,
        snapshot_id=str(snapshot.get("snapshot_id") or ""),
    )
    reconciliation_dir = service_dir / "reconciliation"
    reconciliation_dir.mkdir(parents=True, exist_ok=True)
    (reconciliation_dir / "report.json").write_text(
        json.dumps(reconciliation, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    generated_root.mkdir(parents=True, exist_ok=True)
    baseline = data_root / "baseline" / "canonical.json"
    promote_one = promote_run(runs_root / run_one, generated_root, baseline_path=baseline)
    promote_two = promote_run(runs_root / run_two, generated_root, baseline_path=baseline)
    rollback = rollback_to_run(run_one, runs_root, generated_root)
    latest = _read_json(generated_root / "_promotion" / "latest.json")
    if latest.get("run_id") != run_one:
        raise RuntimeError(f"{service_id}: rollback did not restore first run")
    rollback_identity = {
        "service_id": service_id,
        "first_run": run_one,
        "second_run": run_two,
        "rollback_target": rollback.get("run_id"),
        "restored_run": latest.get("run_id"),
    }
    rollback_run_id = "rollback-" + service_id + "-" + hashlib.sha256(
        json.dumps(rollback_identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]

    observation = start_observation(
        service_id=service_id,
        source_commit=source_commit,
        snapshot_id=str(snapshot.get("snapshot_id") or ""),
        content_digest=str(snapshot.get("content_digest") or ""),
        v3_run_id=run_two,
        semantic_run_id=semantic_run_id,
        reconciliation_run_id=reconciliation["run_id"],
        rollback_run_id=rollback_run_id,
    )

    report = {
        "schema": "phase2_service_canary_v1",
        "service_id": service_id,
        "source": {
            "repository": "cn-wanmei/Popular-Rules-Source",
            "commit": source_commit,
            "snapshot_id": snapshot.get("snapshot_id"),
            "content_digest": snapshot.get("content_digest"),
            "evidence_digest": snapshot.get("evidence_digest"),
            "policy_digest": snapshot.get("policy_digest"),
            "generator_digest": snapshot.get("generator_digest"),
            "release_digest": snapshot.get("release_digest"),
            "release_identity_version": snapshot.get("release_identity_version"),
            "domain_count": snapshot.get("domain_count"),
            "seed_only_count": snapshot.get("seed_only_count", 0),
            "unverified_candidate_count": snapshot.get("unverified_candidate_count", 0),
            "release_state": snapshot.get("release_state"),
            "official_evidence_count": len(snapshot.get("evidence") or []),
            "release_artifact": str(release_file.relative_to(source_root)),
            "release_schema": release_doc.get("schema"),
        },
        "verified": True,
        "canary": {
            "v3_golden": golden_report,
            "golden_run_id": golden_run,
            "v3_release_run_id": run_two,
            "semantic": {
                "pass": semantic_report.get("pass") is True,
                "client_count": len(semantic_report.get("passed") or []),
                "passed_clients": semantic_report.get("passed") or [],
                "failure_count": len(semantic_report.get("failures") or []),
            },
            "semantic_run_id": semantic_run_id,
            "reconciliation_run_id": reconciliation["run_id"],
            "reconciliation": reconciliation,
            "observation_run_id": observation["run_id"],
            "observation_started_at": observation["started_at"],
            "observation": observation,
        },
        "rollback": {
            "first_run": run_one,
            "second_run": run_two,
            "first_promotion": promote_one.get("run_id"),
            "second_promotion": promote_two.get("run_id"),
            "rollback_run": rollback_run_id,
            "rollback_target_run": rollback.get("run_id"),
            "restored_run": latest.get("run_id"),
            "pass": latest.get("run_id") == run_one,
        },
        "production_ready": bool(
            semantic_report.get("pass") is True
            and reconciliation.get("status") == "PASS"
            and latest.get("run_id") == run_one
            and observation.get("status") == "ACTIVE"
        ),
    }
    out = service_dir / "report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--verified-input-commit", required=True)
    parser.add_argument("--services", nargs="*", default=list(SERVICES))
    parser.add_argument("--output", type=Path, default=Path("reports/phase2-canary"))
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    output = args.output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    results = {}
    failures = {}
    for service_id in args.services:
        try:
            results[service_id] = canary_service(
                service_id,
                source_root,
                args.source_commit,
                args.verified_input_commit,
                output,
            )
        except Exception as exc:
            failures[service_id] = f"{type(exc).__name__}: {exc}"
            continue

    summary = {
        "schema": "phase2_canary_summary_v1",
        "source_commit": args.source_commit,
        "services": results,
        "failures": failures,
        "verified_count": sum(1 for item in results.values() if item.get("verified")),
        "canary_pass_count": sum(
            1 for item in results.values()
            if item.get("canary", {}).get("v3_golden")
            and item.get("canary", {}).get("semantic", {}).get("pass") is True
            and item.get("canary", {}).get("reconciliation", {}).get("status") == "PASS"
            and item.get("rollback", {}).get("pass")
        ),
        "production_ready_count": sum(1 for item in results.values() if item.get("production_ready")),
        "all_pass": not failures and len(results) == len(args.services),
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
