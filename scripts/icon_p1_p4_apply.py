#!/usr/bin/env python3
"""Icon Variants P1–P4 apply (idempotent)."""
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
CLIENT = ICON / "client_profiles.yaml"
DOCS = ROOT / "docs" / "CLIENT_ICON_PROFILES.md"

HOT = [
    "google", "youtube", "microsoft", "apple", "amazon", "meta", "facebook",
    "instagram", "whatsapp", "messenger", "telegram", "discord", "twitter", "x",
    "reddit", "linkedin", "tiktok", "spotify", "netflix", "github", "gitlab",
    "docker", "cloudflare", "openai", "anthropic", "claude", "gemini", "deepseek",
    "perplexity", "huggingface", "wechat", "qq", "baidu", "bilibili", "alibaba",
    "alipay", "taobao", "tencent", "douyin", "zhihu", "huawei", "xiaomi",
    "meituan", "netease", "steam", "epic", "twitch", "paypal", "stripe",
    "shopify", "notion", "zoom", "figma", "slack", "dropbox", "uber", "airbnb",
    "adobe", "aws", "azure", "vercel", "firebase", "icloud", "applemusic",
]

SLUG = {
    "google": "google", "youtube": "youtube", "microsoft": "microsoft", "apple": "apple",
    "amazon": "amazon", "facebook": "facebook", "instagram": "instagram",
    "whatsapp": "whatsapp", "messenger": "messenger", "telegram": "telegram",
    "discord": "discord", "twitter": "x", "x": "x", "reddit": "reddit",
    "linkedin": "linkedin", "tiktok": "tiktok", "spotify": "spotify", "netflix": "netflix",
    "github": "github", "gitlab": "gitlab", "docker": "docker", "cloudflare": "cloudflare",
    "openai": "openai", "anthropic": "anthropic", "claude": "anthropic",
    "gemini": "googlegemini", "perplexity": "perplexity", "huggingface": "huggingface",
    "wechat": "wechat", "baidu": "baidu", "bilibili": "bilibili",
    "alibaba": "alibabadotcom", "alipay": "alipay", "tencent": "tencent",
    "douyin": "tiktok", "zhihu": "zhihu", "huawei": "huawei", "xiaomi": "xiaomi",
    "meituan": "meituan", "steam": "steam", "epic": "epicgames", "twitch": "twitch",
    "paypal": "paypal", "stripe": "stripe", "shopify": "shopify", "notion": "notion",
    "zoom": "zoom", "figma": "figma", "slack": "slack", "dropbox": "dropbox",
    "uber": "uber", "airbnb": "airbnb", "adobe": "adobe", "aws": "amazonaws",
    "azure": "microsoftazure", "vercel": "vercel", "firebase": "firebase",
    "icloud": "icloud", "applemusic": "applemusic", "meta": "meta",
}

NETWORK = {
    "direct": ("#22C55E", "Direct"), "proxy": ("#3B82F6", "Proxy"),
    "reject": ("#EF4444", "Reject"), "dns": ("#A855F7", "DNS"),
    "lan": ("#64748B", "LAN"), "china": ("#EAB308", "China"),
    "geoip": ("#14B8A6", "GeoIP"), "geosite": ("#6366F1", "GeoSite"),
    "asn": ("#F472B6", "ASN"), "global": ("#0EA5E9", "Global"),
    "network": ("#94A3B8", "Network"), "placeholder": ("#94A3B8", "Placeholder"),
    "chinamobile": ("#0066CC", "China Mobile"), "chinaunicom": ("#E60027", "China Unicom"),
    "chinatelecom": ("#003399", "China Telecom"), "stun": ("#6366F1", "STUN"),
    "adblock": ("#EF4444", "AdBlock"), "gfw": ("#64748B", "GFW"),
    "private": ("#64748B", "Private"),
}


