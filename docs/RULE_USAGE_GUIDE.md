# Popular-Rules-Collection 规则完整使用说明

> 当前基线：2026-09-24 Release · Run `20260924T043120249584Z-run` · IR `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7`

## 1. 两个核心入口

- `rule/`：人类浏览、搜索、选择服务。
- `generated/<client>/`：具体客户端最终规则。

## 2. 服务 / 子服务 / 服务集

完整入口：[SERVICE_CATALOG.md](SERVICE_CATALOG.md)。当前规则索引有 **262** 条记录、**116** 个顶级服务集。每条记录都有独立说明页。

**服务集**：用于较宽覆盖面的统一引用。

**独立服务 / 子服务**：用于精确分流，直接使用独立 Raw，不要从聚合规则手工拆分。

## 3. 当前客户端

| 客户端 | 目录 |
|---|---|
| egern | `generated/egern/` |
| loon | `generated/loon/` |
| mihomo | `generated/mihomo/` |
| quantumultx | `generated/quantumultx/` |
| shadowrocket | `generated/shadowrocket/` |
| singbox | `generated/singbox/` |
| surge | `generated/surge/` |

## 4. Raw URL

目标地址统一来自 `generated/manifest.json`。通用形式：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/<client>/<file>`

## 5. 标准使用流程

服务目录 → 服务页 → 客户端 Raw → 远程 Rule Set / Rule Provider → 自己的策略。

## 6. 更新时间与校验

- Collection Date：`2026-09-24`
- Generated At：`2026-09-24T04:39:15.367236+00:00`
- Run：`20260924T043120249584Z-run`
- IR Digest：`f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7`
- Generated files：**1984**

服务页分别展示语义 rule_count 与客户端编译 rule_count；不要将二者混为一个统计值。

## 7. 图标

当前 Icon SSOT：`assets/icons/v3/release-pointer.json` → Icon System 3 Release → client index。服务页直接嵌入对应服务身份图标；没有独立身份时明确使用 placeholder。

## 8. 常见错误

- 把 `rule/` 当作客户端输入。
- 用某客户端目录给另一个客户端。
- 使用旧 `generated/sing-box/` 或 `generated/quantumult-x/` 路径。
- 手工修改 Raw URL / rule_count / SHA-256。
- 把 Provider / ASN / GeoIP / Geosite 当成 Service Identity。

## 9. 自动化消费

读取 `generated/manifest.json` → 过滤 `kind=client_rules` → 按客户端和精确 `file` 选择 → 使用 Raw URL 下载 → 用 sha256 做缓存/变化检测。