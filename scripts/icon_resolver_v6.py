#!/usr/bin/env python3
"""Resolve service_id → V6 CDN URL using the configured immutable manifest.

V6 is fail-closed: a missing/broken V6 asset is an error and never falls back
to a local Collection V5 asset.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load_provider(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml:
        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            raise ValueError("invalid icon provider config")
        return data

    out: dict = {"provider": None, "v6": {}, "rollback": {}}
    section = None
    for line in text.splitlines():
        if line.startswith("provider:"):
            out["provider"] = line.split(":", 1)[1].strip()
            section = None
        elif line.strip() == "v6:":
            section = "v6"
        elif line.strip() == "rollback:":
            section = "rollback"
        elif section and line.startswith("  ") and ":" in line:
            k, _, v = line.strip().partition(":")
            out[section][k.strip()] = v.strip().strip('"')
    return out


def fetch_manifest(cfg: dict) -> dict:
    v6 = cfg.get("v6") or {}
    manifest_path = v6.get("manifest_path")
    if not manifest_path:
        raise ValueError("V6 manifest_path is missing")
    mirrors = v6.get("mirrors") or {}
    base = mirrors.get("jsdelivr") or mirrors.get("raw")
    if not base:
        base = "https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist/{path}"
    url = base.format(path=manifest_path)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Popular-Rules-Collection-IconResolver/2.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def resolve(
    manifest: dict,
    service_id: str,
    *,
    size: int = 256,
    style: str = "source_original",
) -> str | None:
    key = f"{style}:{size}:png"
    for entry in manifest.get("entries") or []:
        if entry.get("service_id") != service_id:
            continue
        meta = (entry.get("variants") or {}).get(key)
        if not isinstance(meta, dict):
            return None
        path = meta.get("path")
        variant_hash = meta.get("variant_hash")
        if not isinstance(path, str) or not path.startswith("/v/") or not path.endswith(".png"):
            raise ValueError(f"invalid manifest path for {service_id}: {path!r}")
        if not isinstance(variant_hash, str) or len(variant_hash) != 64:
            raise ValueError(f"invalid variant hash for {service_id}: {variant_hash!r}")
        return f"https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist{path}"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=Path("config/icon_v6.yaml"))
    ap.add_argument("--service", required=True)
    ap.add_argument("--size", type=int, default=256)
    ap.add_argument("--style", default="source_original")
    ap.add_argument("--manifest-file", type=Path, default=None)
    args = ap.parse_args()

    try:
        cfg = load_provider(args.config)
        if cfg.get("provider") != "v6":
            print(f"provider is {cfg.get('provider')}, not v6", file=sys.stderr)
            return 2
        if args.manifest_file:
            manifest = json.loads(args.manifest_file.read_text(encoding="utf-8"))
        else:
            manifest = fetch_manifest(cfg)

        configured_release = (cfg.get("v6") or {}).get("release_id")
        actual_release = manifest.get("release_id")
        if configured_release and actual_release != configured_release:
            print(
                f"manifest release mismatch: expected={configured_release} actual={actual_release}",
                file=sys.stderr,
            )
            return 4

        url = resolve(manifest, args.service, size=args.size, style=args.style)
        if url:
            print(url)
            return 0

        print(f"NOT_FOUND {args.service}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"V6_ERROR {args.service}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
