"""Decision engine."""
from __future__ import annotations
from src.v3.core.models.decision import Decision

DIRECT_HINTS = {
    "china", "private", "lan", "alibaba", "tencent", "baidu", "bytedance",
    "jingdong", "meituan", "bilibili", "wechat", "qq", "zhihu", "weibo",
    "xiaohongshu", "douyin", "netease", "iqiyi", "youku", "kuaishou",
    "unionpay", "alipay", "chinamobile", "chinatelecom", "chinaunicom",
}

def decide_for_service(service_id: str, category: str = "") -> Decision:
    sid_l = (service_id or "").lower()
    cat = (category or "").lower()
    if cat == "adblock" or sid_l.startswith("adblock"):
        return Decision(action="REJECT", layer="service", precedence=900, reason="adblock")
    if cat in ("china", "domestic") or sid_l in DIRECT_HINTS or any(h in sid_l for h in DIRECT_HINTS):
        return Decision(action="DIRECT", layer="service", precedence=800, reason="domestic_hint")
    return Decision(action="PROXY", layer="service", precedence=800, reason="default_proxy")
