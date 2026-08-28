# Popular-Rules-Collection

> **规则数据供应链 + 标准化中间库 + 多客户端构建系统**
> Rules Data Supply Chain · Universal Rule Database · Multi-format Build System

自动采集、标准化、智能去重、冲突检测、版本追踪，并向 **Mihomo / Clash Meta / sing-box / Surge / Shadowrocket / Quantumult X / Egern / Loon** 输出规则集。

## 我该怎么用？

1. 打开 **[使用指南 docs/USAGE.md](docs/USAGE.md)** — 选规则、订阅读、策略顺序  
2. 查 **[规则目录 docs/RULE_CATALOG.md](docs/RULE_CATALOG.md)** — 每条规则的说明与使用场景  
3. 单服务 Raw 链接见 **[docs/rules/](docs/rules/)**

### 30 秒示例（Mihomo）

```yaml
rule-providers:
  china:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/china.yaml"
    interval: 86400
  openai:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/openai.yaml"
    interval: 86400
rules:
  - RULE-SET,china,DIRECT
  - RULE-SET,openai,PROXY
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
```

| 场景 | 规则 ID | 建议 |
|------|---------|------|
| 国内直连 | `china` | DIRECT |
| ChatGPT | `openai` / `ai` | PROXY |
| YouTube | `youtube` | PROXY |
| 微信/支付宝 | `wechat` / `alipay` | DIRECT |
| 广告拦截 | `adblock-light` | REJECT |

## 架构

双轨数据供应链（Service Rules **与** Network Datasets 隔离）：

```
Service Sources (registry.yaml)
  → collect → normalize → database/services|domains|ips
  → build_×7 → generated/{mihomo,sing-box,...}

Dataset Sources (sources/datasets/*)
  → collect_datasets / collect_ip / collect_providers
  → database/{network,geosite,geoip,provider,asn,policies}
  → build_network_* / build_provider_* → generated/{network,geosite,geoip,provider}

Quality Gate → Coverage / HOT_MISSING / Client Capability Matrix → reports/
```

## 目录

| 路径 | 用途 |
|------|------|
| `rule/` | 人读浏览（Primary 生态路径） |
| `database/` | Schema 中间库（services + network） |
| `generated/` | 客户端可订阅产物 |
| `sources/` | registry · ip_registry · datasets · health |
| `docs/` | **USAGE · RULE_CATALOG · 架构与质检** |
| `docs/rules/` | 每服务说明 + Raw/CDN 链接 |
| `config/` | primary · capabilities · intentional |
| `reports/` | 覆盖率 / 质量 / 能力矩阵 |
| `tests/` | 契约测试 |

## 文档索引

| 文档 | 说明 |
|------|------|
| [docs/USAGE.md](docs/USAGE.md) | 订阅方式、策略顺序、China 说明 |
| [docs/RULE_CATALOG.md](docs/RULE_CATALOG.md) | **全部规则：说明 + 场景 + 建议策略** |
| [docs/NETWORK_DATASETS.md](docs/NETWORK_DATASETS.md) | GeoSite / GeoIP / Provider / LAN |
| [docs/PHASE4_CAPABILITY.md](docs/PHASE4_CAPABILITY.md) | 客户端能力矩阵 |
| [docs/PHASE3_QUALITY.md](docs/PHASE3_QUALITY.md) | Quality Gate |
| [docs/RELEASE_AND_QC.md](docs/RELEASE_AND_QC.md) | 发布与质检 |
| [docs/rules/README.md](docs/rules/README.md) | 单服务文档索引 |

## 快速开始（开发者）

```bash
pip install -r requirements.txt
python scripts/collect.py
python scripts/normalize.py          # 完整 China 不要加 --skip-large
python scripts/deduplicate.py
python scripts/build_mihomo.py
# … 其他 build_* / validate
```

## 订阅约定

- **Primary**: GitHub Raw  
- **Mirror**: jsDelivr / Fastly（仅加速，非权威）

```text
.../generated/<client>/<service_id>.yaml|list|json
```

## License

MIT
