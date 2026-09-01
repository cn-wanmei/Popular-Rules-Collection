# Popular-Rules-Collection

> **规则数据供应链 + 标准化中间库 + 多客户端构建系统**
> Rules Data Supply Chain · Universal Rule Database · Multi-format Build System

自动采集、标准化、智能去重、冲突检测、版本追踪，并向 **Mihomo / Clash Meta / sing-box / Surge / Shadowrocket / Quantumult X / Egern / Loon** 输出规则集。

## 我该怎么用？

1. 打开 **[使用指南 docs/USAGE.md](docs/USAGE.md)** — 选规则、订阅读、策略顺序
2. 查 **[规则目录 docs/RULE_CATALOG.md](docs/RULE_CATALOG.md)** — 每条规则的说明与使用场景
3. 单服务 Raw 链接见 **[docs/rules/](docs/rules/)**

## 架构

Service Rules 与 Network Datasets 隔离。Service Rules 的生产构建统一由 V3 Engine 执行：

```text
Upstream / Source Registry
  → collect（只负责抓取）
  → immutable snapshot
  → ingest → quarantine → canonical
  → hierarchy / decision → IR
  → adapters ×7 → diff → golden → release
  → atomic promotion → generated/

Network Dataset Sources
  → collect_datasets / collect_ip / collect_providers
  → database/{network,geosite,geoip,provider,asn,policies}
  → dataset validation → generated/{network,geosite,geoip,provider}
```

## 目录

| 路径 | 用途 |
|------|------|
| `rule/` | 人读浏览（Primary 生态路径） |
| `database/` | Network Dataset 中间库；不是 V3 Service Rule Runtime 输入 |
| `generated/` | 客户端可订阅产物 |
| `sources/` | registry · ip_registry · datasets · health |
| `data/runs/` | V3 immutable run 与发布证据 |
| `docs/` | USAGE · RULE_CATALOG · 架构与质检 |
| `config/` | pipeline · capabilities · intentional |
| `reports/` | 覆盖率 / 质量 / 能力矩阵 |
| `tests/` | 契约与回归测试 |

## 快速开始（开发者）

```bash
pip install -r requirements.txt

# 仅抓取上游
python scripts/collect.py

# V3：从当天 collected snapshot 构建一整次 immutable run
DAY=$(date -u +%Y-%m-%d)
PYTHONPATH=. python -m src.engine.cli all --sources "backup/${DAY}" --data data

# 查看当前 Engine 版本
PYTHONPATH=. python -m src.engine.cli --version

# 对一个已经通过 release gate 的 run 做发布
PYTHONPATH=. python -m src.engine.cli promote --run-id <run_id>
```

`python scripts/normalize.py`、`python scripts/deduplicate.py` 与 `scripts/build_*.py` 已退出生产链，仅作为迁移阶段遗留工具保留。

## 订阅约定

- **Primary**: GitHub Raw
- **Mirror**: jsDelivr / Fastly（仅加速，非权威）

```text
.../generated/<client>/<service_id>.yaml|list|json
```

## License

MIT
