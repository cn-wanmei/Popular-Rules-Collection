#!/usr/bin/env python3
"""icon_resolver.py — Service + Profile → final icon asset URL/path."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
REG = ICON / "registry.yaml"
PROF = ICON / "profiles.yaml"
THEME = ICON / "themes.yaml"
MAN = ICON / "manifest.yaml"


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


def _raw(defaults: dict, path: str | None):
    if not path:
        return None
    tmpl = defaults.get("raw_url_template") or (
        "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/assets/icons/{path}"
    )
    return tmpl.format(
        owner=defaults.get("owner", "cn-wanmei"),
        repo=defaults.get("repo", "Popular-Rules-Collection"),
        branch=defaults.get("branch", "main"),
        path=path,
    )


def resolve(service_id: str, profile: str = "client", theme: str | None = None) -> dict:
    reg = load(REG) or {}
    profiles = (load(PROF) or {}).get("profiles") or {}
    themes = (load(THEME) or {}).get("themes") or {}
    defaults = (load(MAN) or {}).get("defaults") or {}

    if theme:
        profile = str((themes.get(theme) or {}).get("profile") or profile)

    svc = (reg.get("services") or {}).get(service_id)
    if not svc:
        return {
            "service_id": service_id,
            "profile": profile,
            "variant_id": "placeholder-default",
            "role": "placeholder",
            "path_svg": "source/placeholder.svg",
            "path_png_256": "png/256/placeholder.png",
            "url_png_256": _raw(defaults, "png/256/placeholder.png"),
            "ok": False,
            "reason": "service_not_in_registry",
        }

    dbp = svc.get("default_by_profile") or {}
    preferred = list((profiles.get(profile) or {}).get("preferred") or ["default"])
    variant_id = dbp.get(profile)
    role_used = profile
    if not variant_id:
        variants = svc.get("variants") or {}
        for role in preferred:
            if role in variants:
                variant_id = variants[role]
                role_used = role
                break
        variant_id = variant_id or svc.get("default")

    vmeta = (reg.get("variants") or {}).get(variant_id) or {}
    png = vmeta.get("png") or {}
    png256 = png.get("256") or png.get(256)
    svg = vmeta.get("path")
    return {
        "service_id": service_id,
        "profile": profile,
        "theme": theme,
        "variant_id": variant_id,
        "role": vmeta.get("type") or role_used,
        "path_svg": svg,
        "path_png_256": png256,
        "url_png_256": _raw(defaults, png256) if png256 else None,
        "url_svg": _raw(defaults, svg) if svg else None,
        "color_mode": vmeta.get("color_mode"),
        "status": vmeta.get("status"),
        "ok": bool(variant_id),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("service_id", nargs="?")
    ap.add_argument("--profile", default="client")
    ap.add_argument("--theme", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()
    if args.sample:
        for sid in ("google", "wechat", "direct", "lan", "12306"):
            print(json.dumps(resolve(sid, args.profile, args.theme), ensure_ascii=False))
        return 0
    if not args.service_id:
        ap.error("service_id required unless --sample")
    r = resolve(args.service_id, args.profile, args.theme)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"{r['service_id']} [{r['profile']}] → {r['variant_id']} ({r['role']})")
        print(f"  png: {r.get('url_png_256')}")
        print(f"  svg: {r.get('url_svg')}")
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
