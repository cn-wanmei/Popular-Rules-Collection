#!/usr/bin/env python3
"""Materialize the complete Network Dataset publication layer.

Service rules and Network Datasets have different semantics and remain in
separate namespaces.  This builder gives Network Datasets a deterministic,
first-class place in the same release candidate as the seven client rule
projections.

Inputs are already-collected repository files under database/.  The builder
never performs network I/O.  Collection is responsible for refreshing those
inputs; this stage is responsible for deterministic publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
NETWORK_SCOPES = {"asn", "geoip", "geosite", "network", "provider", "policies", "ip", "mmdb"}


def _load_dataset_docs() -> list[tuple[str, dict[str, Any]]]:
    root = ROOT / "sources" / "datasets"
    docs: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(root.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            raise RuntimeError(f"Invalid dataset registry: {path}")
        docs.append((path.name, data))
    return docs


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _clean_network_outputs(output: Path) -> None:
    for scope in sorted(NETWORK_SCOPES):
        target = output / scope
        if target.exists():
            shutil.rmtree(target)


def _text_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _write_text(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _write_network_variants(scope: str, name: str, lines: list[str], output: Path) -> None:
    target = output / scope
    _write_text(target / f"{name}.txt", lines)

    if not lines:
        return

    def cidr(line: str) -> bool:
        return "/" in line and not line.startswith("http://") and not line.startswith("https://")

    if scope == "geosite":
        _write_text(
            target / f"{name}_mihomo.list",
            [f"DOMAIN-SUFFIX,{line.lstrip('.')}" for line in lines],
        )
    elif scope in {"geoip", "network"}:
        mihomo: list[str] = []
        for line in lines:
            mihomo.append(
                f"IP-CIDR6,{line}" if ":" in line.split("/")[0] else
                f"IP-CIDR,{line}" if cidr(line) else
                f"DOMAIN-SUFFIX,{line.lstrip('.')}"
            )
        _write_text(target / f"{name}_mihomo.list", mihomo)
        if any(cidr(line) for line in lines):
            _write_text(
                target / f"{name}_surge.list",
                [f"IP-CIDR6,{line}" if ":" in line.split("/")[0] else f"IP-CIDR,{line}" for line in lines if cidr(line)],
            )
            _write_text(
                target / f"{name}_singbox_cidrs.txt",
                [line for line in lines if cidr(line)],
            )
    elif scope == "provider":
        _write_text(
            target / f"{name}_mihomo.list",
            [f"IP-CIDR6,{line}" if ":" in line.split("/")[0] else f"IP-CIDR,{line}" for line in lines if cidr(line)],
        )


def _destination_scope(kind: str, scope: str) -> str:
    if kind == "asn":
        return "asn"
    if kind == "binary" or scope == "artifact":
        return "mmdb"
    if kind == "policy" or scope == "policy":
        return "policies"
    return scope


def _materialize_database_entry(
    kind: str,
    dataset: dict[str, Any],
    output: Path,
    records: list[dict[str, Any]],
) -> None:
    enabled = bool(dataset.get("enabled"))
    if not enabled:
        return

    scope = str(dataset.get("scope") or kind)
    dest_scope = _destination_scope(kind, scope)
    source_path: Path | None = None

    artifact = dataset.get("artifact")
    path = dataset.get("path")
    if artifact:
        source_path = ROOT / str(artifact)
    elif path:
        source_path = ROOT / str(path)

    if source_path is None:
        raise RuntimeError(f"{dataset.get('id')}: no local materialization path")

    if not source_path.is_file():
        raise RuntimeError(
            f"{dataset.get('id')}: required collected input is missing: {source_path.relative_to(ROOT)}"
        )

    did = str(dataset.get("id") or source_path.stem)
    target_name = source_path.name
    target = output / dest_scope / target_name

    # Artifact inputs are binary or structured files and must be copied byte-for-byte.
    if kind == "binary" or artifact:
        target.parent.mkdir(parents=True, exist_ok=True)
        if source_path.resolve() != target.resolve():
            shutil.copy2(source_path, target)
        records.append({
            "id": did,
            "kind": kind,
            "scope": dest_scope,
            "source": str(source_path.relative_to(ROOT)),
            "file": str(target.relative_to(output)),
            "sha256": _sha256(target),
            "bytes": target.stat().st_size,
        })
        return

    if source_path.suffix.lower() in {".yaml", ".yml", ".json"}:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target)
        records.append({
            "id": did,
            "kind": kind,
            "scope": dest_scope,
            "source": str(source_path.relative_to(ROOT)),
            "file": str(target.relative_to(output)),
            "sha256": _sha256(target),
            "bytes": target.stat().st_size,
        })
        return

    lines = sorted(dict.fromkeys(_text_lines(source_path)))
    _write_network_variants(dest_scope, source_path.stem, lines, output)
    raw_target = output / dest_scope / f"{source_path.stem}.txt"
    records.append({
        "id": did,
        "kind": kind,
        "scope": dest_scope,
        "source": str(source_path.relative_to(ROOT)),
        "file": str(raw_target.relative_to(output)),
        "sha256": _sha256(raw_target),
        "bytes": raw_target.stat().st_size,
        "lines": len(lines),
    })


def _materialize_service_ips(output: Path, records: list[dict[str, Any]]) -> None:
    src = ROOT / "database" / "ips"
    if not src.is_dir():
        return
    for source_path in sorted(src.glob("*.txt")):
        lines = sorted(dict.fromkeys(_text_lines(source_path)))
        _write_network_variants("ip", source_path.stem, lines, output)
        target = output / "ip" / f"{source_path.stem}.txt"
        records.append({
            "id": source_path.stem,
            "kind": "service_ip",
            "scope": "ip",
            "source": str(source_path.relative_to(ROOT)),
            "file": str(target.relative_to(output)),
            "sha256": _sha256(target),
            "bytes": target.stat().st_size,
            "lines": len(lines),
        })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "generated")
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    parser.add_argument("--allow-missing-artifacts", action="store_true")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    _clean_network_outputs(output)

    records: list[dict[str, Any]] = []
    missing_optional: list[str] = []

    for _filename, doc in _load_dataset_docs():
        kind = str(doc.get("kind") or "other")
        for dataset in doc.get("datasets") or []:
            if not isinstance(dataset, dict) or not dataset.get("enabled"):
                continue
            try:
                _materialize_database_entry(kind, dataset, output, records)
            except RuntimeError as exc:
                artifact = bool(dataset.get("artifact")) or kind == "binary"
                if artifact and args.allow_missing_artifacts:
                    missing_optional.append(str(exc))
                    continue
                raise

    _materialize_service_ips(output, records)

    if not records:
        raise RuntimeError("Network publication produced no artifacts")

    generated_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "schema": "network_publication_v2",
        "generated_at": generated_at,
        "collection_date": args.date,
        "runtime_contract": "network_dataset_distribution_v2",
        "semantics": {
            "service_rules": "generated/<client>/...",
            "network_datasets": "generated/<scope>/...",
            "provider_cidrs_are_not_service_ownership": True,
            "geosite_is_not_service_identity": True,
            "geoip_is_not_service_ip_ownership": True,
            "asn_is_provider_metadata_only": True,
        },
        "file_count": len(records),
        "files": records,
        "missing_optional": sorted(missing_optional),
    }
    (output / "network_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "schema": manifest["schema"],
        "files": len(records),
        "missing_optional": len(missing_optional),
        "output": str(output),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
