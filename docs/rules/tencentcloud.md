# Tencentcloud

> Source 官方证据链进入 Collection V3 后的当前规则说明页。订阅路径直接取自 `generated/manifest.json`。

| 项目 | 内容 |
|------|------|
| Rule ID | `tencentcloud` |
| Primary Ecosystem | `tencent` |
| Source | Popular-Rules-Source immutable lineage |
| Release Date | 2026-09-22 |
| Rule Count | 1 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| mihomo | `mihomo/tencent/tencentcloud/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/tencent/tencentcloud/rules.yaml) |
| singbox | `singbox/tencent/tencentcloud/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/tencent/tencentcloud/rules.json) |
| surge | `surge/tencent/tencentcloud/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/tencent/tencentcloud/rules.list) |
| shadowrocket | `shadowrocket/tencent/tencentcloud/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/tencent/tencentcloud/rules.list) |
| quantumultx | `quantumultx/tencent/tencentcloud/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/tencent/tencentcloud/rules.list) |
| egern | `egern/tencent/tencentcloud/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/tencent/tencentcloud/rules.yaml) |
| loon | `loon/tencent/tencentcloud/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/tencent/tencentcloud/rules.list) |

## Source 边界

该服务的上游证据由 Popular-Rules-Source 提供；Collection 通过 immutable Source binding 消费。Candidate / lifecycle 状态不能绕过 Source Gate 直接晋级生产。

## 当前真源

V3 Canonical：`data/runs/<run-id>/canonical/`；Semantic IR：`data/runs/<run-id>/ir/`；最终交付：`generated/`。

---
_页面由当前生产 manifest 约束；不要引用历史 generated/sing-box、generated/quantumult-x 或 database/services 路径。_
