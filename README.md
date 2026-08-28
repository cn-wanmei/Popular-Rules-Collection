# Popular-Rules-Collection

> **规则数据供应链 + 标准化中间库 + 多客户端构建系统**
> Rules Data Supply Chain · Universal Rule Database · Multi-format Build System

自动采集、标准化、智能去重、冲突检测、版本追踪，并向 **Mihomo / Clash Meta / sing-box / Surge / Shadowrocket / Quantumult X / Egern** 输出规则集。

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

Quality Gate (dataset_diff + dataset_quality) → Hard/Warn
Coverage / HOT_MISSING / Client Capability Matrix → reports/
```

文档：`docs/PHASE3_QUALITY.md` · `docs/PHASE3BC.md` · `docs/PHASE4_CAPABILITY.md` · `docs/NETWORK_DATASETS.md`

## 目录

| 路径 | 用途 |
|------|------|
| `rule/` | 人读浏览 |
| `database/` | Schema 中间库（services + network datasets） |
| `generated/` | 客户端产物 + network/provider 导出 |
| `sources/` | registry · ip_registry · datasets/* · health |
| `scripts/` | 采集 / 标准化 / 构建 / Quality Gate / Matrix |
| `config/` | primary · client_capabilities · intentional_unmaterialized |
| `reports/` | coverage · quality · capability · HOT_MISSING |
| `tests/` | 关键路径契约测试 |

## 快速开始

```bash
pip install -r requirements.txt
python scripts/collect.py
python scripts/normalize.py --skip-large
python scripts/deduplicate.py
python scripts/build_mihomo.py
python scripts/build_surge.py
python scripts/build_singbox.py
python scripts/build_shadowrocket.py
python scripts/build_quantumultx.py
python scripts/build_egern.py
python scripts/validate.py
```

## 订阅约定

- **Primary**: GitHub Raw
- **Mirror**: jsDelivr / Fastly / Cloudflare（仅加速，非权威）

Example (Egern):

```yaml
rules:
  - rule_set:
      match: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/google.yaml"
      policy: Proxy
      update_interval: 86400
```

## License

MIT
