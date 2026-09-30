#!/usr/bin/env python3
"""Resolve service_id → V6 CDN URL using the configured immutable manifest."""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def load_provider(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text)
    out: dict = {"provider": "v6", "v6": {}}
    section = None
    for line in text.splitlines():
        if line.startswith("provider:"):
            out["provider"] = line.split(":", 1)[1].strip()
        elif line.strip() == "v6:":
            section = "v6"
        elif section == "v6" and line.startswith("  ") and ":" in line and not line.strip().startswith("#"):
            k, _, v = line.strip().partition(":")
            out["v6"][k.strip()] = v.strip().strip('"')
        elif line.startswith("rollback:") or (
            line and not line.startswith(" ") and line.endswith(":") and line.strip() != "v6:"
        ):
            section = None
    return out


def fetch_manifest(cfg: dict) -> dict:
    v6 = cfg.get("v6") or {}
    path = v6.get("manifest_path")
    if not path:
        raise ValueError("V6 manifest_path is missing")
    mirrors = v6.get("mirrors") or {}
    base = mirrors.get("jsdelivr") or mirrors.get("raw")
    if not base:
        base = "https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist/{path}"
    url = base.format(path=path)
    req = urllib.request.Request(url, headers={"User-Agent": "Popular-Rules-Collection-IconResolver/1.1"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def resolve(manifest: dict, service_id: str, *, size: int = 256, style: str = "source_original") -> str | None:
    key = f"{style}:{size}:png"
    for entry in manifest.get("entries") or []:
        if entry.get("service_id") != service_id:
            continue
        variants = entry.get("variants") or {}
        meta = variants.get(key)
        if not meta:
            return None
        variant_hash = meta.get("variant_hash") if isinstance(meta, dict) else meta
        if not variant_hash:
            return None
        manifest_path = meta.get("path") if isinstance(meta, dict) else None
        if manifest_path:
            if not manifest_path.startswith("/v/") or not manifest_path.endswith(".png"):
                raise ValueError(f"invalid manifest path for {service_id}: {manifest_path}")
            return f"https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist{manifest_path}"
        return f"https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist/v/{variant_hash}.png"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=Path("config/icon_v6.yaml"))
    ap.add_argument("--service", required=True)
    ap.add_argument("--size", type=int, default=256)
    ap.add_argument("--style", default="source_original")
    ap.add_argument("--manifest-file", type=Path, default=None, help="offline manifest JSON")
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
        if configured_release and manifest.get("release_id") != configured_release:
            print(
                f"manifest release mismatch: expected={configured_release} actual={manifest.get('release_id')}",
                file=sys.stderr,
            )
            return 4
        url = resolve(manifest, args.service, size=args.size, style=args.style)
        if url:
            print(url)
            return 0
    except Exception as exc:
        print(f"V6_ERROR {args.service}: {exc}", file=sys.stderr)
        return 1

    print(f"NOT_FOUND {args.service}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
