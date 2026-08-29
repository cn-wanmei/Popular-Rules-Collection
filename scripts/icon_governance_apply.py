#!/usr/bin/env python3
"""icon_governance_apply.py — P0–P4 Icon Dataset governance (idempotent)."""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "assets/icons/manifest.yaml"
SRC = ROOT / "assets/icons/source"
DOMAINS = ROOT / "database/domains"
SERVICES = ROOT / "database/services"
PRIM = ROOT / "config/service_primary.yaml"
EXTRA = ROOT / "config/service_primary_extra.yaml"
DEC = ROOT / "assets/icons/decisions.yaml"

POLICY = {
    "direct", "proxy", "reject", "dns", "lan", "china", "global", "geoip",
    "geosite", "asn", "network", "placeholder",
}
NETWORK_EXTRA = {
    "chinamobile": ("#0066CC", "China Mobile"),
    "chinaunicom": ("#E60027", "China Unicom"),
    "chinatelecom": ("#003399", "China Telecom"),
    "stun": ("#6366F1", "STUN"),
    "adblock": ("#EF4444", "AdBlock"),
    "gfw": ("#64748B", "GFW"),
    "private": ("#64748B", "Private"),
}
COLOR_OK = {
    "google", "microsoft", "youtube", "spotify", "netflix", "discord", "telegram",
    "whatsapp", "docker", "facebook", "reddit", "tiktok", "wechat", "baidu",
    "bilibili", "alibaba", "alipay", "zhihu", "douyin", "huawei", "xiaomi",
    "meituan", "tencent", "openai", "anthropic", "claude", "gemini", "deepseek",
    "perplexity", "huggingface",
}


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


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


def is_color_svg(p: Path) -> bool:
    t = p.read_text(encoding="utf-8", errors="replace")
    fills = set(re.findall(r'fill=["\']([^"\']+)["\']', t, flags=re.I))
    fills = {f.lower() for f in fills if f.lower() not in ("none", "transparent")}
    if len(fills) >= 2:
        return True
    if len(fills) == 1:
        f = next(iter(fills))
        if f not in ("#000", "#000000", "black", "#0f172a", "#111", "#111111", "#fff", "#ffffff", "white"):
            return True
    return False


