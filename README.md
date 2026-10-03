# Popular Rules Collection

<p align="center">
  <img src="https://img.shields.io/badge/Clients-7-0d9488?style=for-the-badge" alt="7 clients" />
  <img src="https://img.shields.io/badge/SSOT-rule%2F_index.yaml-1e293b?style=for-the-badge" alt="SSOT" />
  <img src="https://img.shields.io/badge/Release-manual%20only-64748b?style=for-the-badge" alt="Manual release" />
  <img src="https://img.shields.io/badge/Icon-V6-6366f1?style=for-the-badge" alt="Icon V6" />
</p>

<p align="center">
  <strong>规则生产 · 服务目录 · 客户端发行</strong><br/>
  <sub>Canonical Identity · Multi-client Build · Publish · User Consumption</sub>
</p>

---

## 这是什么

**Popular Rules Collection** 是面向 **Mihomo / sing-box / Surge / Shadowrocket / Quantumult X / Egern / Loon** 的规则生产、服务目录与客户端发行仓库。

本仓库承担：

- Canonical Service Identity
- 规则归一化与构建
- 服务 / 子服务目录
- 客户端生成物
- Release Candidate / Publish
- 最终用户消费入口

| 权威项 | 入口 |
|--------|------|
| 服务身份唯一权威 | [`rule/_index.yaml`](rule/_index.yaml) |
| 动态发布状态唯一入口 | [`PUBLISH_STATUS.md`](PUBLISH_STATUS.md) |

> **README 不手写**服务数、规则数、Source Health、Coverage、Release 状态等权威统计。数字以 CI / SSOT 为准。

---

## 30 秒入口

