#!/usr/bin/env python3
"""sync_service_icons.py — Simple Icons fetch + brand.color into manifest (P1)."""
from __future__ import annotations

import json
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "icons" / "source"
MAN = ROOT / "assets" / "icons" / "manifest.yaml"
COLORS = ROOT / "assets" / "icons" / "metadata" / "colors.yaml"
DOMAINS = ROOT / "database" / "domains"

SLUG = {
    "google": "google", "apple": "apple", "github": "github", "gitlab": "gitlab",
    "telegram": "telegram", "discord": "discord", "cloudflare": "cloudflare",
    "netflix": "netflix", "facebook": "facebook", "instagram": "instagram",
    "twitter": "x", "youtube": "youtube", "tiktok": "tiktok", "whatsapp": "whatsapp",
    "reddit": "reddit", "spotify": "spotify", "steam": "steam", "epic": "epicgames",
    "docker": "docker", "baidu": "baidu", "bilibili": "bilibili", "wechat": "wechat",
    "paypal": "paypal", "stripe": "stripe", "shopify": "shopify", "notion": "notion",
    "zoom": "zoom", "figma": "figma", "dropbox": "dropbox", "twitch": "twitch",
    "signal": "signal", "line": "line", "soundcloud": "soundcloud", "vimeo": "vimeo",
    "wikipedia": "wikipedia", "uber": "uber", "airbnb": "airbnb", "ebay": "ebay",
    "binance": "binance", "huawei": "huawei", "xiaomi": "xiaomi", "jetbrains": "jetbrains",
    "atlassian": "atlassian", "trello": "trello", "vercel": "vercel", "netlify": "netlify",
    "digitalocean": "digitalocean", "hashicorp": "hashicorp", "huggingface": "huggingface",
    "claude": "anthropic", "anthropic": "anthropic", "gemini": "googlegemini",
    "copilot": "githubcopilot", "playstation": "playstation", "roblox": "roblox",
    "ea": "ea", "ubisoft": "ubisoft", "hbo": "hbo", "deezer": "deezer", "tidal": "tidal",
    "firebase": "firebase", "alibaba": "alibabadotcom", "alipay": "alipay",
    "weibo": "sinaweibo", "sina": "sinaweibo", "applemusic": "applemusic",
    "messenger": "messenger", "threads": "threads", "bluesky": "bluesky",
    "perplexity": "perplexity", "okx": "okx", "wise": "wise", "meituan": "meituan",
    "zhihu": "zhihu", "douyin": "tiktok", "icloud": "icloud", "linkedin": "linkedin",
    "slack": "slack", "adobe": "adobe", "amazon": "amazon", "aws": "amazonaws",
    "azure": "microsoftazure", "microsoft": "microsoft", "xbox": "xbox",
    "disney": "disney", "hulu": "hulu", "canva": "canva", "bbc": "bbc",
    "booking": "bookingdotcom", "heroku": "heroku", "oracle": "oracle",
    "onedrive": "microsoftonedrive", "teams": "microsoftteams", "openai": "openai",
    "walmart": "walmart", "minecraft": "minecraft", "cursor": "cursor",
}


def fetch(url: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Popular-Rules-Collection/icon-sync"})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
        return data if len(data) > 40 else None
    except Exception:
        return None


def _si_slugify(title: str) -> str:
    s = title.lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch == "+":
            out.append("plus")
        elif ch == "#":
            out.append("sharp")
    return "".join(out)


def load_simple_icons_colors() -> dict:
    url = "https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/_data/simple-icons.json"
    raw = fetch(url)
    out = {}
    if not raw:
        return out
    try:
        data = json.loads(raw.decode("utf-8"))
        items = data if isinstance(data, list) else data.get("icons") or []
        for it in items:
            if not isinstance(it, dict):
                continue
            hx = (it.get("hex") or "").strip()
            if not hx:
                continue
            hx = "#" + hx.lstrip("#")
            slug = (it.get("slug") or "").lower()
            if slug:
                out[slug] = hx
            title = it.get("title") or ""
            if title:
                out[_si_slugify(title)] = hx
    except Exception as e:
        print(f"  color load warn: {e}")
    return out


def protected(meta: dict) -> bool:
    src = meta.get("source") or {}
    prov = str(src.get("provenance") or "")
    provider = str(src.get("provider") or "")
    return prov in ("official-colors", "project") or provider in ("project-brand", "project")


def main() -> int:
    SRC.mkdir(parents=True, exist_ok=True)
    COLORS.parent.mkdir(parents=True, exist_ok=True)
    si_colors = load_simple_icons_colors()
    print(f"[sync] simple-icons colors loaded: {len(si_colors)}")

    doc = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    if not doc:
        doc = {"version": 1, "icons": {}, "service_icon_map": {}, "defaults": {}}
    icons = doc.setdefault("icons", {})
    smap = doc.setdefault("service_icon_map", {})

    ok = fail = skip = 0
    color_table = {}

    for sid, slug in sorted(SLUG.items()):
        meta = icons.get(sid) or {}
        dest = SRC / f"{sid}.svg"
        if isinstance(meta, dict) and protected(meta):
            skip += 1
            continue

        need_fetch = not dest.exists() or dest.stat().st_size < 40
        if need_fetch:
            data = fetch(f"https://cdn.simpleicons.org/{slug}")
            if not data:
                data = fetch(
                    f"https://raw.githubusercontent.com/simple-icons/simple-icons/master/icons/{slug}.svg"
                )
            if not data:
                fail += 1
                print(f"  FAIL {sid} slug={slug}")
                continue
            dest.write_bytes(data)
            ok += 1
            print(f"  OK {sid} <- {slug}")
        else:
            skip += 1

        hx = si_colors.get(slug)
        color_table[sid] = {"slug": slug, "hex": hx}
        entry = icons.get(sid) or {
            "name": sid.replace("_", " ").title(),
            "type": "service",
            "icon_key": sid,
            "service_ids": [sid],
        }
        if protected(entry):
            icons[sid] = entry
            smap[sid] = sid
            continue
        entry["source"] = {
            "provider": "simple-icons",
            "slug": slug,
            "provenance": "third_party",
            "verified": False,
            "url": f"https://simpleicons.org/?q={slug}",
        }
        if hx:
            entry.setdefault("brand", {})
            if isinstance(entry["brand"], dict):
                entry["brand"]["color"] = hx
                entry["brand"]["color_source"] = "simple-icons"
            entry["source"]["color"] = hx
        entry["files"] = {
            "svg": f"source/{sid}.svg",
            "png": {"64": f"png/64/{sid}.png", "128": f"png/128/{sid}.png", "256": f"png/256/{sid}.png"},
        }
        entry.setdefault(
            "license",
            {
                "type": "see-source",
                "note": "Simple Icons CC0-1.0 project; brand trademarks still apply.",
                "project": "https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md",
            },
        )
        entry["status"] = "sourced"
        entry["visual"] = {
            "style": "brand",
            "color_mode": "monochrome",
            "background": "transparent",
            "variants": ["monochrome"],
            "primary_color": hx,
        }
        icons[sid] = entry
        smap[sid] = sid

    doc["icons"] = icons
    doc["service_icon_map"] = smap
    doc["updated"] = str(date.today())
    MAN.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    COLORS.write_text(
        yaml.dump({"updated": str(date.today()), "source": "simple-icons", "colors": color_table},
                  allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"[sync_service_icons] ok={ok} skip={skip} fail={fail} icons={len(icons)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
