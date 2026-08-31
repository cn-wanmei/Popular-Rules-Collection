#!/usr/bin/env python3
"""P1.1 Universal Rule IR — export typed rules as stable JSONL."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
OUT = ROOT / "generated" / "ir"
DEC_META = ROOT / "generated" / "routing" / "decisions.meta.json"

DIRECT_HINTS = {
    "china", "private", "lan", "alibaba", "tencent", "baidu", "bytedance",
    "jingdong", "meituan", "bilibili", "wechat", "qq", "zhihu", "weibo",
    "xiaohongshu", "douyin", "netease", "iqiyi", "youku", "kuaishou",
    "unionpay", "alipay", "chinamobile", "chinatelecom", "chinaunicom",
}


def default_action(sid: str, cat: str) -> str:
    sid_l, cat = sid.lower(), (cat or "").lower()
    if cat == "adblock" or sid_l.startswith("adblock"):
        return "REJECT"
    if cat in ("china", "domestic") or sid_l in DIRECT_HINTS or any(h in sid_l for h in DIRECT_HINTS):
        return "DIRECT"
    return "PROXY"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "rules.jsonl"
    n = 0
    by_type: dict[str, int] = {}
    digest = hashlib.sha256()
    with path.open("w", encoding="utf-8") as f:
        for p in sorted(SERVICES.glob("*.yaml")):
            if p.name.startswith("example"):
                continue
            try:
                doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            sid = doc.get("id") or p.stem
            cat = doc.get("category") or "other"
            action = default_action(sid, str(cat))
            for r in doc.get("rules") or []:
                if not isinstance(r, dict):
                    continue
                typ, val = r.get("type"), r.get("value")
                if not typ or not val:
                    continue
                rec = {
                    "service": sid,
                    "match": {"type": str(typ), "value": str(val)},
                    "classification": {"category": cat},
                    "decision": {"layer": "service", "action": action, "precedence": 800},
                    "provenance": {"sources": r.get("sources") or doc.get("source") or []},
                }
                line = json.dumps(rec, ensure_ascii=False)
                f.write(line + "\n")
                digest.update(line.encode())
                n += 1
                by_type[str(typ)] = by_type.get(str(typ), 0) + 1
    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rules": n,
        "by_type": by_type,
        "ir_digest": digest.hexdigest(),
        "decision_digest": None,
    }
    if DEC_META.exists():
        try:
            meta["decision_digest"] = json.loads(DEC_META.read_text()).get("decision_digest")
        except Exception:
            pass
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"[universal_ir] rules={n} types={by_type} digest={meta['ir_digest'][:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