| 你想… | 去这里 |
|-------|--------|
| 浏览服务规则 | [`rule/`](rule/) |
| 客户端直接使用 | [`generated/`](generated/) |
| 查服务目录 | [`docs/SERVICE_CATALOG.md`](docs/SERVICE_CATALOG.md) |
| 看服务独立说明 | [`docs/services/`](docs/services/) |
| 查看权威发布状态 | [`PUBLISH_STATUS.md`](PUBLISH_STATUS.md) |
| 查看 Source → Collection 漏斗 | [`docs/SOURCE_COLLECTION_FUNNEL.md`](docs/SOURCE_COLLECTION_FUNNEL.md) |
| 下载 GitHub Release 包 | [Releases](https://github.com/cn-wanmei/Popular-Rules-Collection/releases) |

---

## 权威与边界

| 内容 | 权威入口 | 说明 |
|------|----------|------|
| Canonical service identity | [`rule/_index.yaml`](rule/_index.yaml) | `service_id` / 服务目录身份 |
| Collection 发布状态 | [`PUBLISH_STATUS.md`](PUBLISH_STATUS.md) | CI 生成 |
| Source lifecycle | [`config/source_canary_state.yaml`](config/source_canary_state.yaml) | Source 侧状态，**不等同于** Collection Production |
| Immutable Source binding | [`sources/immutable_registry.yaml`](sources/immutable_registry.yaml) | Source → Collection 精确绑定 |
| Icon production | [Icon `config/release-pointers.yaml`](https://github.com/cn-wanmei/Popular-Rules-Icon/blob/main/config/release-pointers.yaml) | Icon V6 production / rollback |
| 客户端生成物 | [`generated/`](generated/) | 派生发行物 |

> **Source lifecycle ≠ Collection Production**  
> Source 负责证据与 Durable Seal；Collection 负责最终消费与 Production 发布。

---

## 生产链

```text
Upstream
   ↓
Source / Evidence
   ↓
Durable Release
   ↓
Immutable Seal
   ↓
Auto Handoff
   ↓
Collection Canary
   ↓
Production
   ↓
Collect / V3 Engine / Gates
   ↓
Release Candidate
   ↓
Publish
   ↓
generated/
```

### 状态语义

```text
REVIEW → VERIFIED → CANARY → PRODUCTION
                    ↘
                     BLOCKED
```

完整规则见 [`docs/SOURCE_COLLECTION_FUNNEL.md`](docs/SOURCE_COLLECTION_FUNNEL.md)。

---

## 当前状态

本节**不复制动态数字**；所有状态均以机器生成文件与 SSOT 为准。

| 状态域 | 权威入口 |
|--------|----------|
| Collection snapshot | [`PUBLISH_STATUS.md`](PUBLISH_STATUS.md) |
| Source health | [`PUBLISH_STATUS.md`](PUBLISH_STATUS.md) |
| Active Source bindings | [`sources/immutable_registry.yaml`](sources/immutable_registry.yaml) |
| Canonical services | [`rule/_index.yaml`](rule/_index.yaml) |
| Icon V6 pointer | [Icon `config/release-pointers.yaml`](https://github.com/cn-wanmei/Popular-Rules-Icon/blob/main/config/release-pointers.yaml) |
| 发布操作手册 | [`docs/RELEASE_RUNBOOK.md`](docs/RELEASE_RUNBOOK.md) |

---

## 客户端目录

| 客户端 | 路径 | 格式 |
|--------|------|------|
| Mihomo | `generated/mihomo/` | YAML |
| sing-box | `generated/singbox/` | JSON |
| Surge | `generated/surge/` | LIST |
| Shadowrocket | `generated/shadowrocket/` | LIST |
| Quantumult X | `generated/quantumultx/` | LIST |
| Egern | `generated/egern/` | YAML |
| Loon | `generated/loon/` | LIST |

---

## 目录边界

| 路径 | 职责 |
|------|------|
| `data/runs/` | Engine run / immutable production evidence |
| `rule/` | 人类浏览 / 搜索 / 选择 |
| `generated/<client>/` | 客户端规则 |
| `docs/services/` | 服务 / 子服务说明 |
| `docs/SERVICE_CATALOG.md` | 全量服务目录 |
| `sources/` | Source immutable binding / lineage |

`rule/` 与 `generated/` 都属于**派生发行层**。不要手工修补规则数量、SHA-256、Raw URL 或图标路径。

---

## Release

Collection 的 **Build / Publish** 与 **用户 GitHub Release** 分离：

| 阶段 | 作用 |
|------|------|
| Build Client Rules | 构建 immutable Release Candidate |
| Publish Release Candidate | 将验证通过的产物原子晋升到 `main` |
| Client GitHub Release Packages | 可选；仅在需要用户 zip 时 **手动** `workflow_dispatch` |

> Build / Publish 成功**不会**自动创建 GitHub Release。  
> 完整操作手册：[`docs/RELEASE_RUNBOOK.md`](docs/RELEASE_RUNBOOK.md)

---

## 文档

| 文档 | 用途 |
|------|------|
| [`docs/INDEX.md`](docs/INDEX.md) | 文档索引 |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | 架构说明 |
| [`docs/PRODUCTION_RULE_CHAIN.md`](docs/PRODUCTION_RULE_CHAIN.md) | 生产规则链 |
| [`docs/GENERATED_OUTPUTS.md`](docs/GENERATED_OUTPUTS.md) | Generated Outputs |
| [`docs/NETWORK_DATASETS.md`](docs/NETWORK_DATASETS.md) | Network Dataset |
| [`docs/SERVICE_CATALOG.md`](docs/SERVICE_CATALOG.md) | 服务目录 |
| [`docs/SOURCE_COLLECTION_FUNNEL.md`](docs/SOURCE_COLLECTION_FUNNEL.md) | Source → Collection 晋升漏斗 |
| [`docs/RELEASE_RUNBOOK.md`](docs/RELEASE_RUNBOOK.md) | 发布 Runbook |
| [`docs/RELEASE_NAMING.md`](docs/RELEASE_NAMING.md) | Release 命名 |
| [`docs/ACTIONS_SHA_PIN.md`](docs/ACTIONS_SHA_PIN.md) | Actions SHA 钉扎合同 |

---

## 关联项目仓库

| 仓库 | 关系 |
|------|------|
| [Popular-Rules-Source](https://github.com/cn-wanmei/Popular-Rules-Source) | 官方来源、Evidence、Snapshot、Durable Release、Immutable Seal |
| [Popular-Rules-Icon](https://github.com/cn-wanmei/Popular-Rules-Icon) | Icon V6 资产与生产指针 |

```text
Popular-Rules-Source
        │
        │ Durable Seal / Handoff
        ▼
Popular-Rules-Collection
        │
        │ Canonical Identity
        ▼
Popular-Rules-Icon
```

---

<sub>README 描述制度与入口；动态数字与覆盖率以各仓 SSOT / CI 生成为准。</sub>
