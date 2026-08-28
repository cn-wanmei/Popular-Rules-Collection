# 一类服务覆盖审计（2026-08-28）

## 完整度判定

| 等级 | 含义 |
|------|------|
| **A** | 多源合并，日常分流足够 |
| **B** | 可用；上游本身偏薄 |
| **C** | 仅子集；请用父生态聚合 |

## 审计结果

| 服务 | domains | 等级 | 说明 |
|------|--------:|------|------|
| google | ~1094 | **A** | BM7+MCX+v2fly |
| youtube | ~182 | **A** | 含 Music 源 |
| apple | ~1821 | **A** | AppStore/Dev/FindMy/Media/Music/TV/iCloud 多源 |
| microsoft | ~884 | **A** | 多源 |
| azure | ~151 | **A** | MCX |
| tencent | ~678 | **A** | 生态聚合 |
| wechat | ~30 | **B/C** | 上游仅 BM7 薄列表；细粒度用 wechat，兜底用 tencent |
| alibaba | ~463 | **A** | |
| alipay | ~21 | **B** | 上游薄；兜底 alibaba |
| amap | ~16 | **B** | 上游薄 |
| baidu | ~324 | **A** | |
| huawei | **~402** | **A** | 补 MCX+v2fly 后 160→402 |
| xiaomi | ~148 | **A** | |
| bytedance | ~1074 | **A** | |
| douyin | **~78** | **B** | 补 MCX 后 13→78 |
| tiktok | ~53 | **B** | |
| amazon | ~256 | **A** | ≠ aws provider IP |
| aws | ~77 | **B** | 域名；IP 在 provider |
| cloudflare | ~76 | **B** | 域名；IP 在 provider |
| github | ~68 | **B** | 上游规模上限 |
| facebook | ~549 | **A** | |
| openai | ~40 | **B** | 上游规模上限 |
| claude/anthropic | ~8–9 | **B** | 上游规模上限 |
| netflix | ~32 | **B** | 上游规模上限 |
| ai 聚合 | **~224** | **A** | category-ai + AI Suite |

## 不猜域名

npm / PyPI / Maven / Mistral / GCP / Supabase — 仍 NO_UPSTREAM。

## 使用建议

- 需要「微信一定直连」：`wechat` + `tencent` 都挂 DIRECT 更稳。
- Apple 全家桶：只订 `apple` 即可覆盖 Store/Music/iCloud/Find My 等。
- AI 全家桶：订 `ai` 或分别订 openai/claude/gemini。
