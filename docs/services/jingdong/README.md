<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg" alt="JingDong 图标" width="72" height="72">

# JingDong — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `jingdong_aggregate` |
| 类型 | provider_aggregate |
| Provider | `jingdong` |
| 语义规则数量 | **277** |
| 语义 SHA-256 | `6d9b43bd56eb6ffcf5a3cc2681e1072a70abe56220f9126b70f2a1c2586cfc44` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**lucide semantic fallback**

- Style：`lucide`
- Identity：`semantic.fallback.lucide`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/lucide/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/jingdong/jingdong.yaml` | 277 | 5640 | `ac13485133ee11b41e3ad1721a7c7d43e469bf10c0c35b36d320e74ab2682ba4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/jingdong/jingdong.yaml) |
| loon | `loon/jingdong/jingdong.list` | 277 | 7837 | `38b444e3b7cf52c5f9cbf35cdf4ed544f90848aa55ff5ddb10d4407868cc304f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/jingdong/jingdong.list) |
| mihomo | `mihomo/jingdong/jingdong.yaml` | 277 | 8954 | `ec2330d9e4dcc4effb7bd19df13b04aa7cd0b6a4bb824339ea297c7ce82e53db` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/jingdong/jingdong.yaml) |
| quantumultx | `quantumultx/jingdong/jingdong.list` | 277 | 9499 | `b135dba642ab2901bb608e7b8bf9e01147d01ffe044587745b426333b0b2ff6f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/jingdong/jingdong.list) |
| shadowrocket | `shadowrocket/jingdong/jingdong.list` | 277 | 7837 | `38b444e3b7cf52c5f9cbf35cdf4ed544f90848aa55ff5ddb10d4407868cc304f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/jingdong/jingdong.list) |
| singbox | `singbox/jingdong/jingdong.json` | 0 | 7087 | `bcd4e58349dc46d91b037d1d1f0f7e701216ae6b263f13f45a781881a0516fff` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/jingdong/jingdong.json) |
| surge | `surge/jingdong/jingdong.list` | 277 | 7837 | `38b444e3b7cf52c5f9cbf35cdf4ed544f90848aa55ff5ddb10d4407868cc304f` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/jingdong/jingdong.list) |

## 4. 使用方法

选择客户端 → 复制对应 Raw → 加入客户端远程 Rule Set / Rule Provider / rule-set → 再绑定自己的 DIRECT / PROXY / REJECT 等策略。

不要跨客户端复用另一种格式的规则文件，也不要把 `rule/` 浏览树直接作为客户端运行时输入。

## 5. 服务集与独立子服务

服务集用于较宽覆盖；独立子服务用于精确分流。父级与子级同时存在时，实际命中关系由客户端规则顺序决定。

## 6. 图标来源与安全规则

真实品牌图标优先；缺失品牌身份时只使用 semantic fallback。禁止把风格化 fallback 冒充品牌官方 Logo，禁止用 favicon 作为永久主图标。

## 7. 完整性检查

| 项目 | SSOT |
|---|---|
| 服务 ID / 语义规则数 / SHA-256 | `rule/_index.yaml` |
| 客户端文件 / rule_count / size / SHA-256 | `generated/manifest.json` |
| 图标主层 / fallback | `assets/icons/v4/service-index.json` |
| 当前图标 Release | `assets/icons/v4/release-pointer.json` |

本页属于派生文档，不要手工维护发行数字、Raw、SHA 或图标地址。

## 8. 相关入口

- [服务总目录](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SERVICE_CATALOG.md)
- [V4 图标库说明](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/assets/icons/v4/README.md)
- [完整使用说明](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/RULE_USAGE_GUIDE.md)
- [Icon Usage](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/ICON_USAGE.md)

[回到顶部](#top)