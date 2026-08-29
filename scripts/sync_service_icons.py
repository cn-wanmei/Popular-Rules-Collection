#!/usr/bin/env python3
"""sync_service_icons.py — fetch Simple Icons SVGs for services with domain rules."""
from __future__ import annotations

import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "icons" / "source"
MAN = ROOT / "assets" / "icons" / "manifest.yaml"
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
    "pinterest": "pinterest", "snapchat": "snapchat", "signal": "signal", "line": "line",
    "soundcloud": "soundcloud", "vimeo": "vimeo", "wikipedia": "wikipedia",
    "uber": "uber", "airbnb": "airbnb", "ebay": "ebay", "binance": "binance",
    "huawei": "huawei", "xiaomi": "xiaomi", "jetbrains": "jetbrains",
    "atlassian": "atlassian", "trello": "trello", "vercel": "vercel", "netlify": "netlify",
    "digitalocean": "digitalocean", "hashicorp": "hashicorp", "huggingface": "huggingface",
    "claude": "anthropic", "anthropic": "anthropic", "gemini": "googlegemini",
    "copilot": "githubcopilot", "playstation": "playstation", "roblox": "roblox",
    "rockstar": "rockstargames", "ea": "ea", "ubisoft": "ubisoft", "hbo": "hbo",
    "paramountplus": "paramountplus", "deezer": "deezer", "tidal": "tidal",
    "emby": "emby", "firebase": "firebase", "kakaotalk": "kakaotalk", "naver": "naver",
    "alibaba": "alibabadotcom", "alipay": "alipay", "weibo": "sinaweibo", "sina": "sinaweibo",
    "applemusic": "applemusic", "youtubemusic": "youtubemusic", "appletv": "appletv",
    "messenger": "messenger", "threads": "threads", "bluesky": "bluesky",
    "perplexity": "perplexity", "okx": "okx", "wise": "wise", "speedtest": "speedtest",
    "oppo": "oppo", "vivo": "vivo", "meituan": "meituan", "zhihu": "zhihu",
    "douyin": "tiktok", "icloud": "icloud",
}

POLICY = {
    "direct", "proxy", "reject", "dns", "lan", "china", "global", "geoip",
    "geosite", "asn", "network", "placeholder",
}


def fetch(slug: str):
    url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/master/icons/{slug}.svg"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Popular-Rules-Collection/icon-sync"})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
        return data if len(data) > 40 else None
    except Exception:
        return None


def main() -> int:
    SRC.mkdir(parents=True, exist_ok=True)
    ok = fail = skip = 0
    domain_ids = {p.stem for p in DOMAINS.glob("*.txt")} if DOMAINS.is_dir() else set()
    for sid, slug in sorted(SLUG.items()):
        if domain_ids and sid not in domain_ids:
            continue
        dest = SRC / f"{sid}.svg"
        if dest.exists() and dest.stat().st_size > 40:
            skip += 1
            continue
        data = fetch(slug)
        if not data:
            fail += 1
            print(f"  FAIL {sid} slug={slug}")
            continue
        dest.write_bytes(data)
        ok += 1
        print(f"  OK {sid} <- {slug}")

    doc = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    if not doc:
        doc = {"version": 1, "icons": {}, "service_icon_map": {}, "defaults": {}}
    icons = doc.setdefault("icons", {})
    smap = doc.setdefault("service_icon_map", {})
    doc["updated"] = str(date.today())
    for svg in sorted(SRC.glob("*.svg")):
        key = svg.stem
        if key in POLICY:
            continue
        if key not in icons:
            icons[key] = {
                "name": key.replace("_", " ").title(),
                "type": "service",
                "icon_key": key,
                "service_ids": [key],
                "source": {"provider": "simple-icons", "url": "https://github.com/simple-icons/simple-icons"},
                "files": {
                    "svg": f"source/{key}.svg",
                    "png": {"64": f"png/64/{key}.png", "128": f"png/128/{key}.png", "256": f"png/256/{key}.png"},
                },
                "license": {
                    "type": "see-source",
                    "note": "Simple Icons project CC0-1.0; brand trademarks still apply.",
                    "project": "https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md",
                },
                "status": "sourced",
            }
        smap[key] = key
    MAN.parent.mkdir(parents=True, exist_ok=True)
    MAN.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[sync_service_icons] ok={ok} skip={skip} fail={fail} icons={len(icons)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
