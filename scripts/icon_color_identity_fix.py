#!/usr/bin/env python3
"""Colorize mono-black brand SVGs with brand.color; fix Huawei; China flag."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "icons" / "source"
MAN = ROOT / "assets" / "icons" / "manifest.yaml"

OFFICIAL_BLACK = {
    "apple", "github", "x", "twitter", "notion", "vercel", "steam", "uber", "threads",
    "tidal", "hashicorp", "hbo", "jetbrains", "ea", "epic", "ubisoft", "wikipedia",
    "tiktok", "douyin", "cursor",
}

PALETTE = {
    "adobe": "FF0000", "airbnb": "FF5A5F", "amazon": "FF9900", "aws": "FF9900",
    "baidu": "2932E1", "binance": "F0B90B", "bluesky": "0085FF", "booking": "003580",
    "canva": "00C4CC", "claude": "D97757", "cloudflare": "F38020",
    "deezer": "FEAA2D", "digitalocean": "0080FF", "docker": "2496ED", "dropbox": "0061FF",
    "ebay": "E53238", "facebook": "0866FF", "figma": "F24E1E", "firebase": "DD2C00",
    "gitlab": "FC6D26", "heroku": "430098", "icloud": "3693F3", "instagram": "FF0069",
    "kakaotalk": "FFCD00", "line": "00C300", "linkedin": "0A66C2", "messenger": "00B2FF",
    "meta": "0467DF", "netflix": "E50914", "oracle": "F80000", "paypal": "00457C",
    "pinterest": "BD081C", "playstation": "003791", "reddit": "FF4500", "shopify": "7AB55C",
    "signal": "3A76F0", "sina": "E6162D", "slack": "4A154B", "snapchat": "FFFC00",
    "soundcloud": "FF3300", "stripe": "635BFF", "trello": "0052CC", "twitch": "9146FF",
    "vimeo": "1AB7EA", "wise": "9FE870", "youtube": "FF0000", "youtubemusic": "FF0000",
    "zoom": "0B5CFF", "huawei": "CF0A2C", "tencent": "00A4FF", "weibo": "E6162D",
    "applemusic": "FA243C", "openai": "412991", "anthropic": "D4A27F",
    "spotify": "1DB954", "telegram": "26A5E4", "discord": "5865F2", "whatsapp": "25D366",
    "wechat": "07C160", "xiaomi": "FF6900", "alibaba": "FF6A00", "alipay": "1677FF",
    "bilibili": "00A1D6", "atlassian": "0052CC", "meituan": "FFC300", "github": "181717",
    "apple": "000000",
}

CHINA_FLAG = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 30 20\">
  <rect width=\"30\" height=\"20\" fill=\"#DE2910\"/>
  <g fill=\"#FFDE00\">
    <polygon points=\"5,2 5.6,3.9 7.6,3.9 6,5.1 6.6,7 5,5.8 3.4,7 4,5.1 2.4,3.9 4.4,3.9\"/>
    <polygon transform=\"translate(8,1) scale(0.35)\" points=\"5,2 5.6,3.9 7.6,3.9 6,5.1 6.6,7 5,5.8 3.4,7 4,5.1 2.4,3.9 4.4,3.9\"/>
    <polygon transform=\"translate(10,3) scale(0.35)\" points=\"5,2 5.6,3.9 7.6,3.9 6,5.1 6.6,7 5,5.8 3.4,7 4,5.1 2.4,3.9 4.4,3.9\"/>
    <polygon transform=\"translate(10,5.5) scale(0.35)\" points=\"5,2 5.6,3.9 7.6,3.9 6,5.1 6.6,7 5,5.8 3.4,7 4,5.1 2.4,3.9 4.4,3.9\"/>
    <polygon transform=\"translate(8,7) scale(0.35)\" points=\"5,2 5.6,3.9 7.6,3.9 6,5.1 6.6,7 5,5.8 3.4,7 4,5.1 2.4,3.9 4.4,3.9\"/>
  </g>
</svg>
"""


def force_fill(svg: str, hex_color: str) -> str:
    c = hex_color if hex_color.startswith("#") else f"#{hex_color}"
    out = re.sub(r'\sfill="[^"]*"', "", svg)
    out = re.sub(r"\sfill='[^']*'", "", out)
    out = re.sub(r"<svg\b", f'<svg fill="{c}"', out, count=1)
    for tag in ("path", "circle", "polygon", "rect"):
        out = re.sub(rf"<{tag}\b", f'<{tag} fill="{c}"', out)
    return out


def fetch_si(slug: str):
    url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/11.14.0/icons/{slug}.svg"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 PRC-Icons"})
    try:
        return urllib.request.urlopen(req, timeout=20).read().decode()
    except Exception:
        return None


def main() -> int:
    h = fetch_si("huawei")
    if h:
        (SRC / "huawei.svg").write_text(force_fill(h, "CF0A2C"), encoding="utf-8")
        print("[fix] huawei <- simple-icons")
    (SRC / "china.svg").write_text(CHINA_FLAG.replace('\\"', '"'), encoding="utf-8")
    print("[fix] china <- national flag")

    man = yaml.safe_load(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    icons = man.get("icons") or {}
    n = 0
    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        svg_path = SRC / f"{key}.svg"
        if not svg_path.exists():
            continue
        ns = str(meta.get("namespace") or meta.get("type") or "")
        if ns in ("policy", "dataset", "network") and key != "china":
            continue
        bc = (meta.get("brand") or {}).get("color") or (meta.get("source") or {}).get("color")
        hexc = None
        if isinstance(bc, str):
            hexc = bc[1:] if bc.startswith("#") else bc
        hexc = hexc or PALETTE.get(key)
        if not hexc:
            continue
        text = force_fill(svg_path.read_text(encoding="utf-8", errors="replace"), hexc)
        svg_path.write_text(text, encoding="utf-8")
        meta.setdefault("brand", {})["color"] = f"#{hexc}" if not str(hexc).startswith("#") else hexc
        meta.setdefault("visual", {})["approved_mono"] = key in OFFICIAL_BLACK or hexc.upper() in (
            "000000",
            "181717",
        )
        icons[key] = meta
        n += 1
    man["icons"] = icons
    MAN.write_text(yaml.dump(man, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    print(f"[fix] color-forced svgs={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
