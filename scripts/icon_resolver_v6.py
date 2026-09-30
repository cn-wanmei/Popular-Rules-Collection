#!/usr/bin/env python3
"""Resolve service_id → V6 CDN URL using Icon dist physical manifest + icon_v6.yaml."""
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
    # minimal parse
    out: dict = {"provider": "v5", "v6": {}}
    section = None
    for line in text.splitlines():
        if line.startswith("provider:"):
            out["provider"] = line.split(":", 1)[1].strip()
        if line.strip() == "v6:":
            section = "v6"
            continue
        if section == "v6" and line.startswith("  ") and ":" in line and not line.strip().startswith("#"):
            k, _, v = line.strip().partition(":")
            out["v6"][k.strip()] = v.strip().strip('"')
        if line.startswith("rollback:") or (line and not line.startswith(" ") and line.endswith(":") and line.strip() != "v6:"):
            if not line.startswith("v6"):
                section = None
    return out


def fetch_manifest(cfg: dict) -> dict:
    v6 = cfg.get("v6") or {}
    path = v6.get("manifest_path") or "manifests/icon-2026.09.30.freeze1.json"
    mirrors = v6.get("mirrors") or {}
    if isinstance(mirrors, dict):
        base = mirrors.get("jsdelivr") or mirrors.get("raw")
    else:
        base = None
    if not base:
        base = "https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist/{path}"
    url = base.format(path=path)
    req = urllib.request.Request(url, headers={"User-Agent": "Popular-Rules-Collection-IconResolver/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def resolve(manifest: dict, service_id: str, *, size: int = 256, style: str = "source_original") -> str | None:
    key = f"{style}:{size}:png"
    for e in manifest.get("entries") or []:
        if e.get("service_id") != service_id:
            continue
        variants = e.get("variants") or {}
        meta = variants.get(key)
        vh = meta.get("variant_hash") if isinstance(meta, dict) else meta
        if not vh:
            # try any png
            for k, v in variants.items():
                if k.endswith(":png"):
                    vh = v.get("variant_hash") if isinstance(v, dict) else v
                    break
        if vh:
            return f"https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist/v/{vh}.png"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=Path("config/icon_v6.yaml"))
    ap.add_argument("--service", required=True)
    ap.add_argument("--size", type=int, default=256)
    ap.add_argument("--manifest-file", type=Path, default=None, help="offline manifest JSON")
    args = ap.parse_args()
    cfg = load_provider(args.config)
    if cfg.get("provider") != "v6":
        print(f"provider is {cfg.get('provider')}, not v6", file=sys.stderr)
        return 2
    if args.manifest_file:
        manifest = json.loads(args.manifest_file.read_text())
    else:
        manifest = fetch_manifest(cfg)
    url = resolve(manifest, args.service, size=args.size)
    if not url:
        if (cfg.get("v6") or {}).get("fallback_to_v5") in (True, "true", "true"):
            print(f"V6_MISS fallback_v5 service={args.service}", file=sys.stderr)
            return 3
        print(f"NOT_FOUND {args.service}", file=sys.stderr)
        return 1
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
