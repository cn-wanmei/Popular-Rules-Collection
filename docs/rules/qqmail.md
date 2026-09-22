# Qqmail

> Source 官方证据链进入 Collection V3 后的当前规则说明页。订阅路径直接取自 `generated/manifest.json`。

| 项目 | 内容 |
|------|------|
| Rule ID | `qqmail` |
| Primary Ecosystem | `tencent` |
| Source | Popular-Rules-Source immutable lineage |
| Release Date | 2026-09-22 |
| Rule Count | 1 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| mihomo | `mihomo/tencent/qqmail/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/tencent/qqmail/rules.yaml) |
| singbox | `singbox/tencent/qqmail/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/tencent/qqmail/rules.json) |
| surge | `surge/tencent/qqmail/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/tencent/qqmail/rules.list) |
| shadowrocket | `shadowrocket/tencent/qqmail/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/tencent/qqmail/rules.list) |
| quantumultx | `quantumultx/tencent/qqmail/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/tencent/qqmail/rules.list) |
| egern | `egern/tencent/qqmail/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/tencent/qqmail/rules.yaml) |
| loon | `loon/tencent/qqmail/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/tencent/qqmail/rules.list) |

## Source 边界

该服务的上游证据由 Popular-Rules-Source 提供；Collection 通过 immutable Source binding 消费。Candidate / lifecycle 状态不能绕过 Source Gate 直接晋级生产。

## 当前真源

V3 Canonical：`data/runs/<run-id>/canonical/`；Semantic IR：`data/runs/<run-id>/ir/`；最终交付：`generated/`。

---
_页面由当前生产 manifest 约束；不要引用历史 generated/sing-box、generated/quantumult-x 或 database/services 路径。_
