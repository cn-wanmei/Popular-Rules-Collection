#!/usr/bin/env python3
"""collect.py — V1.1 registry-driven collector with Fetcher abstraction, SHA256, manifest, empty protection, health.yaml"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fetchers import get_fetcher  # noqa: E402

REGISTRY_PATH = ROOT / "sources" / "registry.yaml"
HEALTH_PATH = ROOT / "sources" / "health.yaml"
BACKUP_ROOT = ROOT / "backup"

SOURCE_FILES: dict[str, list[dict[str, str]]] = {
    "blackmatrix7": [
        {"path": "rule/Clash/Apple/Apple.yaml", "name": "Clash_Apple.yaml"},
        {"path": "rule/Clash/Google/Google.yaml", "name": "Clash_Google.yaml"},
        {"path": "rule/Clash/Telegram/Telegram.yaml", "name": "Clash_Telegram.yaml"},
        {"path": "rule/Clash/Netflix/Netflix.yaml", "name": "Clash_Netflix.yaml"},
        {"path": "rule/Clash/GitHub/GitHub.yaml", "name": "Clash_GitHub.yaml"},
        {"path": "rule/Clash/Microsoft/Microsoft.yaml", "name": "Clash_Microsoft.yaml"},
        {"path": "rule/Clash/Discord/Discord.yaml", "name": "Clash_Discord.yaml"},
        {"path": "rule/Clash/OpenAI/OpenAI.yaml", "name": "Clash_OpenAI.yaml"},
        {"path": "rule/Clash/YouTube/YouTube.yaml", "name": "Clash_YouTube.yaml"},
        {"path": "rule/Clash/BiliBili/BiliBili.yaml", "name": "Clash_BiliBili.yaml"},
        {"path": "rule/Clash/Steam/Steam.yaml", "name": "Clash_Steam.yaml"},
        {"path": "rule/Clash/TikTok/TikTok.yaml", "name": "Clash_TikTok.yaml"},
        {"path": "rule/Clash/Twitter/Twitter.yaml", "name": "Clash_Twitter.yaml"},
        {"path": "rule/Clash/Disney/Disney.yaml", "name": "Clash_Disney.yaml"},
        {"path": "rule/Clash/China/China.yaml", "name": "Clash_China.yaml"},
        {"path": "rule/Surge/Apple/Apple.list", "name": "Surge_Apple.list"},
        {"path": "rule/Surge/Google/Google.list", "name": "Surge_Google.list"},
    ],
    "loyalsoldier": [
        {"path": "reject.txt", "name": "reject.txt"},
        {"path": "icloud.txt", "name": "icloud.txt"},
        {"path": "apple.txt", "name": "apple.txt"},
        {"path": "google.txt", "name": "google.txt"},
        {"path": "proxy.txt", "name": "proxy.txt"},
        {"path": "direct.txt", "name": "direct.txt"},
        {"path": "private.txt", "name": "private.txt"},
        {"path": "gfw.txt", "name": "gfw.txt"},
        {"path": "greatfire.txt", "name": "greatfire.txt"},
        {"path": "tld-not-cn.txt", "name": "tld-not-cn.txt"},
        {"path": "telegramcidr.txt", "name": "telegramcidr.txt"},
        {"path": "cncidr.txt", "name": "cncidr.txt"},
        {"path": "lancidr.txt", "name": "lancidr.txt"},
        {"path": "applications.txt", "name": "applications.txt"},
    ],
    "anti-ad": [
        {"path": "anti-ad-domains.txt", "name": "anti-ad-domains.txt"},
        {"path": "anti-ad-surge.txt", "name": "anti-ad-surge.txt"},
        {"path": "anti-ad-clash.yaml", "name": "anti-ad-clash.yaml"},
    ],
    "hagezi": [
        {"path": "adblock/ultimate.txt", "name": "adblock-ultimate.txt"},
        {"path": "adblock/pro.txt", "name": "adblock-pro.txt"},
        {"path": "adblock/light.txt", "name": "adblock-light.txt"},
    ],
    "sukkaw": [
        {"path": "List/non_ip/apple_services.conf", "name": "non_ip_apple_services.conf"},
        {"path": "List/non_ip/microsoft.conf", "name": "non_ip_microsoft.conf"},
        {"path": "List/non_ip/ai.conf", "name": "non_ip_ai.conf"},
        {"path": "List/non_ip/global.conf", "name": "non_ip_global.conf"},
        {"path": "List/non_ip/reject.conf", "name": "non_ip_reject.conf"},
        {"path": "List/ip/telegram.conf", "name": "ip_telegram.conf"},
        {"path": "List/ip/china_ip.conf", "name": "ip_china.conf"},
        {"path": "List/domainset/reject.conf", "name": "domainset_reject.conf"},
    ],
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def today_str() -> str:
    return utc_now().strftime("%Y-%m-%d")


def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_health() -> dict[str, Any]:
    if HEALTH_PATH.exists():
        return yaml.safe_load(HEALTH_PATH.read_text(encoding="utf-8")) or {"sources": {}}
    return {"sources": {}}


def save_health(data: dict[str, Any]) -> None:
    data["updated_at"] = utc_now().isoformat()
    HEALTH_PATH.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )


def fetcher_cfg_for(src: dict[str, Any]) -> dict[str, Any]:
    explicit = src.get("fetch") or {}
    if explicit:
        return explicit
    defaults = {
        "blackmatrix7": {"type": "github_raw", "owner": "blackmatrix7", "repo": "ios_rule_script", "branch": "master"},
        "loyalsoldier": {"type": "github_raw", "owner": "Loyalsoldier", "repo": "clash-rules", "branch": "release"},
        "anti-ad": {"type": "github_raw", "owner": "privacy-protection-tools", "repo": "anti-AD", "branch": "master"},
        "hagezi": {"type": "github_raw", "owner": "hagezi", "repo": "dns-blocklists", "branch": "main"},
        "sukkaw": {"type": "cdn", "bases": ["https://ruleset.skk.moe", "https://ruleset-mirror.skk.moe"]},
    }
    return defaults.get(src["id"], {"type": "github_raw", "owner": "unknown", "repo": "unknown"})


def collect_source(src: dict[str, Any], day_dir: Path, health: dict[str, Any]) -> dict[str, Any]:
    sid = src["id"]
    entries = SOURCE_FILES.get(sid, [])
    out_dir = day_dir / "sources" / sid
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = fetcher_cfg_for(src)
    fetcher = get_fetcher(cfg)
    files_meta: list[dict[str, Any]] = []
    ok = fail = empty_blocked = 0
    for entry in entries:
        result = fetcher.fetch_one(entry)
        result.source_id = sid
        name = result.name
        local = out_dir / name
        if not result.ok or not result.content:
            files_meta.append({"name": name, "path": result.path, "url": result.url, "status": "failed", "error": result.error, "status_code": result.status_code})
            fail += 1
            print(f"  FAIL {sid}/{name}: {result.error}")
            continue
        if len(result.content.strip()) == 0:
            files_meta.append({"name": name, "path": result.path, "url": result.url, "status": "blocked_empty", "error": "empty body — refuse to write"})
            empty_blocked += 1
            fail += 1
            print(f"  BLOCK empty {sid}/{name}")
            continue
        local.write_bytes(result.content)
        files_meta.append({"name": name, "path": result.path, "url": result.url, "local": str(local.relative_to(day_dir)), "size": result.size, "sha256": result.sha256, "status": "ok"})
        ok += 1
        print(f"  OK   {sid}/{name} ({result.size} bytes, {(result.sha256 or '')[:12]}…)")
    hs = health.setdefault("sources", {}).setdefault(sid, {})
    hs["last_attempt"] = utc_now().isoformat()
    if ok > 0:
        hs["last_success"] = utc_now().isoformat()
        hs["failure_count"] = 0
        hs["status"] = "healthy" if fail == 0 else "degraded"
    else:
        hs["last_failure"] = utc_now().isoformat()
        hs["failure_count"] = int(hs.get("failure_count") or 0) + 1
        hs["status"] = "down"
        hs["reason"] = "all fetches failed"
    if fail and ok:
        hs["reason"] = f"{fail} file(s) failed"
    elif not fail:
        hs.pop("reason", None)
    hs["files_ok"] = ok
    hs["files_failed"] = fail
    hs["empty_blocked"] = empty_blocked
    return {"source": sid, "fetch": cfg.get("type"), "timestamp": utc_now().isoformat(), "files_ok": ok, "files_failed": fail, "empty_blocked": empty_blocked, "files": files_meta, "registry_priority": src.get("priority"), "registry_trust": src.get("trust")}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect upstream (V1.1)")
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--source", action="append")
    args = parser.parse_args()
    registry = load_registry()
    health = load_health()
    sources = [s for s in registry.get("sources", []) if s.get("enabled")]
    if args.source:
        sources = [s for s in sources if s["id"] in args.source]
    day_dir = BACKUP_ROOT / args.date
    (day_dir / "sources").mkdir(parents=True, exist_ok=True)
    manifests_dir = day_dir / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    print(f"[collect] date={args.date} sources={len(sources)}")
    summary = []
    for src in sources:
        print(f"[collect] → {src['id']} ({fetcher_cfg_for(src).get('type')})")
        man = collect_source(src, day_dir, health)
        summary.append(man)
        (manifests_dir / f"{src['id']}.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (manifests_dir / "_day.json").write_text(json.dumps({"date": args.date, "timestamp": utc_now().isoformat(), "sources": summary}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    save_health(health)
    total_ok = sum(s["files_ok"] for s in summary)
    total_fail = sum(s["files_failed"] for s in summary)
    print(f"[collect] done ok={total_ok} failed={total_fail}")
    print(f"[collect] health → {HEALTH_PATH.relative_to(ROOT)}")
    return 0 if total_ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
