# Actions 清单（三仓）

侧栏过长时：GitHub **Actions → All workflows** 仍会列出 *disabled* 项；日常以 **Active** 为准。

## Popular-Rules-Collection（生产主链）

| 工作流 | 用途 |
|--------|------|
| **Collect Upstream** | 上游采集 |
| **Build Client Rules** | 客户端构建 |
| **Publish Release Candidate** | 发布候选 |
| **Unit Tests** / **Engine v3** / **Validate** | 质量门禁 |
| **Directory Gate** / **P3 Audit Gates** | 结构与审计 |
| **Generated Status** | 状态页刷新 |
| **Source Auto Handoff** / **Post-Handoff Binding Sync** | Source 交接 |
| **Service Production Hard Gate** / **Service Completion Gate** | 服务晋级 |
| **Ecosystem Release Lock Refresh** | 跨仓锁 |
| **Ecosystem Status (Read Model)** | 只读生态状态 |
| **Notify Icon Identity Change** | 通知 Icon（需 `ICON_DISPATCH_TOKEN`） |
| **Retention** | 保留策略（默认 dry-run） |
| **Documentation Layer** | 文档层 |
| **Published Raw E2E** | 发布后 E2E |
| **Client GitHub Release Packages** | 人工打包 Release |
| **Rule Mapping Release** | 规则映射变更时 |
| **Source Canary** / **Source Upstream Gate** | PR 路径 Source 策略门禁 |

### 已禁用（不删文件语义 / 幽灵）

| 工作流 | 原因 |
|--------|------|
| Icon V5 One-Shot Acquisition | V6 已接替；文件已不在树中 |
| Recovery Drill | 周调度探活，减少噪声；需要时在 Actions 里 **Enable** |

## Popular-Rules-Source

| 工作流 | 用途 |
|--------|------|
| **CI** (validate) | 校验 |
| **Generate Official Sources** | 生成官方源 |
| **Durable Source Bridge** | 持久化桥 |
| **Release Gate** | 发布门 |
| **Reconcile with Collection** | 与 Collection 对账 |
| **Source Lifecycle Status** | README / lifecycle 刷新 |

### 已禁用

| 工作流 | 原因 |
|--------|------|
| P1 P2 Self-Built Wave | 过程波次结束；文件已不在树中 |
| Emergency Restore Canary State | 紧急一次性；避免误点；事故时 **Enable** 再 `workflow_dispatch` |

## Popular-Rules-Icon

| 工作流 | 用途 |
|--------|------|
| **PR CI (L0–L1)** | PR 门禁 |
| **Identity Freshness** | Collection 身份对齐 |
| **V6 Release Writer** | V6 发布写入 |
| **V6 Manifest Verification** | Manifest 校验 |
| **Icon Style GitHub Release Packages** | 样式包人工 Release |

### 已禁用

| 工作流 | 原因 |
|--------|------|
| Full Icon Production Repair | 一次性全量修复；仅人工 Enable + dispatch |

## 原则

1. **主链**（Collect → Build → Publish → Lock / Status）保持 Active。  
2. **一次性 / 紧急 / 已退役** → Disable，不删历史 run。  
3. 需要时：Actions → 该 workflow → `...` → Enable workflow。  
