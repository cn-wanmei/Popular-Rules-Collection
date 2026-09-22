# Popular-Rules-Collection

> 面向 Mihomo / sing-box / Surge / Shadowrocket / Quantumult X / Egern / Loon 的规则数据生产管线：Collect → Normalize → Canonical → IR → Client Adapters → Immutable Release。

## 生产真源与目录

当前 V3 生产链路只有一条权威路径：

`backup/<collection-date>` → V3 Engine → `data/runs/<run-id>` → Release Candidate → `generated/` → Publish。

| 路径 | 角色 | 是否为 V3 Runtime 输入 |
|---|---|---|
| `backup/<date>/` | 不可变 Collection 输入快照 | 是 |
| `data/runs/<run>/canonical/` | 本次运行的 Canonical 真源 | 是 |
| `data/runs/<run>/ir/` | Semantic IR | 是 |
| `generated/<client>/` | 七客户端最终编译分流规则集 | 否（运行输出） |
| `generated/network/` | LAN / Private / DNS / NTP / STUN 等 Network Dataset | 否（运行输出） |
| `generated/geosite/` | Geosite 分类数据 | 否（运行输出） |
| `generated/geoip/` | Country GeoIP CIDR 数据 | 否（运行输出） |
| `generated/provider/` | Provider CIDR 数据 | 否（运行输出） |
| `generated/asn/` | ASN / Provider 元数据 | 否（运行输出） |
| `generated/ip/` | 已审计的服务 IP 数据 | 否（运行输出） |
| `generated/policies/` | Network Policy 数据集 | 否（运行输出） |
| `generated/mmdb/` | MMDB / DAT 二进制发行物 | 否（运行输出） |
| `rule/` | **用户浏览 / 搜索 / 选择的可读发行树**，与本次 Run 的 `generated/` 同步生成 | 否（派生发行物） |
| `rules/` | **删除；不得重新建立第三套规则目录** | — |

`generated/manifest.json` 是整个最终发行树的单一文件级目录清单；`generated/network_manifest.json` 是 Network Dataset 的独立 provenance 清单。

## 完整生产链

```text
Official / External Upstream
          ↓
Collection DAG
          ↓
backup/<date>
          ↓
Immutable Source Lineage Gate
          ↓
V3 Snapshot
  → Ingest
  → Source Gate
  → Quarantine
  → Canonical
  → Hierarchy
  → Semantic IR
  → 7 Client Adapters
  → Determinism / Semantic / Directory Gates
          ↘
           Network Dataset Materialization
            → generated/network
            → generated/geosite
            → generated/geoip
            → generated/provider
            → generated/asn
            → generated/ip
            → generated/policies
            → generated/mmdb
          ↓
Release Candidate
          ↓
Immutable Publish
          ↓
generated/ + data/runs/ + baseline
```

Network Dataset 与 Service Rule 是不同语义层，但现在属于同一个 Release Candidate，不再通过旁路脚本决定“这次有没有生成”。

## Source Integration

Popular-Rules-Source 提供官方证据驱动的 Supplemental Source。Collection 对 Source 使用 immutable SHA 与 provenance v2 精确绑定：

```text
Source durable seal
      ↓
immutable_registry.yaml
      ↓
exact SHA + content/evidence/policy/generator/release digests
      ↓
Collection Source Gate
      ↓
V3 Build / Canary / Production
```

Source 的跨仓库自动交接由 Collection 自己持有，不依赖跨仓库 Secret。

## 最终发行入口

用户浏览、搜索、挑选规则使用 `rule/`；客户端订阅使用 `generated/<client>/...`；网络数据使用 `generated/<network-scope>/...`。三者都来自同一个 V3 Run，但只有 `data/runs/<run>/canonical` 是规则真源。

## CI / Release

所有主线发布都经过 Architecture、Lineage、V3、Semantic、Determinism、Directory、Evidence 与 Release Gate。Network Dataset 现在额外要求：

- 统一构建；
- 明确 provenance；
- 关键 scope 完整；
- `generated/manifest.json` 存在；
- Release Publish 前再次 fail-closed 校验。

## 文档

- `docs/PRODUCTION_RULE_CHAIN.md`
- `docs/GENERATED_OUTPUTS.md`
- `docs/NETWORK_DATASETS.md`
- `docs/ARCHITECTURE.md`
- `docs/IP_ARCHITECTURE.md`
- `rule/README.md

`PUBLISH_STATUS.md`、状态报告和 `reports/` 下的运行结果属于自动生成证据，不手工维护派生数字。
