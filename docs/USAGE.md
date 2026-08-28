# 使用指南（Usage）

本仓库产出的是 **规则数据**，不是完整代理客户端配置。你在 Mihomo / Surge / Quantumult X 等中引用规则集，并自行指定 DIRECT / PROXY / REJECT。

## 1. 选哪条规则？

| 你的目标 | 推荐 |
|----------|------|
| 国内 App / 网站走直连 | `china` + `geoip/cn` + `network/lan` |
| 只代理 Google | `google`、`youtube`、`googlefcm` |
| 常用 AI 一键代理 | `ai` 或 `openai`+`claude`+`gemini` |
| 刷 Netflix | `netflix`（节点需解锁） |
| 拦截广告 | `adblock-light`（轻）或 `adblock`（全） |
| 开发者 GitHub | `github`、`docker`、`cloudflare`（域名） |

完整场景表见 [RULE_CATALOG.md](./RULE_CATALOG.md)。

## 2. 订阅 URL 格式

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/<client>/<id>.<ext>
```

| 客户端 | 目录 | 常见扩展名 |
|--------|------|------------|
| Mihomo / Clash Meta | `generated/mihomo/` | `.yaml` / `.list` |
| sing-box | `generated/sing-box/` | `.json` |
| Surge | `generated/surge/` | `.list` |
| Shadowrocket | `generated/shadowrocket/` | `.list` |
| Quantumult X | `generated/quantumult-x/` | `.list` |
| Egern | `generated/egern/` | `.yaml` |
| Loon | `generated/loon/` | `.list` |

CDN 镜像（非权威）：jsDelivr `https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Collection@main/...`

## 3. 推荐规则顺序（逻辑）

```text
1. REJECT    ← adblock-light / adblock
2. DIRECT    ← lan / private / china / 国内银行支付
3. PROXY     ← google / ai / netflix / telegram …
4. GEOIP CN  ← DIRECT（IP 层兜底）
5. MATCH     ← 默认 PROXY 或 DIRECT（按你的策略）
```

**不要**把 `provider/aws` 的 IP 当成「亚马逊购物」；那是云厂商基础设施。

## 4. China 说明

- **域名**：`china` ← ChinaMax 级列表（约 11 万+），用于国内域名直连。
- **IP**：`database/ips/china.txt` / `geoip/cn` ← 国家地址段。
- 上游旧版 `China.yaml` 仅含少量 keyword，**已弃用**，仓库改为 `ChinaMax_Domain`。

## 5. 双轨数据

| 轨道 | 内容 | 目录 |
|------|------|------|
| Service Rules | 按产品/公司 | `generated/<client>/<service>` |
| Network Datasets | LAN、GeoSite、GeoIP、Provider | `generated/geosite|geoip|network|provider` |

## 6. 质量与更新

- 每日 Collect 流水线更新上游。
- `reports/` 含 coverage、quality、capability。
- 本地：`pip install -r requirements.txt` 后按 README 跑 collect → normalize → build。

## 7. 更多文档

| 文档 | 内容 |
|------|------|
| [RULE_CATALOG.md](./RULE_CATALOG.md) | 每条规则说明 + 场景 + 建议策略 |
| [NETWORK_DATASETS.md](./NETWORK_DATASETS.md) | 网络数据集架构 |
| [PHASE4_CAPABILITY.md](./PHASE4_CAPABILITY.md) | 客户端能力矩阵 |
| [RELEASE_AND_QC.md](./RELEASE_AND_QC.md) | 发布与质检 |
| `docs/rules/<id>.md` | 单服务 Raw 链接页 |