def fetch(url: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRC-icon-p14"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = r.read()
        return d if len(d) > 40 else None
    except Exception:
        return None


def geometric(name: str, rgb: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img">\n'
        f'  <title>{name}</title>\n'
        f'  <rect x="2" y="2" width="20" height="20" rx="4" fill="{rgb}" fill-opacity="0.18"/>\n'
        f'  <circle cx="12" cy="12" r="6" fill="none" stroke="{rgb}" stroke-width="1.6"/>\n'
        f"</svg>\n"
    )


def files(key: str) -> dict:
    return {
        "svg": f"source/{key}.svg",
        "png": {"64": f"png/64/{key}.png", "128": f"png/128/{key}.png", "256": f"png/256/{key}.png"},
    }


def load_si_colors() -> dict:
    raw = fetch("https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/_data/simple-icons.json")
    out = {}
    if not raw:
        return out
    try:
        data = json.loads(raw.decode())
        for it in data.get("icons") or []:
            hx = (it.get("hex") or "").strip()
            title = (it.get("title") or "").lower()
            if not hx:
                continue
            hx = "#" + hx.lstrip("#")
            slug = "".join(c for c in title if c.isalnum())
            out[slug] = hx
            if it.get("slug"):
                out[str(it["slug"]).lower()] = hx
    except Exception:
        pass
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
    si_colors = load_si_colors()

    for key, (color, title) in NETWORK.items():
        p = SRC / f"{key}.svg"
        if not p.exists() or p.stat().st_size < 40:
            p.write_text(geometric(title, color), encoding="utf-8")
        icons[key] = {
            "name": title,
            "type": "policy" if key in ("direct", "proxy", "reject", "dns", "global", "placeholder")
            else ("dataset" if key in ("china", "geoip", "geosite", "asn") else "network"),
            "icon_key": key,
            "source": {"provider": "project", "provenance": "project", "method": "geometric", "verified": True},
            "files": files(key),
            "license": {"type": "CC0-1.0", "note": "Project geometric mark"},
            "status": "verified",
            "visual": {"style": "geometric", "color_mode": "color", "background": "transparent", "variants": ["color"]},
            "brand": {"color": color, "color_source": "project"},
        }
        smap.setdefault(key, key)

    p1_ok = p1_skip = p1_fail = 0
    for sid in HOT:
        slug = SLUG.get(sid)
        if not slug:
            continue
        meta = icons.get(sid) or {}
        if isinstance(meta, dict) and protected(meta):
            p1_skip += 1
            smap[sid] = sid
            continue
        dest = SRC / f"{sid}.svg"
        if not dest.exists() or dest.stat().st_size < 40:
            data = fetch(f"https://cdn.simpleicons.org/{slug}") or fetch(
                f"https://raw.githubusercontent.com/simple-icons/simple-icons/master/icons/{slug}.svg"
            )
            if not data:
                p1_fail += 1
                continue
            dest.write_bytes(data)
            p1_ok += 1
        else:
            p1_skip += 1
        hx = si_colors.get(slug)
        entry = icons.get(sid) or {"name": sid.title(), "type": "service", "icon_key": sid}
        if not protected(entry):
            entry["source"] = {
                "provider": "simple-icons", "slug": slug,
                "provenance": "third_party", "verified": False,
            }
            if hx:
                entry["brand"] = {"color": hx, "color_source": "simple-icons"}
                entry["source"]["color"] = hx
            entry["files"] = files(sid)
            entry["status"] = "sourced"
            entry["license"] = {"type": "see-source", "note": "Simple Icons; brand trademarks apply."}
            entry["visual"] = {
                "style": "brand", "color_mode": "monochrome", "background": "transparent",
                "variants": ["monochrome", "brand"], "primary_color": hx,
            }
            icons[sid] = entry
        smap[sid] = sid

    domains = ROOT / "database" / "domains"
    domain_ids = {p.stem for p in domains.glob("*.txt")} if domains.is_dir() else set()
    for sid in sorted(domain_ids):
        if sid in smap and smap[sid]:
            continue
        if (SRC / f"{sid}.svg").exists():
            smap[sid] = sid
            continue
        smap[sid] = "placeholder"

    man["icons"] = icons
    man["service_icon_map"] = smap
    man["updated"] = str(date.today())
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")

    base = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons"
    client = {
        "version": 1,
        "updated": str(date.today()),
        "description": "Per-client Icon Profile + URL templates",
        "default_profile": "client",
        "clients": {
            k: {
                "profile": "client",
                "formats": ["png"],
                "preferred_size": 256 if k not in ("mihomo", "singbox") else 128,
                "url_template": f"{base}/png/{{size}}/{{icon_key}}.png",
            }
            for k in ("surge", "loon", "egern", "mihomo", "singbox", "shadowrocket", "quantumultx")
        },
        "resolver": "python scripts/icon_resolver.py {service_id} --profile client",
    }
    CLIENT.write_text(yaml.dump(client, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"[icon_p1_p4] icons={len(icons)} map={len(smap)} p1_ok={p1_ok} fail={p1_fail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