def main() -> int:
    domain_ids = {p.stem for p in DOMAINS.glob("*.txt")} if DOMAINS.is_dir() else set()
    svc_ids = {p.stem for p in SERVICES.glob("*.yaml")} if SERVICES.is_dir() else set()
    primary, extra = load(PRIM), load(EXTRA)
    services_meta = dict(primary.get("services") or {})
    services_meta.update(extra.get("services") or {})
    expected = sorted(domain_ids | svc_ids | set(services_meta.keys()))

    doc = load(MAN) or {"version": 1, "icons": {}, "service_icon_map": {}, "defaults": {}}
    icons = doc.setdefault("icons", {})
    smap = doc.setdefault("service_icon_map", {})
    SRC.mkdir(parents=True, exist_ok=True)

    for key, (color, title) in NETWORK_EXTRA.items():
        p = SRC / f"{key}.svg"
        if not p.exists() or p.stat().st_size < 40:
            p.write_text(geometric(title, color), encoding="utf-8")
        icons[key] = {
            "name": title,
            "type": "network" if key in ("stun", "private") else "dataset",
            "icon_key": key,
            "source": {"provider": "project", "provenance": "project", "method": "geometric", "verified": True},
            "files": files(key),
            "license": {"type": "CC0-1.0", "note": "Project geometric mark"},
            "status": "verified",
            "visual": {"style": "geometric", "color_mode": "color", "background": "transparent", "variants": ["color"]},
        }
        smap[key] = key

    for key, color, title in [
        ("placeholder", "#94A3B8", "Placeholder"),
        ("direct", "#22C55E", "Direct"),
        ("proxy", "#3B82F6", "Proxy"),
        ("reject", "#EF4444", "Reject"),
        ("dns", "#A855F7", "DNS"),
        ("lan", "#64748B", "LAN"),
        ("china", "#EAB308", "China"),
        ("geoip", "#14B8A6", "GeoIP"),
        ("geosite", "#6366F1", "GeoSite"),
        ("asn", "#F472B6", "ASN"),
        ("global", "#0EA5E9", "Global"),
        ("network", "#94A3B8", "Network"),
    ]:
        p = SRC / f"{key}.svg"
        if not p.exists() or p.stat().st_size < 40:
            p.write_text(geometric(title, color), encoding="utf-8")
        icons[key] = {
            "name": title,
            "type": "policy" if key in ("direct", "proxy", "reject", "dns", "global", "placeholder") else (
                "dataset" if key in ("china", "geoip", "geosite", "asn") else "network"
            ),
            "icon_key": key,
            "source": {"provider": "project", "provenance": "project", "method": "geometric", "verified": True},
            "files": files(key),
            "license": {"type": "CC0-1.0", "note": "Project geometric mark"},
            "status": "verified",
            "visual": {"style": "geometric", "color_mode": "color", "background": "transparent", "variants": ["color"]},
        }

    for key in ("sina", "weibo"):
        meta = icons.get(key) or {"name": key.title(), "type": "service", "icon_key": key}
        meta["relation"] = "shared_brand"
        meta["brand"] = {"owner": "sina", "product": "weibo", "relation": "shared_brand"}
        meta.setdefault("source", {})
        meta["source"].setdefault("provider", "simple-icons")
        meta["source"]["provenance"] = meta["source"].get("provenance") or "third_party"
        meta.setdefault("files", files(key))
        meta.setdefault("license", {"type": "see-source", "note": "Shared Sina Weibo mark"})
        meta["status"] = meta.get("status") or "sourced"
        meta["visual"] = {"style": "brand", "color_mode": "monochrome", "background": "transparent", "variants": ["monochrome"]}
        icons[key] = meta
        smap[key] = key

    for svg in sorted(SRC.glob("*.svg")):
        key = svg.stem
        if key in POLICY or key in NETWORK_EXTRA or key in ("sina", "weibo"):
            continue
        meta = icons.get(key) or {}
        meta.setdefault("name", key.replace("_", " ").title())
        meta.setdefault("icon_key", key)
        meta["files"] = files(key)
        meta["type"] = meta.get("type") or "service"
        if key in COLOR_OK and is_color_svg(svg):
            meta["source"] = {"provider": "project-brand", "provenance": "official-colors", "verified": True}
            meta["visual"] = {"style": "brand", "color_mode": "color", "background": "transparent", "variants": ["color"]}
            meta["license"] = {"type": "brand-guidelines", "note": "Identification mark; trademarks apply."}
            meta["status"] = "verified"
        elif key in ("apple", "github"):
            meta["source"] = {"provider": "project-brand", "provenance": "official-colors", "verified": True}
            meta["visual"] = {"style": "brand", "color_mode": "monochrome", "background": "transparent", "variants": ["monochrome"]}
            meta.setdefault("license", {"type": "see-source", "note": "Brand monochrome"})
            meta["status"] = "verified"
        else:
            meta["source"] = {
                "provider": str((meta.get("source") or {}).get("provider") or "simple-icons"),
                "provenance": "third_party",
                "verified": False,
            }
            color = is_color_svg(svg)
            meta["visual"] = {
                "style": "brand",
                "color_mode": "color" if color else "monochrome",
                "background": "transparent",
                "variants": ["color"] if color else ["monochrome"],
            }
            meta.setdefault("license", {"type": "see-source", "note": "Third-party; trademarks apply."})
            meta["status"] = "sourced"
        icons[key] = meta
        smap.setdefault(key, key)

    ph = []
    for sid in expected:
        if sid in smap:
            continue
        if (SRC / f"{sid}.svg").exists() or sid in icons:
            smap[sid] = sid
            continue
        smap[sid] = "placeholder"
        ph.append(sid)

    doc["icons"] = icons
    doc["service_icon_map"] = smap
    doc["updated"] = str(date.today())
    doc["governance"] = {
        "decision_coverage_target": "100%",
        "placeholder_allowed": True,
        "phases_applied": ["P0_placeholder", "P1_provenance", "P2_network", "P3_shared_brand"],
    }
    MAN.parent.mkdir(parents=True, exist_ok=True)
    MAN.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    DEC.write_text(
        yaml.dump(
            {
                "date": str(date.today()),
                "placeholder_services": sorted(ph),
                "shared_brand": ["sina", "weibo"],
                "network_project": sorted(NETWORK_EXTRA.keys()),
            },
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    print(
        f"[icon_governance] icons={len(icons)} map={len(smap)} "
        f"placeholder_new={len(ph)} coverage={sum(1 for s in expected if s in smap)}/{len(expected)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
