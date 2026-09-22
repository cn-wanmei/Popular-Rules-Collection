# Taobao

> Source 官方证据链进入 Collection V3 后的当前规则说明页。订阅路径直接取自 `generated/manifest.json`。

| 项目 | 内容 |
|------|------|
| Rule ID | `taobao` |
| Primary Ecosystem | `alibaba` |
| Source | Popular-Rules-Source immutable lineage |
| Release Date | 2026-09-22 |
| Rule Count | 14 |

## 当前生产订阅路径

| 客户端 | 路径 | Raw |
|--------|------|-----|
| mihomo | `mihomo/alibaba/taobao/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/mihomo/alibaba/taobao/rules.yaml) |
| singbox | `singbox/alibaba/taobao/rules.json` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/singbox/alibaba/taobao/rules.json) |
| surge | `surge/alibaba/taobao/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/surge/alibaba/taobao/rules.list) |
| shadowrocket | `shadowrocket/alibaba/taobao/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/shadowrocket/alibaba/taobao/rules.list) |
| quantumultx | `quantumultx/alibaba/taobao/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/quantumultx/alibaba/taobao/rules.list) |
| egern | `egern/alibaba/taobao/rules.yaml` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/egern/alibaba/taobao/rules.yaml) |
| loon | `loon/alibaba/taobao/rules.list` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/loon/alibaba/taobao/rules.list) |

## Source 边界

该服务的上游证据由 Popular-Rules-Source 提供；Collection 通过 immutable Source binding 消费。Candidate / lifecycle 状态不能绕过 Source Gate 直接晋级生产。

## 当前真源

V3 Canonical：`data/runs/<run-id>/canonical/`；Semantic IR：`data/runs/<run-id>/ir/`；最终交付：`generated/`。

---
_页面由当前生产 manifest 约束；不要引用历史 generated/sing-box、generated/quantumult-x 或 database/services 路径。_
