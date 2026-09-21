from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

SOURCE_REPORT_URL = (
    "https://raw.githubusercontent.com/cn-wanmei/"
    "Popular-Rules-Source/main/reports/durable-bridge/latest.json"
)
REGISTRY_PATH = Path("sources/immutable_registry.yaml")


def _get_report() -> dict:
    request = Request(SOURCE_REPORT_URL, headers={"User-Agent": "Popular-Rules-Collection/source-auto-handoff"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _replace_binding_block(text: str, service_id: str, values: dict[str, str]) -> str:
    pattern = re.compile(
        r"(?ms)^  (?:" + re.escape(service_id) + r"|\"" + re.escape(service_id) + r"\"):\n"
        r".*?(?=^  (?:\"?[A-Za-z0-9_-]+\"?):\n|\Z)"
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"immutable registry binding not found: {service_id}")
    block = match.group(0)
    for key, value in values.items():
        line = f"    {key}: {value}"
        block, count = re.subn(
            rf"(?m)^    {re.escape(key)}:.*$",
            line,
            block,
        )
        if count != 1:
            raise RuntimeError(f"binding key {service_id}.{key} missing or duplicated")
    return text[:match.start()] + block + text[match.end():]


def main() -> None:
    report = _get_report()
    if report.get("schema") not in {"popular_rules_source_durable_bridge_v1", "popular_rules_source_durable_bridge_v2"}:
        raise SystemExit(f"unsupported Source durable report schema: {report.get('schema')}")
    source_ref = str(report.get("persistence_commit") or "")
    verified_input = str(report.get("verified_input_commit") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", source_ref):
        raise SystemExit("Source durable report does not contain a valid persistence commit")
    if not re.fullmatch(r"[0-9a-f]{40}", verified_input):
        raise SystemExit("Source durable report does not contain a valid verified input commit")

    current_text = REGISTRY_PATH.read_text(encoding="utf-8")
    current = yaml.safe_load(current_text) or {}
    bindings = current.get("bindings") or {}
    changed: list[str] = []

    for service_id, item in sorted((report.get("services") or {}).items()):
        if item.get("status") != "PERSISTED":
            continue
        binding = bindings.get(service_id) or {}
        if (
            binding.get("status") == "active"
            and binding.get("snapshot_id") == item.get("snapshot_id")
            and binding.get("content_digest") == item.get("content_digest")
        ):
            continue
        values = {
            "status": "active",
            "source_id": "popular-rules-source",
            "source_ref": source_ref,
            "verified_input_commit": verified_input,
            "artifact_path": str(item["artifact_path"]),
            "release_path": str(item["release_path"]),
            "snapshot_id": str(item["snapshot_id"]),
            "content_digest": str(item["content_digest"]),
            "expected_sha256": str(item["expected_sha256"]),
        }
        current_text = _replace_binding_block(current_text, service_id, values)
        changed.append(service_id)

    if changed:
        REGISTRY_PATH.write_text(current_text, encoding="utf-8")

    print(json.dumps({
        "schema": "source_auto_handoff_v1",
        "source_ref": source_ref,
        "verified_input_commit": verified_input,
        "changed_services": changed,
        "changed": bool(changed),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
