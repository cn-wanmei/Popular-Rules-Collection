#!/usr/bin/env python3
"""generate_ecosystem_release_status.py — cross-repo read model (not SSOT)."""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

UA = {"User-Agent": "popular-rules-ecosystem-status/1.5"}


def fetch_bytes(url: str, timeout: int = 60, token: str | None = None) -> tuple[bytes | None, str | None]:
    try:
        headers = dict(UA)
        headers.update({
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        is_contents_api = "api.github.com/repos/" in url and "/contents/" in url
        if is_contents_api:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}v={time.time_ns()}"
            headers["Accept"] = "application/vnd.github.raw+json"
        else:
            headers["Accept"] = "application/vnd.github+json"
        auth_token = token if token is not None else (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "")
        auth_token = auth_token.strip()
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()

        # Normally the raw media type returns file bytes. Some frontends/proxies
        # still return the Contents API JSON envelope; decode only an explicitly
        # Base64-encoded envelope so ordinary JSON files remain intact.
        if is_contents_api and raw.lstrip().startswith(b"{"):
            try:
                envelope = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                envelope = None
            if (
                isinstance(envelope, dict)
                and envelope.get("encoding") == "base64"
                and isinstance(envelope.get("content"), str)
            ):
                raw = base64.b64decode(envelope["content"])
        return raw, None
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


def fetch_text(url: str, timeout: int = 60, token: str | None = None) -> tuple[str | None, str | None]:
    raw, err = fetch_bytes(url, timeout=timeout, token=token)
    if err:
        return None, err
    return (raw or b"").decode("utf-8", errors="replace"), None


def fetch_json(url: str, token: str | None = None) -> tuple[dict | list | None, str | None]:
    text, err = fetch_text(url, token=token)
    if err:
        return None, err
    try:
        return json.loads(text or ""), None
    except json.JSONDecodeError as exc:
        return None, f"JSONDecodeError: {exc}"


def age_seconds(iso: str | None, now: datetime) -> int | None:
    if not iso:
        return None
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return max(0, int((now - t).total_seconds()))
    except Exception:
        return None


def freshness_label(age: int | None, soft: int, hard: int) -> str:
    if age is None:
        return "unknown"
    if age <= soft:
        return "fresh"
    if age <= hard:
        return "aging"
    return "stale"


def identity_freshness(
    readable: bool,
    semantic_consistency: str,
    live_file_sha256: str | None,
    pinned_file_sha256: str | None,
    verification_report: dict | None,
    verified_at: str | None,
    now: datetime,
    hard_sla_seconds: int = 604800,
) -> tuple[str, str, int | None]:
    """Use a recent successful Identity Freshness comparison as the verification clock.

    The Icon snapshot is intentionally immutable when identity content is unchanged;
    generated_at is not a verification heartbeat. The latest workflow artifact is.
    """
    if not readable:
        return "unknown", "snapshot_unreadable", None
    if semantic_consistency == "error":
        return "stale", "identity_semantic_error", None
    if semantic_consistency == "warning":
        return "unknown", "identity_semantic_warning", None
    if not live_file_sha256 or not pinned_file_sha256:
        return "unknown", "identity_content_hash_missing", None
    if live_file_sha256 != pinned_file_sha256:
        return "stale", "identity_content_hash_mismatch", None
    if not isinstance(verification_report, dict):
        return "unknown", "identity_verification_report_unavailable", None
    verification_age = age_seconds(verified_at, now)
    if verification_age is None:
        return "unknown", "identity_verification_timestamp_missing", None
    if verification_age > hard_sla_seconds:
        return "stale", "identity_verification_expired", verification_age
    if verification_report.get("drift") is not False:
        return "stale", "identity_freshness_drift_detected", verification_age
    if verification_report.get("content_match") is not True:
        return "unknown", "identity_verification_not_content_match", verification_age
    if verification_report.get("live_file_sha256") != live_file_sha256:
        return "stale", "identity_verification_targets_different_collection_index", verification_age
    if verification_report.get("pinned_file_sha256") != pinned_file_sha256:
        return "stale", "identity_verification_targets_different_icon_pin", verification_age
    if verification_report.get("only_in_collection") or verification_report.get("only_in_snapshot"):
        return "stale", "identity_service_set_mismatch", verification_age
    if verification_report.get("field_mismatches"):
        return "stale", "identity_service_field_mismatch", verification_age
    return "fresh", "recent_identity_freshness_workflow_pass", verification_age


def fetch_latest_identity_verification() -> tuple[dict | None, str | None, int | None, str | None]:
    """Read the latest successful Icon Identity Freshness run and its JSON artifact."""
    base = "https://api.github.com/repos/cn-wanmei/Popular-Rules-Icon"
    icon_token = (os.environ.get("ICON_DISPATCH_TOKEN") or "").strip()
    if not icon_token:
        return None, None, None, "ICON_DISPATCH_TOKEN_unavailable"
    runs, err = fetch_json(
        f"{base}/actions/workflows/identity-freshness.yml/runs?branch=main&status=completed&per_page=1",
        token=icon_token,
    )
    if err or not isinstance(runs, dict):
        return None, None, None, err or "invalid_workflow_runs_response"
    items = runs.get("workflow_runs") or []
    if not items:
        return None, None, None, "no_identity_freshness_runs"
    run = items[0]
    run_id = run.get("id")
    created_at = run.get("created_at")
    if run.get("status") != "completed" or run.get("conclusion") != "success" or not run_id:
        return None, created_at, run_id, "latest_identity_freshness_run_not_successful"
    artifacts, err = fetch_json(
        f"{base}/actions/runs/{run_id}/artifacts?per_page=100", token=icon_token
    )
    if err or not isinstance(artifacts, dict):
        return None, created_at, run_id, err or "invalid_artifacts_response"
    artifact = next((item for item in artifacts.get("artifacts", [])
                     if item.get("name") == "identity-freshness-report"
                     and not item.get("expired")
                     and item.get("archive_download_url")), None)
    if not artifact:
        return None, created_at, run_id, "identity_freshness_artifact_missing"
    archive, err = fetch_bytes(artifact["archive_download_url"], token=icon_token)
    if err or not archive:
        return None, created_at, run_id, err or "identity_freshness_artifact_empty"
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            names = [name for name in bundle.namelist() if name.endswith("identity_freshness.json")]
            if len(names) != 1:
                return None, created_at, run_id, "identity_freshness_artifact_invalid"
            report = json.loads(bundle.read(names[0]).decode("utf-8"))
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        return None, created_at, run_id, f"identity_freshness_artifact_decode_error: {type(exc).__name__}"
    return report if isinstance(report, dict) else None, created_at, run_id, None

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("reports/ecosystem_release_status.json"))
    ap.add_argument(
        "--md-out",
        type=Path,
        default=Path("reports/ecosystem_release_status.md"),
        help="Human status page with explicit STALE OBSERVATION markers",
    )
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    now_s = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    sources = {
        "collection_publish_status": "https://api.github.com/repos/cn-wanmei/Popular-Rules-Collection/contents/PUBLISH_STATUS.md?ref=main",
        "collection_main_sha": "https://api.github.com/repos/cn-wanmei/Popular-Rules-Collection/commits/main",
        "collection_index": "https://api.github.com/repos/cn-wanmei/Popular-Rules-Collection/contents/rule/_index.yaml?ref=main",
        "source_durable_bridge": "https://api.github.com/repos/cn-wanmei/Popular-Rules-Source/contents/reports/durable-bridge/latest.json?ref=main",
        "icon_identity_snapshot": "https://api.github.com/repos/cn-wanmei/Popular-Rules-Icon/contents/config/collection_identity_snapshot.json?ref=main",
        "icon_release_pointers": "https://api.github.com/repos/cn-wanmei/Popular-Rules-Icon/contents/config/release-pointers.yaml?ref=main",
    }

    report: dict = {
        "schema": "ecosystem_release_status_v5",
        "generated_at": now_s,
        "observed_at": now_s,
        "authority_note": (
            "READ MODEL ONLY. Does not replace Collection/Source/Icon SSOT. "
            "See docs/STATE_MODEL.md."
        ),
        "repos": {
            "collection": "cn-wanmei/Popular-Rules-Collection",
            "source": "cn-wanmei/Popular-Rules-Source",
            "icon": "cn-wanmei/Popular-Rules-Icon",
        },
        "signals": {},
        "summary": {},
    }

    text, err = fetch_text(sources["collection_publish_status"])
    report["signals"]["collection_publish_status"] = {
        "url": sources["collection_publish_status"],
        "readability": "ok" if err is None else "error",
        "ok": err is None,
        "error": err,
        "bytes": len(text or ""),
    }

    data, err = fetch_json(sources["collection_main_sha"])
    collection_sha = data.get("sha") if isinstance(data, dict) else None
    report["signals"]["collection_main"] = {
        "url": sources["collection_main_sha"],
        "readability": "ok" if err is None and bool(collection_sha) else "error",
        "ok": err is None and bool(collection_sha),
        "error": err,
        "sha": collection_sha,
    }

    index_raw, index_err = fetch_bytes(sources["collection_index"])
    live_file_sha256 = hashlib.sha256(index_raw).hexdigest() if index_raw else None
    report["signals"]["collection_index"] = {
        "url": sources["collection_index"],
        "readability": "ok" if index_err is None and index_raw else "error",
        "ok": index_err is None and bool(index_raw),
        "error": index_err,
        "file_sha256": live_file_sha256,
        "bytes": len(index_raw or b""),
    }

    data, err = fetch_json(sources["source_durable_bridge"])
    persisted = 0
    incomplete: list = []
    batch_status = "unknown"
    run_comp = seal_comp = None
    created_at = None
    if isinstance(data, dict):
        services = data.get("services") or {}
        if isinstance(services, dict):
            persisted = sum(1 for v in services.values() if isinstance(v, dict) and v.get("status") == "PERSISTED")
        incomplete = list(data.get("incomplete") or [])
        created_at = data.get("created_at")
        run_comp = data.get("run_completeness")
        seal_comp = data.get("seal_completeness") or data.get("batch_completeness")
        if seal_comp not in ("COMPLETE", "PARTIAL", "FAILED"):
            if persisted <= 0:
                seal_comp = "FAILED"
            elif incomplete:
                seal_comp = "PARTIAL"
            else:
                seal_comp = "COMPLETE"
        batch_status = str(seal_comp)

    durable_age = age_seconds(created_at, now) if isinstance(created_at, str) else None
    report["signals"]["source_durable_bridge"] = {
        "url": sources["source_durable_bridge"],
        "readability": "ok" if err is None and isinstance(data, dict) else "error",
        "ok": err is None and isinstance(data, dict),
        "error": err,
        "persisted_count": persisted,
        "incomplete_count": len(incomplete) if isinstance(incomplete, list) else None,
        "run_completeness": run_comp,
        "seal_completeness": seal_comp,
        "batch_completeness": batch_status,
        "semantic_consistency": (
            "ok" if seal_comp == "COMPLETE" else ("warning" if seal_comp == "PARTIAL" else "error")
        ),
        "created_at": created_at,
        "age_seconds": durable_age,
        "freshness": freshness_label(durable_age, 86400, 604800),
        "persistence_commit": data.get("persistence_commit") if isinstance(data, dict) else None,
    }

    data, err = fetch_json(sources["icon_identity_snapshot"])
    svc_count = gen_at = src_ref = file_sha256 = None
    if isinstance(data, dict):
        svc_count = data.get("service_count")
        gen_at = data.get("generated_at")
        src = data.get("source")
        if isinstance(src, dict):
            src_ref = src.get("ref")
            file_sha256 = src.get("file_sha256") or src.get("file_sha")

    icon_sem = "ok"
    reasons = []
    if not file_sha256:
        icon_sem = "warning"
        reasons.append("file_sha256_missing")
    if live_file_sha256 and file_sha256 and file_sha256 != live_file_sha256:
        icon_sem = "error"
        reasons.append("file_sha256_mismatch")
    head_lag = bool(collection_sha and src_ref and src_ref not in (collection_sha, "main"))
    if head_lag and icon_sem == "ok":
        reasons.append("collection_head_ahead_content_ok")

    icon_age = age_seconds(gen_at if isinstance(gen_at, str) else None, now)
    icon_age_freshness = freshness_label(icon_age, 86400, 604800)
    identity_report, identity_verified_at, identity_run_id, identity_fetch_error = (
        fetch_latest_identity_verification()
    )
    icon_freshness, icon_freshness_reason, identity_verification_age = identity_freshness(
        err is None and isinstance(data, dict),
        icon_sem,
        live_file_sha256,
        file_sha256,
        identity_report,
        identity_verified_at,
        now,
    )
    report["signals"]["icon_identity_snapshot"] = {
        "url": sources["icon_identity_snapshot"],
        "readability": "ok" if err is None and isinstance(data, dict) else "error",
        "ok": err is None and isinstance(data, dict),
        "error": err,
        "service_count": svc_count,
        "generated_at": gen_at,
        "source_ref": src_ref,
        "file_sha256": file_sha256,
        "collection_main_sha": collection_sha,
        "collection_index_file_sha256": live_file_sha256,
        "semantic_consistency": icon_sem,
        "semantic_reasons": reasons,
        "age_seconds": icon_age,
        "age_freshness": icon_age_freshness,
        "verification_run_id": identity_run_id,
        "verification_created_at": identity_verified_at,
        "verification_age_seconds": identity_verification_age,
        "verification_error": identity_fetch_error,
        "freshness": icon_freshness,
        "freshness_basis": "latest_successful_identity_freshness_run",
        "freshness_reason": icon_freshness_reason,
    }

    text, err = fetch_text(sources["icon_release_pointers"])
    freeze_age = None
    freeze_label = "unknown"
    frozen = False
    if text and err is None:
        for line in text.splitlines():
            if line.strip().startswith("frozen:"):
                frozen = "true" in line.lower()
            if line.strip().startswith("updated_at:"):
                ts = line.split(":", 1)[1].strip().strip('"').strip("'")
                freeze_age = age_seconds(ts, now)
                freeze_label = freshness_label(freeze_age, 86400 * 14, 86400 * 45)
    report["signals"]["icon_release_pointers"] = {
        "url": sources["icon_release_pointers"],
        "readability": "ok" if err is None else "error",
        "ok": err is None,
        "error": err,
        "bytes": len(text or ""),
        "frozen": frozen,
        "freeze_age_seconds": freeze_age,
        "freeze_freshness": freeze_label,
    }

    if run_comp == "COMPLETE" and seal_comp == "COMPLETE":
        handoff_state = "COMPLETE"
    elif run_comp in ("PARTIAL", "FAILED") or seal_comp in ("PARTIAL", "FAILED"):
        handoff_state = "FAILED" if run_comp == "FAILED" and seal_comp == "FAILED" else "MANUAL_ACTION_REQUIRED"
    else:
        handoff_state = "UNKNOWN"

    signal_freshness = [
        report["signals"]["source_durable_bridge"].get("freshness"),
        report["signals"]["icon_identity_snapshot"].get("freshness"),
    ]
    if "stale" in signal_freshness:
        observation_status = "STALE OBSERVATION"
    elif "aging" in signal_freshness or "unknown" in signal_freshness:
        observation_status = "AGING OBSERVATION"
    else:
        observation_status = "FRESH OBSERVATION"

    readability_ok = all(
        report["signals"][k].get("readability") == "ok"
        for k in ("collection_main", "collection_index", "source_durable_bridge", "icon_identity_snapshot")
    )
    sem_vals = [
        report["signals"]["source_durable_bridge"].get("semantic_consistency"),
        report["signals"]["icon_identity_snapshot"].get("semantic_consistency"),
    ]
    if any(v == "error" for v in sem_vals):
        overall_sem = "error"
    elif any(v == "warning" for v in sem_vals):
        overall_sem = "warning"
    else:
        overall_sem = "ok"

    report["summary"] = {
        "collection_head": collection_sha,
        "collection_index_file_sha256": live_file_sha256,
        "source_durable_persisted": persisted,
        "source_seal_completeness": seal_comp,
        "source_run_completeness": run_comp,
        "handoff_state": handoff_state,
        "icon_snapshot_services": svc_count,
        "icon_snapshot_ref": src_ref,
        "icon_snapshot_file_sha256": file_sha256,
        "icon_vs_collection": icon_sem,
        "icon_production_frozen": frozen,
        "icon_freeze_freshness": freeze_label,
        "all_core_signals_ok": readability_ok,
        "readability": "ok" if readability_ok else "error",
        "semantic_consistency": overall_sem,
        "observation_status": observation_status,
        "observation_watermark": now_s,
        "freshness_sla_note": "source soft=24h hard=7d; icon identity uses latest successful Identity Freshness verification (snapshot age informational); freeze soft=14d hard=45d (read-model labels only)",
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = []
    md.append("# Ecosystem Release Status (Read Model)\n")
    md.append(f"> **{observation_status}** — observed_at `{now_s}`  \n")
    md.append("> Not SSOT. See `docs/STATE_MODEL.md`.\n")
    md.append("\n## Summary\n")
    md.append(f"| Field | Value |")
    md.append(f"|-------|-------|")
    md.append(f"| observation_status | **{observation_status}** |")
    md.append(f"| handoff_state | `{handoff_state}` |")
    md.append(f"| collection_head | `{collection_sha}` |")
    md.append(f"| source run / seal | `{run_comp}` / `{seal_comp}` |")
    md.append(f"| icon semantic | `{icon_sem}` |")
    md.append(f"| icon freeze | frozen={frozen} freshness=`{freeze_label}` |")
    md.append(f"| readability | `{report['summary']['readability']}` |")
    md.append(f"| semantic_consistency | `{overall_sem}` |")
    md.append("\n## Signal freshness\n")
    md.append("| Signal | freshness | age_seconds |")
    md.append("|--------|-----------|-------------|")
    for key in ("source_durable_bridge", "icon_identity_snapshot"):
        sig = report["signals"][key]
        md.append(f"| {key} | {sig.get('freshness')} | {sig.get('age_seconds')} |")
    if observation_status == "STALE OBSERVATION":
        md.append("\n> ⚠️ **STALE OBSERVATION**: one or more underlying signals exceed hard SLA. "
                  "Re-run Durable Bridge / Identity Freshness / Publish as appropriate.\n")
    args.md_out.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"wrote {args.out}")
    print(f"wrote {args.md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
