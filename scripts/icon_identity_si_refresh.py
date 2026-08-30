#!/usr/bin/env python3
"""Refresh brand SVGs from Simple Icons — fix wrong project-redraw identities."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "icons" / "source"
MAN = ROOT / "assets" / "icons" / "manifest.yaml"
UA = {"User-Agent": "Mozilla/5.0 PRC-Icons"}

CANDIDATES = {
    "alibaba": ["alibabadotcom", "alibaba"],
    "alipay": ["alipay"],
    "tencent": ["tencentqq"],
    "wechat": ["wechat"],
    "baidu": ["baidu"],
    "bilibili": ["bilibili"],
    "xiaomi": ["xiaomi"],
    "huawei": ["huawei"],
    "tiktok": ["tiktok"],
    "douyin": ["tiktok"],
    "meituan": ["meituan"],
    "oppo": ["oppo"],
    "vivo": ["vivo"],
    "amazon": ["amazon"],
    "adobe": ["adobe"],
    "cloudflare": ["cloudflare"],
    "facebook": ["facebook"],
    "instagram": ["instagram"],
    "netflix": ["netflix"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "docker": ["docker"],
    "discord": ["discord"],
    "telegram": ["telegram"],
    "whatsapp": ["whatsapp"],
    "youtube": ["youtube"],
    "spotify": ["spotify"],
    "linkedin": ["linkedin"],
    "reddit": ["reddit"],
    "twitch": ["twitch"],
    "steam": ["steam"],
    "paypal": ["paypal"],
    "stripe": ["stripe"],
    "shopify": ["shopify"],
    "apple": ["apple"],
    "microsoft": ["microsoft"],
    "google": ["google"],
    "openai": ["openai"],
    "anthropic": ["anthropic"],
    "dropbox": ["dropbox"],
    "ebay": ["ebay"],
    "figma": ["figma"],
    "firebase": ["firebase"],
    "heroku": ["heroku"],
    "line": ["line"],
    "messenger": ["messenger"],
    "meta": ["meta"],
    "notion": ["notion"],
    "oracle": ["oracle"],
    "pinterest": ["pinterest"],
    "playstation": ["playstation"],
    "signal": ["signal"],
    "slack": ["slack"],
    "snapchat": ["snapchat"],
    "soundcloud": ["soundcloud"],
    "trello": ["trello"],
    "twitter": ["x"],
    "x": ["x"],
    "uber": ["uber"],
    "vercel": ["vercel"],
    "vimeo": ["vimeo"],
    "wikipedia": ["wikipedia"],
    "zoom": ["zoom"],
    "airbnb": ["airbnb"],
    "binance": ["binance"],
    "bluesky": ["bluesky"],
    "canva": ["canva"],
    "atlassian": ["atlassian"],
    "aws": ["amazonaws"],
    "deezer": ["deezer"],
    "digitalocean": ["digitalocean"],
    "epic": ["epicgames"],
    "hbo": ["hbo"],
    "icloud": ["icloud"],
    "kakaotalk": ["kakaotalk"],
    "sina": ["sinaweibo"],
    "weibo": ["sinaweibo"],
    "speedtest": ["speedtest"],
    "tidal": ["tidal"],
    "threads": ["threads"],
    "wise": ["wise"],
    "youtubemusic": ["youtubemusic"],
}

COLORS = {
    "alibaba": "FF6A00", "alipay": "1677FF", "tencent": "12B7F5", "wechat": "07C160",
    "baidu": "2932E1", "bilibili": "00A1D6", "xiaomi": "FF6900", "huawei": "CF0A2C",
    "meituan": "FFD100", "tiktok": "000000", "douyin": "000000", "amazon": "FF9900",
    "adobe": "FF0000", "cloudflare": "F38020", "facebook": "0866FF", "instagram": "FF0069",
    "netflix": "E50914", "github": "181717", "gitlab": "FC6D26", "docker": "2496ED",
    "discord": "5865F2", "telegram": "26A5E4", "whatsapp": "25D366", "youtube": "FF0000",
    "spotify": "1DB954", "linkedin": "0A66C2", "reddit": "FF4500", "twitch": "9146FF",
    "steam": "000000", "paypal": "00457C", "stripe": "635BFF", "shopify": "7AB55C",
    "apple": "000000", "openai": "412991", "anthropic": "D4A27F", "dropbox": "0061FF",
    "ebay": "E53238", "figma": "F24E1E", "firebase": "DD2C00", "heroku": "430098",
    "line": "00C300", "messenger": "00B2FF", "meta": "0467DF", "notion": "000000",
    "oracle": "F80000", "pinterest": "BD081C", "playstation": "003791", "signal": "3A76F0",
    "slack": "4A154B", "snapchat": "FFFC00", "soundcloud": "FF3300", "trello": "0052CC",
    "x": "000000", "twitter": "000000", "uber": "000000", "vercel": "000000",
    "vimeo": "1AB7EA", "wikipedia": "000000", "zoom": "0B5CFF", "airbnb": "FF5A5F",
    "binance": "F0B90B", "bluesky": "0085FF", "canva": "00C4CC", "atlassian": "0052CC",
    "aws": "FF9900", "deezer": "FEAA2D", "digitalocean": "0080FF", "epic": "000000",
    "hbo": "000000", "icloud": "3693F3", "kakaotalk": "FFCD00", "sina": "E6162D",
    "weibo": "E6162D", "tidal": "000000", "threads": "000000", "wise": "9FE870",
    "youtubemusic": "FF0000", "oppo": "1A472A", "vivo": "415FFF",
}

OFFICIAL_BLACK = {
    "apple", "github", "x", "twitter", "notion", "vercel", "steam", "uber",
    "threads", "tidal", "hbo", "epic", "wikipedia", "tiktok", "douyin",
}


def fetch_si(slug: str):
    for ver in ("11.14.0", "9.21.0"):
        url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/{ver}/icons/{slug}.svg"
        req = urllib.request.Request(url, headers=UA)
        try:
            return urllib.request.urlopen(req, timeout=15).read().decode()
        except Exception:
            continue
    return None


def force_fill(svg: str, hex_color: str) -> str:
    c = hex_color if hex_color.startswith("#") else f"#{hex_color}"
    fills = re.findall(r'fill="(#[0-9A-Fa-f]{3,8})"', svg)
    distinct = {f.upper() for f in fills if f.upper() not in ("#000", "#000000", "#FFF", "#FFFFFF")}
    if len(distinct) >= 2:
        return svg
    out = re.sub(r'\sfill="[^"]*"', "", svg)
    out = re.sub(r"\sfill='[^']*'", "", out)
    out = re.sub(r"<svg\b", f'<svg fill="{c}"', out, count=1)
    for tag in ("path", "circle", "polygon", "rect"):
        out = re.sub(rf"<{tag}\b", f'<{tag} fill="{c}"', out)
    return out


def main() -> int:
    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    n = 0
    for key, slugs in sorted(CANDIDATES.items()):
        svg = None
        used = None
        for s in slugs:
            svg = fetch_si(s)
            if svg:
                used = s
                break
        if not svg:
            print(f"  SKIP {key}")
            continue
        hexc = COLORS.get(key, "000000")
        svg = force_fill(svg, hexc)
        (SRC / f"{key}.svg").write_text(svg, encoding="utf-8")
        meta = icons.get(key) or {"name": key.title(), "type": "service", "icon_key": key}
        meta.setdefault("source", {})
        meta["source"].update(
            {"provider": "simple-icons", "slug": used, "provenance": "third_party", "type": "simple-icons"}
        )
        meta.setdefault("brand", {})["color"] = f"#{hexc}"
        meta["brand"]["color_source"] = "simple-icons"
        meta.setdefault("visual", {})["approved_mono"] = key in OFFICIAL_BLACK
        meta.setdefault("files", {})["svg"] = f"source/{key}.svg"
        icons[key] = meta
        n += 1
    man["icons"] = icons
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[identity_si_refresh] replaced={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
