#!/usr/bin/env python3
"""Phase II: ensure CORE ~50 brands have SVG + brand.color (SI or existing)."""
from __future__ import annotations

import json
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
SRC = ICON / "source"
MAN = ICON / "manifest.yaml"
REP = ROOT / "reports" / "phase2_core_icons.md"

CORE_SLUG = {
    "google": "google", "youtube": "youtube", "microsoft": "microsoft", "apple": "apple",
    "amazon": "amazon", "aws": "amazonwebservices", "facebook": "facebook", "instagram": "instagram",
    "whatsapp": "whatsapp", "telegram": "telegram", "discord": "discord", "twitter": "x", "x": "x",
    "reddit": "reddit", "linkedin": "linkedin", "tiktok": "tiktok", "spotify": "spotify",
    "netflix": "netflix", "github": "github", "gitlab": "gitlab", "docker": "docker",
    "cloudflare": "cloudflare", "openai": "openai", "anthropic": "anthropic", "claude": "anthropic",
    "gemini": "googlegemini", "perplexity": "perplexity", "huggingface": "huggingface",
    "wechat": "wechat", "baidu": "baidu", "bilibili": "bilibili", "alibaba": "alibabadotcom",
    "alipay": "alipay", "tencent": "tencent", "douyin": "tiktok", "zhihu": "zhihu",
    "huawei": "huawei", "xiaomi": "xiaomi", "meituan": "meituan", "steam": "steam",
    "paypal": "paypal", "stripe": "stripe", "shopify": "shopify", "notion": "notion",
    "zoom": "zoom", "figma": "figma", "slack": "slack", "dropbox": "dropbox", "uber": "uber",
    "adobe": "adobe", "firebase": "firebase", "vercel": "vercel", "icloud": "icloud",
    "messenger": "messenger", "signal": "signal", "line": "line", "twitch": "twitch",
}


def fetch(url: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRC-phase2"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = r.read()
        return d if len(d) > 40 else None
    except Exception:
        return None


def load_colors() -> dict:
    raw = fetch("https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/_data/simple-icons.json")
    out = {}
    if not raw:
        return out
    for it in json.loads(raw.decode()).get("icons") or []:
        hx = (it.get("hex") or "").strip()
        if not hx:
            continue
        hx = "#" + hx.lstrip("#")
        title = "".join(c for c in (it.get("title") or "").lower() if c.isalnum())
        out[title] = hx
        if it.get("slug"):
            out[str(it["slug"]).lower()] = hx
    return out


def protected(meta: dict) -> bool:
    src = meta.get("source") or {}
    return str(src.get("provenance") or "") in ("official-colors", "project") or str(
        src.get("provider") or ""
    ) in ("project-brand", "project")


def main() -> int:
    SRC.mkdir(parents=True, exist_ok=True)
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.setdefault("icons", {})
    smap = man.setdefault("service_icon_map", {})
    col = load_colors()
    ok = skip = fail = color_fill = 0
    lines = ["# Phase II Core Brands", "", f"date: {date.today()}", ""]

    for sid, slug in sorted(CORE_SLUG.items()):
        meta = icons.get(sid) or {}
        if isinstance(meta, dict) and protected(meta):
            skip += 1
            smap[sid] = sid
            if not (meta.get("brand") or {}).get("color") and col.get(slug):
                meta.setdefault("brand", {})["color"] = col[slug]
                meta["brand"]["color_source"] = "simple-icons-ref"
                icons[sid] = meta
                color_fill += 1
            lines.append(f"- `{sid}`: protected/{meta.get('status')}")
            continue
        dest = SRC / f"{sid}.svg"
        if not dest.exists() or dest.stat().st_size < 40:
            data = fetch(f"https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/{slug}.svg")
            if not data:
                fail += 1
                lines.append(f"- `{sid}`: FAIL no SI")
                continue
            dest.write_bytes(data)
            ok += 1
        else:
            skip += 1
        hx = col.get(slug)
        entry = icons.get(sid) or {"name": sid.title(), "type": "service", "icon_key": sid}
        if not protected(entry):
            entry["source"] = {
                "provider": "simple-icons",
                "slug": slug,
                "provenance": "third_party",
                "verified": False,
                "phase": "II",
            }
            if hx:
                entry["brand"] = {"color": hx, "color_source": "simple-icons"}
                entry["source"]["color"] = hx
            entry["files"] = {
                "svg": f"source/{sid}.svg",
                "png": {"64": f"png/64/{sid}.png", "128": f"png/128/{sid}.png", "256": f"png/256/{sid}.png"},
            }
            entry["status"] = "sourced"
            entry["license"] = {"type": "see-source", "note": "Simple Icons; trademarks apply."}
            entry["visual"] = {
                "style": "brand",
                "color_mode": "monochrome",
                "background": "transparent",
                "primary_color": hx,
                "phase": "II",
            }
            icons[sid] = entry
        smap[sid] = sid
        lines.append(f"- `{sid}`: sourced")

    man["icons"] = icons
    man["service_icon_map"] = smap
    man["updated"] = str(date.today())
    man["phase_ii"] = {"core": len(CORE_SLUG), "ok": ok, "fail": fail}
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    lines.insert(4, f"- fetched={ok} skip={skip} fail={fail} color_fill={color_fill}")
    lines.insert(5, "")
    REP.parent.mkdir(parents=True, exist_ok=True)
    REP.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[icon_phase2_core] ok={ok} skip={skip} fail={fail} color_fill={color_fill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
