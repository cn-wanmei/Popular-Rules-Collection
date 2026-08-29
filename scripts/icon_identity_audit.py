#!/usr/bin/env python3
"""icon_identity_audit.py — Phase-1 Icon Dataset inventory & identity mismatch.

Read-only governance: does NOT download or replace icons.
Outputs reports/<day>/icon_identity_audit.json + ICON_IDENTITY_AUDIT.md
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "assets/icons/manifest.yaml"
SRC = ROOT / "assets/icons/source"
PNG256 = ROOT / "assets/icons/png/256"
DOMAINS = ROOT / "database/domains"
SERVICES = ROOT / "database/services"
PRIM = ROOT / "config/service_primary.yaml"
EXTRA = ROOT / "config/service_primary_extra.yaml"

KNOWN_CHILD_PARENT = {
    "youtube": "google",
    "youtubemusic": "youtube",
    "applemusic": "apple",
    "appletv": "apple",
    "icloud": "apple",
    "onedrive": "microsoft",
    "teams": "microsoft",
    "xbox": "microsoft",
    "azure": "microsoft",
    "aws": "amazon",
    "primevideo": "amazon",
    "tencentvideo": "tencent",
    "wechat": "tencent",
    "alipay": "alibaba",
    "douyin": "bytedance",
    "tiktok": "bytedance",
    "instagram": "facebook",
    "messenger": "facebook",
    "whatsapp": "facebook",
    "threads": "facebook",
}
NETWORK_IDS = {
    "geoip", "geosite", "asn", "lan", "china", "chinamobile", "chinaunicom",
    "chinatelecom", "proxy", "direct", "reject", "dns", "private", "stun",
    "adblock", "gfw",
}
HIGH_FREQ = {
    "google", "apple", "microsoft", "amazon", "youtube", "netflix", "spotify",
    "discord", "telegram", "wechat", "baidu", "bilibili", "alibaba", "alipay",
    "zhihu", "douyin", "huawei", "openai", "claude", "github", "facebook",
    "instagram", "twitter", "tiktok", "steam", "docker", "cloudflare",
}
POLICY = {
    "direct", "proxy", "reject", "dns", "lan", "china", "global", "geoip",
    "geosite", "asn", "network", "placeholder",
}


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def svg_mono_black(p: Path) -> dict:
    t = p.read_text(encoding="utf-8", errors="replace")
    fills = set(re.findall(r'fill=["\']([^"\']+)["\']', t, flags=re.I))
    fills = {f.lower() for f in fills if f.lower() not in ("none", "transparent")}
    no_fill = "fill=" not in t.lower()
    mono = len(fills) <= 1 or no_fill
    blackish = no_fill or any(
        f in ("#000", "#000000", "black", "#0f172a", "#111", "#111111") for f in fills
    )
    return {"mono": mono, "blackish": blackish and mono, "fills": sorted(fills)[:5]}


def main() -> int:
    domain_ids = {p.stem for p in DOMAINS.glob("*.txt")} if DOMAINS.is_dir() else set()
    svc_ids = {p.stem for p in SERVICES.glob("*.yaml")} if SERVICES.is_dir() else set()
    primary, extra = load(PRIM), load(EXTRA)
    services_meta = dict(primary.get("services") or {})
    services_meta.update(extra.get("services") or {})
    expected = sorted(domain_ids | svc_ids | set(services_meta.keys()))

    parents = {}
    for sid, meta in services_meta.items():
        if isinstance(meta, dict) and meta.get("parent"):
            parents[sid] = str(meta["parent"])

    manifest = load(MAN)
    icons = manifest.get("icons") or {}
    smap = dict(manifest.get("service_icon_map") or {})
    source_svgs = {p.stem: p for p in SRC.glob("*.svg")} if SRC.is_dir() else {}
    pngs = {p.stem: p for p in PNG256.glob("*.png")} if PNG256.is_dir() else {}

    hash_to_keys = defaultdict(list)
    for key, p in source_svgs.items():
        hash_to_keys[sha16(p)].append(key)
    duplicates = {h: keys for h, keys in hash_to_keys.items() if len(keys) > 1}

    parent_reuse = []
    for sid in expected:
        icon_key = smap.get(sid) or (sid if sid in icons else None)
        if not icon_key:
            continue
        parent = KNOWN_CHILD_PARENT.get(sid) or parents.get(sid)
        if parent and icon_key == parent and sid != parent:
            meta = icons.get(icon_key) or {}
            rel = (meta.get("brand") or {}).get("relation") or meta.get("relation")
            if rel not in ("parent_brand", "shared_brand", "aggregate"):
                parent_reuse.append(
                    {
                        "service": sid,
                        "icon_key": icon_key,
                        "issue": "uses_parent_icon_without_relation",
                    }
                )

    missing = [
        sid
        for sid in expected
        if sid not in smap and sid not in icons and sid not in source_svgs
    ]
    orphan = [
        key
        for key in sorted(set(icons) | set(source_svgs))
        if key not in POLICY and key not in smap.values() and key not in expected
    ]

    mono_list, black_list = [], []
    for key, p in source_svgs.items():
        m = svg_mono_black(p)
        if m["mono"]:
            mono_list.append(key)
        if m["blackish"]:
            black_list.append(key)

    no_prov = []
    for key, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        if not ((meta.get("source") or {}).get("provenance")):
            no_prov.append(key)

    should_official = []
    for sid in sorted(HIGH_FREQ):
        meta = icons.get(sid) or icons.get(smap.get(sid) or "") or {}
        prov = str(
            ((meta.get("source") or {}).get("provenance"))
            or ((meta.get("source") or {}).get("provider"))
            or ""
        )
        if sid not in source_svgs:
            should_official.append({"id": sid, "reason": "missing source svg"})
        elif prov in ("third_party", "simple-icons", "") and svg_mono_black(source_svgs[sid])["blackish"]:
            should_official.append({"id": sid, "reason": "high-freq still blackish third_party"})

    network_need = []
    for nid in sorted(NETWORK_IDS):
        if nid in source_svgs or nid in icons:
            meta = icons.get(nid) or {}
            provider = str(((meta.get("source") or {}).get("provider") or ""))
            prov = str(((meta.get("source") or {}).get("provenance") or ""))
            if provider == "simple-icons" or prov == "third_party":
                network_need.append(nid)
        else:
            network_need.append(nid)

    mapped = sum(1 for s in expected if s in smap or s in icons or s in source_svgs)
    day = str(date.today())
    report = {
        "date": day,
        "phase": 1,
        "summary": {
            "expected_services": len(expected),
            "manifest_icons": len(icons),
            "source_svgs": len(source_svgs),
            "png_256": len(pngs),
            "mapped_services": mapped,
            "missing_service_icons": len(missing),
            "orphan_icons": len(orphan),
            "duplicate_hash_groups": len(duplicates),
            "parent_reuse_without_relation": len(parent_reuse),
            "mono_svgs": len(mono_list),
            "blackish_svgs": len(black_list),
            "no_provenance": len(no_prov),
            "should_prefer_official": len(should_official),
            "network_need_project_icon": len(network_need),
        },
        "parent_reuse": parent_reuse,
        "duplicate_groups": {h: keys for h, keys in list(duplicates.items())[:50]},
        "missing_service_icons": missing,
        "should_prefer_official": should_official,
        "network_need_project_icon": network_need,
        "backlog": {
            "P0_fix_identity": [x["service"] for x in parent_reuse],
            "P1_high_freq_color": [x["id"] for x in should_official],
            "P2_missing_services": missing[:80],
            "P3_network_project_icons": network_need,
            "P4_dedupe_review": list(duplicates.values())[:30],
            "P5_write_provenance": no_prov[:80],
        },
    }

    out = ROOT / "reports" / day
    out.mkdir(parents=True, exist_ok=True)
    (out / "icon_identity_audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["summary"], indent=2))
    print(f"[icon_identity_audit] → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
