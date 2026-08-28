# 上游覆盖与日常使用标准

## 原则

1. **只物化有可信上游的服务**（BM7 / MetaCubeX / v2fly / Dler / 官方 IP 列表）。
2. **不猜测域名**；无上游写入 `config/intentional_unmaterialized.yaml`。
3. **生态聚合**：如 Apple = App Store + Music + ID + Maps + Find My + iCloud + Dev + Media… 多源合并到同一 service 或 Primary 子服务。

## 第一层：国内直连基础

| 能力 | 状态 | 路径 |
|------|------|------|
| China Domain | ✓ ChinaMax 级 | `china` / `database/domains/china.txt` |
| China CIDR | ✓ | `database/ips/china.txt` + `geoip/cn` |
| LAN | ✓ | `database/network/lan.txt` |
| Private | ✓ | service `private` |
| Carrier | ✓ | chinamobile / chinaunicom / chinatelecom |

## 第二层：海外核心（多源加强后）

| 生态 | 主要 ID | 上游 |
|------|---------|------|
| Apple 全系 | `apple` (+ `icloud`/`applemusic`/`appletv`) | BM7 子规则全量 + MetaCubeX apple* + v2fly |
| Google | `google` `youtube` `googlefcm` | BM7 + MetaCubeX + v2fly |
| Microsoft | `microsoft` `onedrive` `teams` `xbox` `azure` | BM7 + MetaCubeX + v2fly |
| Meta | `facebook` `instagram` `whatsapp` `messenger` `threads` | BM7 + MetaCubeX + v2fly |
| Amazon | `amazon` `aws` `primevideo` | 域名与 IP/Provider 分轨 |
| Cloudflare | `cloudflare` 域名 + `provider/cloudflare` IP | 分轨 |
| GitHub / AI / Streaming / Gaming / Social | 已 registry 覆盖 | 见 RULE_CATALOG |

## 第三层：网络基础设施

GeoIP / GeoSite / ASN / Provider / LAN / STUN — 见 `docs/NETWORK_DATASETS.md`。

## 明确 NO_UPSTREAM（不猜域名）

| 服务 | 说明 |
|------|------|
| npm / PyPI / Maven | 无独立可信规则源；可用 `developer` 聚合部分覆盖 |
| Mistral / GCP / Supabase | 暂无稳定专用列表 |
| Discovery+ | 无验证源 |

Roblox / Minecraft(Mojang)：v2fly / MetaCubeX 有源，可物化。

## 日常使用推荐最小集

```text
DIRECT:  china, lan, alipay, wechat, 银行
PROXY:   google, youtube, openai/ai, telegram, github, netflix
REJECT:  adblock-light
GEOIP:   CN → DIRECT
MATCH:   PROXY
```
