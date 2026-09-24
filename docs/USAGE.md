# 使用指南

## 1. 从哪里找规则

优先进入 [SERVICE_CATALOG.md](SERVICE_CATALOG.md)。每个条目都能进入独立说明页，直接查看规则数、更新时间、七客户端 Raw、SHA-256 与图标。

## 2. 当前客户端目录

| 客户端 | 实际目录 | 典型格式 |
|---|---|---|
| Mihomo | `generated/mihomo/` | YAML |
| sing-box | `generated/singbox/` | JSON |
| Surge | `generated/surge/` | LIST |
| Shadowrocket | `generated/shadowrocket/` | LIST |
| Quantumult X | `generated/quantumultx/` | LIST |
| Egern | `generated/egern/` | YAML |
| Loon | `generated/loon/` | LIST |

## 3. Raw URL

最终路径以 `generated/manifest.json` 为准。服务页已经给出精确 Raw，因此不建议手工猜路径。

通用形式：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/<client>/<file>`

## 4. 使用流程

找到服务 → 打开服务页 → 选择客户端 → 复制 Raw → 加入远程 Rule Set / Rule Provider → 绑定自己的策略。

## 5. 边界

- `rule/` 是人类浏览 / 搜索 / 选择发行树，不是客户端运行时输入。
- `generated/<client>/` 是客户端消费入口。
- 不跨客户端复用 YAML / JSON / LIST。
- Provider / ASN / GeoIP / Geosite 等 Network Dataset 不等于 Service Identity。