"""Build the client-neutral human rule browse distribution from Semantic IR."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
IR_SCHEMA = "semantic_ir_v2"
OUTPUT_SCHEMA = "human_rule_distribution_v1"
MANIFEST_SCHEMA = "human_rule_distribution_manifest_v1"


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError(f"expected YAML object: {path}")
    return value


def _slug(value: str) -> str:
    text = str(value).strip().casefold()
    text = re.sub(r"[^a-z0-9._-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip(".-")
    if not text or text in {".", ".."}:
        raise ValueError(f"unsafe empty path component: {value!r}")
    return text


def _rows(rules_by_id: dict[str, dict[str, Any]], rule_ids: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule_id in sorted(rule_ids):
        rule = rules_by_id.get(rule_id)
        if not rule:
            continue
        rows.append({
            "id": rule["id"],
            "type": str(rule["type"]).strip().upper(),
            "value": str(rule["value"]),
        })
    return sorted(rows, key=lambda row: (row["type"], row["value"], row["id"]))


def _load_distribution_layout(policy_path: Path) -> dict[str, str]:
    policy = _load_yaml(Path(policy_path))
    if policy.get("schema") != "rule_distribution_policy_v2":
        raise RuntimeError("Unsupported rule distribution policy schema")
    layout = policy.get("layout") or {}
    required = (
        "human_aggregate",
        "human_service",
        "human_china",
        "human_category",
        "human_group",
        "human_aggregate_entity",
        "human_unmapped_service",
    )
    if not all(isinstance(layout.get(key), str) and layout.get(key).strip() for key in required):
        raise RuntimeError("Directory policy is missing human distribution path templates")
    return {key: str(layout[key]).strip() for key in required}


def _render_rule_path(output_dir: Path, template: str, **values: str) -> Path:
    rendered = template.format(**values)
    parts = Path(rendered).parts
    if not parts or parts[0] != "rule" or any(part in {"", ".", ".."} for part in parts):
        raise RuntimeError(f"invalid human rule distribution path template result: {rendered!r}")
    return output_dir.joinpath(*parts[1:])


def _write_entity(
    output: Path,
    *,
    entity: str,
    entity_id: str,
    display_name: str,
    provider: str | None,
    rows: list[dict[str, Any]],
    ir_digest: str,
    run_id: str,
    records: list[dict[str, Any]],
) -> None:
    if not rows:
        return
    by_type = Counter(row["type"] for row in rows)
    payload: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "version": 1,
        "entity": entity,
        "id": entity_id,
        "display_name": display_name,
        "generated_from": {
            "run_id": run_id,
            "ir_schema": IR_SCHEMA,
            "ir_digest": ir_digest,
        },
        "stats": {"total": len(rows), "by_type": dict(sorted(by_type.items()))},
        "rules": rows,
    }
    if provider:
        payload["provider"] = provider
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")
    records.append({
        "path": output.as_posix(),
        "entity": entity,
        "id": entity_id,
        "display_name": display_name,
        "provider": provider,
        "rule_count": len(rows),
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    })


def build_rule_tree(
    ir_dir: Path,
    output_dir: Path,
    *,
    hierarchy_path: Path,
    run_id: str,
    policy_path: Path | None = None,
) -> dict[str, Any]:
    ir_dir = Path(ir_dir)
    output_dir = Path(output_dir)
    ir = _load_json(ir_dir / "ir.json")
    if ir.get("schema") != IR_SCHEMA:
        raise RuntimeError(f"unsupported IR schema: {ir.get('schema')!r}")
    if ir.get("v2_runtime_dependency") != 0:
        raise RuntimeError("IR reports non-zero V2 runtime dependency")
    ir_manifest = _load_json(ir_dir / "manifest.json")
    ir_digest = str(ir_manifest.get("ir_digest") or "").strip()
    if not re.fullmatch(r"[0-9a-f]{64}", ir_digest):
        raise RuntimeError("IR manifest has no valid ir_digest")
    resolved_run_id = str(run_id).strip()
    if not resolved_run_id:
        raise RuntimeError("run_id is required for human rule distribution")

    policy_path = Path(policy_path) if policy_path is not None else ROOT / "config" / "service_model" / "directories.yaml"
    layout = _load_distribution_layout(policy_path)
    hierarchy = _load_yaml(Path(hierarchy_path))
    providers = hierarchy.get("providers") or {}
    categories = hierarchy.get("categories") or {}
    rules = {str(r["id"]): r for r in ir.get("rules") or [] if isinstance(r, dict) and r.get("id")}
    memberships = {
        str(entity): {str(rule_id) for rule_id in ids if str(rule_id).strip()}
        for entity, ids in (ir.get("memberships") or {}).items()
        if isinstance(ids, list)
    }
    records: list[dict[str, Any]] = []

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    provider_aggregate_ids: set[str] = set()
    service_ids: set[str] = set()
    for provider, meta in sorted(providers.items(), key=lambda item: str(item[0]).casefold()):
        if not isinstance(meta, dict):
            continue
        provider_id = str(provider).strip().casefold()
        aggregate_id = str(meta.get("aggregate") or provider_id).strip()
        provider_aggregate_ids.add(aggregate_id)
        service_block = meta.get("services") or {}
        for service_id, service_meta in sorted(service_block.items(), key=lambda item: str(item[0]).casefold()):
            service_id = str(service_id).strip()
            service_ids.add(service_id)
            service_meta = service_meta if isinstance(service_meta, dict) else {}
            rows = _rows(rules, memberships.get(service_id, set()))
            if rows:
                _write_entity(
                    _render_rule_path(output_dir, layout["human_service"], provider=_slug(provider_id), service=_slug(service_id)),
                    entity="service",
                    entity_id=service_id,
                    display_name=str(service_meta.get("display_name") or service_id),
                    provider=provider_id,
                    rows=rows,
                    ir_digest=ir_digest,
                    run_id=resolved_run_id,
                    records=records,
                )
        aggregate_ids = set(memberships.get(aggregate_id, set()))
        for service_id in service_block:
            aggregate_ids.update(memberships.get(str(service_id), set()))
        rows = _rows(rules, aggregate_ids)
        if rows:
            _write_entity(
                _render_rule_path(output_dir, layout["human_aggregate"], provider=_slug(provider_id)),
                entity="provider_aggregate",
                entity_id=aggregate_id,
                display_name=str(meta.get("display_name") or provider_id),
                provider=provider_id,
                rows=rows,
                ir_digest=ir_digest,
                run_id=resolved_run_id,
                records=records,
            )

    rows = _rows(rules, memberships.get("china", set()))
    if rows:
        _write_entity(
            _render_rule_path(output_dir, layout["human_china"], provider="china"),
            entity="domestic_aggregate",
            entity_id="china",
            display_name="China",
            provider=None,
            rows=rows,
            ir_digest=ir_digest,
            run_id=resolved_run_id,
            records=records,
        )

    category_rule_ids: dict[str, set[str]] = {}
    for rule in rules.values():
        category = str((rule.get("classification") or {}).get("category") or "").strip()
        if category:
            category_rule_ids.setdefault(category, set()).add(str(rule["id"]))
    for category, meta in sorted(categories.items(), key=lambda item: str(item[0]).casefold()):
        category_id = str(category).strip()
        category_ids = set(category_rule_ids.get(category_id, set()))
        category_meta = meta if isinstance(meta, dict) else {}
        if not category_ids:
            for service_id in category_meta.get("services") or {}:
                category_ids.update(memberships.get(str(service_id), set()))
        rows = _rows(rules, category_ids)
        if rows:
            _write_entity(
                _render_rule_path(output_dir, layout["human_category"], category=_slug(category_id)),
                entity="category",
                entity_id=category_id,
                display_name=str(category_meta.get("display_name") or category_id),
                provider=None,
                rows=rows,
                ir_digest=ir_digest,
                run_id=resolved_run_id,
                records=records,
            )

    entity_names = ir.get("entities") or {}
    group_ids = {str(x) for x in entity_names.get("groups") or []}
    aggregate_ids = {str(x) for x in entity_names.get("aggregates") or []}
    for entity_id, rule_ids in sorted(memberships.items(), key=lambda item: item[0].casefold()):
        if not rule_ids or entity_id in provider_aggregate_ids or entity_id in service_ids or entity_id == "china":
            continue
        rows = _rows(rules, rule_ids)
        if not rows:
            continue
        if entity_id in group_ids:
            entity = "group"
        elif entity_id in aggregate_ids:
            entity = "aggregate"
        else:
            entity = "unmapped_service"
        template_key = {
            "group": "human_group",
            "aggregate": "human_aggregate_entity",
            "unmapped_service": "human_unmapped_service",
        }[entity]
        _write_entity(
            _render_rule_path(
                output_dir,
                layout[template_key],
                group=_slug(entity_id),
                aggregate=_slug(entity_id),
                service=_slug(entity_id),
            ),
            entity=entity,
            entity_id=entity_id,
            display_name=entity_id,
            provider=None,
            rows=rows,
            ir_digest=ir_digest,
            run_id=resolved_run_id,
            records=records,
        )

    for item in records:
        item["path"] = Path(item["path"]).relative_to(output_dir).as_posix()
    records.sort(key=lambda item: item["path"])
    index = {
        "schema": "human_rule_distribution_index_v1",
        "status": "ready",
        "run_id": resolved_run_id,
        "ir_schema": IR_SCHEMA,
        "ir_digest": ir_digest,
        "entries": records,
    }
    (output_dir / "_index.yaml").write_text(yaml.safe_dump(index, allow_unicode=True, sort_keys=False), encoding="utf-8")
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "version": 1,
        "status": "ready" if records else "empty",
        "run_id": resolved_run_id,
        "ir_schema": IR_SCHEMA,
        "ir_digest": ir_digest,
        "rule_file_count": len(records),
        "rule_count": sum(item["rule_count"] for item in records),
        "entities": {
            "provider_aggregates": sum(1 for item in records if item["entity"] == "provider_aggregate"),
            "services": sum(1 for item in records if item["entity"] == "service"),
            "categories": sum(1 for item in records if item["entity"] == "category"),
            "other": sum(1 for item in records if item["entity"] not in {"provider_aggregate", "service", "category"}),
        },
        "files": [item["path"] for item in records],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    readme = [
        "# Rule Browse Distribution",
        "",
        "> Generated from the same Semantic IR Run as generated/. This tree is for human browsing, searching and selecting rules; it is never a V3 runtime input.",
        "",
        f"- Run ID: `{resolved_run_id}`",
        f"- IR digest: `{ir_digest}`",
        f"- Rule files: **{len(records)}**",
        "",
        "Do not hand-edit files under this tree. Rebuild the same immutable Run after changing upstream or Canonical inputs.",
    ]
    (output_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--hierarchy", type=Path, default=ROOT / "config" / "ruleset_hierarchy.yaml")
    parser.add_argument("--policy", type=Path, default=ROOT / "config" / "service_model" / "directories.yaml")
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    manifest = build_rule_tree(args.ir, args.output, hierarchy_path=args.hierarchy, run_id=args.run_id, policy_path=args.policy)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())