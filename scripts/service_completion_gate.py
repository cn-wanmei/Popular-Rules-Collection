from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def y(path: str) -> dict:
    data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def main() -> int:
    failures: list[str] = []
    targets = y("config/company_targets.yaml").get("companies") or []
    matrix = y("config/service_completion_matrix.yaml")
    registry = y("config/service_registry.yaml")
    membership = y("config/service_membership.yaml")
    policy = y("config/service_domain_policy.yaml")

    if len(targets) != 200:
        failures.append(f"company target count != 200: {len(targets)}")
    ids = [str(x.get("company_id")) for x in targets]
    if len(set(ids)) != len(ids):
        failures.append("duplicate company_id")
    records = matrix.get("company_records") or []
    if len(records) != 200:
        failures.append(f"completion matrix company records != 200: {len(records)}")

    p0c = (
        "gmail", "google-calendar", "google-chat", "google-contacts", "google-docs",
        "googledrive", "google-forms", "google-groups", "google-meet", "google-sheets",
        "google-sites", "google-slides", "google-vids", "google-workspace-studio",
        "google-maps", "google-photos", "google-play", "google-news", "google-voice",
        "google-earth", "ms365-word", "ms365-excel", "ms365-powerpoint", "ms365-onenote",
        "ms365-planner", "ms365-loop", "ms365-mesh", "applepodcasts", "applebooks", "applemaps",
    )
    reg = registry.get("platforms") or {}
    for group, expected in {
        "google": p0c[:20],
        "microsoft": p0c[20:27],
        "apple": p0c[27:],
    }.items():
        actual = set((reg.get(group) or {}).get("concrete_p0c_services") or [])
        missing = [sid for sid in expected if sid not in actual]
        if missing:
            failures.append(f"{group} registry missing: {missing}")

    verified_domains = policy.get("verified_p0c") or {}
    for sid in p0c:
        if sid not in verified_domains:
            failures.append(f"missing P0-C domain policy: {sid}")

    lineage = ["qqmail", "qqmusic", "taobao", "tencentcloud", "tmall"]
    if membership.get("principle") != "canonical_service_once_multiple_views":
        failures.append("membership model is not canonical-service-once")

    report = {
        "schema": "collection_service_completion_gate_v1",
        "pass": not failures,
        "company_count": len(targets),
        "completion_matrix_count": len(records),
        "p0c_verified_policy_count": len(verified_domains),
        "lineage_lock": lineage,
        "failures": failures,
    }
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)
    (out / "service-completion-gate.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
