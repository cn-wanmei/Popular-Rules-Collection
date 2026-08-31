#!/usr/bin/env python3
"""Routing Decision SSOT emitter (P0) — memory-efficient.

SSOT: generated/routing/decisions.jsonl
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config" / "routing_contract.yaml"
OUT = ROOT / "generated" / "routing"
SERVICES = ROOT / "database" / "services"
GS_DIRECT = ROOT / "database" / "geosite" / "direct.txt"
GS_PROXY = ROOT / "database" / "geosite" / "proxy.txt"
OVERRIDES = ROOT / "database" / "policies" / "overrides"

DIRECT_HINTS = {
    "china", "private", "lan", "alibaba", "tencent", "baidu", "bytedance",
    "jingdong", "meituan", "bilibili", "wechat", "qq", "zhihu", "weibo",
    "xiaohongshu", "douyin", "netease", "iqiyi", "youku", "kuaishou",
    "unionpay", "alipay", "chinamobile", "chinatelecom", "chinaunicom",
    "12306", "ctrip", "pinduoduo", "xianyu", "eleme",
}


def load_layers():
    c = yaml.safe_load(CONTRACT.read_text(encoding="utf-8")) or {}
    layers = {x["id"]: int(x.get("precedence") or 0) for x in (c.get("layers") or []) if isinstance(x, dict)}
    terminal = (c.get("terminal") or {}).get("unmatched") or "PROXY"
    return layers, terminal, c


def norm_domain(s: str):
    s = (s or "").strip().lower()
    if not s or s.startswith("#"):
        return None
    if s.startswith("+."):
        s = s[2:]
    s = s.lstrip(".")
    if "/" in s or "*" in s:
        return None
    if not re.match(r"^[a-z0-9._-]+$", s):
        return None
    return s


def read_set(path: Path) -> set:
    if not path.exists():
        return set()
    out = set()
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            d = norm_domain(line)
            if d:
                out.add(d)
    return out


def resolve(hits, layers, terminal):
    if not hits:
        return terminal, "fallback", "unmatched", None
    for h in hits:
        if h[1] == "REJECT":
            return "REJECT", h[0], "reject_vs_other", h[2]
    hits = sorted(hits, key=lambda h: (-layers.get(h[0], -1), h[2]))
    top = hits[0]
    act = top[1] if top[1] in ("DIRECT", "PROXY", "REJECT") else terminal
    return act, top[0], "higher_precedence", top[2]


def main():
    layers, terminal, contract = load_layers()
    print("[routing_emit] loading geosite…")
    direct = read_set(GS_DIRECT)
    proxy = read_set(GS_PROXY)
    print(f"[routing_emit] geosite direct={len(direct)} proxy={len(proxy)}")

    extra = {}

    def add(domain, layer, action, id_):
        extra.setdefault(domain, []).append((layer, action, id_))

    print("[routing_emit] loading services…")
    n_svc = 0
    if SERVICES.exists():
        for p in SERVICES.glob("*.yaml"):
            sid = p.stem
            try:
                meta = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            if not isinstance(meta, dict):
                continue
            cat = str(meta.get("category") or "").lower()
            sid_l = sid.lower()
            if cat == "adblock" or sid_l.startswith("adblock"):
                continue  # reject-ad profile-optional (P1)
            if cat in ("china", "domestic") or sid_l in DIRECT_HINTS or any(h in sid_l for h in DIRECT_HINTS):
                act, layer = "DIRECT", "service"
            else:
                act, layer = "PROXY", "service"
            for rule in meta.get("rules") or []:
                if not isinstance(rule, dict):
                    continue
                if str(rule.get("type") or "").lower() not in ("domain", "domain_suffix"):
                    continue
                d = norm_domain(str(rule.get("value") or ""))
                if d:
                    add(d, layer, act, f"service:{sid}")
                    n_svc += 1
    print(f"[routing_emit] service domain hits={n_svc}")

    for name, action in (
        ("force_direct.yaml", "DIRECT"),
        ("force_proxy.yaml", "PROXY"),
        ("force_reject.yaml", "REJECT"),
    ):
        path = OVERRIDES / name
        if not path.exists():
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for e in doc.get("entries") or []:
            if not isinstance(e, dict):
                continue
            d = norm_domain(str((e.get("match") or {}).get("domain") or ""))
            if d:
                add(d, "explicit", action, f"override:{name}")

    OUT.mkdir(parents=True, exist_ok=True)
    jsonl = OUT / "decisions.jsonl"
    conflicts = []
    counts = {"DIRECT": 0, "PROXY": 0, "REJECT": 0}

    universe = direct | proxy | set(extra.keys())
    print(f"[routing_emit] universe={len(universe)} writing…")

    with jsonl.open("w", encoding="utf-8") as f, \
         (OUT / "direct.list").open("w", encoding="utf-8") as fd, \
         (OUT / "proxy.list").open("w", encoding="utf-8") as fp, \
         (OUT / "reject.list").open("w", encoding="utf-8") as fr:
        writers = {"DIRECT": fd, "PROXY": fp, "REJECT": fr}
        for domain in universe:
            hits = []
            if domain in direct:
                hits.append(("geosite", "DIRECT", "geosite-direct"))
            if domain in proxy:
                hits.append(("geosite", "PROXY", "geosite-proxy"))
            if domain in extra:
                hits.extend(extra[domain])
            seen = set()
            uniq = []
            for h in hits:
                if h in seen:
                    continue
                seen.add(h)
                uniq.append(h)
            act, layer, reason, source = resolve(uniq, layers, terminal)
            actions = {h[1] for h in uniq}
            matched_out = None
            if len(actions) > 1:
                matched_out = [{"layer": a, "action": b, "id": c} for a, b, c in uniq]
                if len(conflicts) < 5000:
                    conflicts.append({"domain": domain, "matched": matched_out, "action": act})
            rec = {
                "domain": domain,
                "action": act,
                "layer": layer,
                "reason": reason,
                "source": source,
            }
            if matched_out:
                rec["matched"] = matched_out
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            writers[act].write(domain + "\n")
            counts[act] = counts.get(act, 0) + 1

    digest = hashlib.sha256(jsonl.read_bytes()).hexdigest()
    meta = {
        "contract_version": contract.get("version"),
        "engine": "routing_emit-1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decision_digest": digest,
        "counts": {
            "domains": sum(counts.values()),
            "direct": counts.get("DIRECT", 0),
            "proxy": counts.get("PROXY", 0),
            "reject": counts.get("REJECT", 0),
            "conflicts": len(conflicts),
        },
        "ssot": "generated/routing/decisions.jsonl",
        "derivatives": ["direct.list", "proxy.list", "reject.list", "conflicts.json"],
        "semantic_uniqueness": True,
    }
    (OUT / "decisions.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "conflicts.json").write_text(
        json.dumps({"count": len(conflicts), "items": conflicts}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"[routing_emit] domains={meta['counts']['domains']} direct={meta['counts']['direct']} "
        f"proxy={meta['counts']['proxy']} reject={meta['counts']['reject']} "
        f"conflicts={meta['counts']['conflicts']} digest={digest[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
