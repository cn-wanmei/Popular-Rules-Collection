<a id="top"></a>

<img src="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg" alt="Baidu Netdisk 图标" width="72" height="72">

# Baidu Netdisk — 分流规则说明

> 当前 Release 服务说明页。图标使用 PRC Icon Library V4；规则数据继续以当前 Rule / Generated SSOT 为准。

## 1. 服务信息

| 项目 | 当前值 |
|---|---|
| Service ID | `baidunetdisk` |
| 类型 | service |
| Provider | `baidu` |
| 语义规则数量 | **2** |
| 语义 SHA-256 | `5350d45b0dc4eebcd8a803654fa57f389145f793411e96410aab2f21d1d90367` |
| Collection Date | `2026-09-24` |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |

## 2. 图标适配

主图标层：**solar semantic fallback**

- Style：`solar`
- Identity：`semantic.fallback.solar`
- Raw：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/solar/service.svg`
- 该图标用于覆盖缺失身份，不代表官方品牌 Logo。

9 种可选视觉语言：Lucide、Tabler、Phosphor、Material Symbols、Fluent UI、Heroicons、Remix、Bootstrap、Solar。

## 3. 七客户端 Raw

| 客户端 | 文件 | Manifest rule_count | size | SHA-256 | Raw |
|---|---|---:|---:|---|---|
| egern | `egern/baidu/baidunetdisk/baidunetdisk.yaml` | 2 | 67 | `ce7bcc18df9028413f290d16e0e937d7b2cb3126d20d651ac882a65b6bdb05e4` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/baidu/baidunetdisk/baidunetdisk.yaml) |
| loon | `loon/baidu/baidunetdisk/baidunetdisk.list` | 2 | 64 | `88bc62517ed3c058d30f3d0d92d818a9c4d614b0c8d02a9220f1614f3c25b271` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/baidu/baidunetdisk/baidunetdisk.list) |
| mihomo | `mihomo/baidu/baidunetdisk/baidunetdisk.yaml` | 2 | 81 | `13cf0d5a9ef674dc7314ee367ae8184beeca50775e9d1205bfb748771288e878` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/baidu/baidunetdisk/baidunetdisk.yaml) |
| quantumultx | `quantumultx/baidu/baidunetdisk/baidunetdisk.list` | 2 | 76 | `74827c58ff080f920060801334473bf5729aac3d8a90cfd3efe1769ef56f2ff0` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/baidu/baidunetdisk/baidunetdisk.list) |
| shadowrocket | `shadowrocket/baidu/baidunetdisk/baidunetdisk.list` | 2 | 64 | `88bc62517ed3c058d30f3d0d92d818a9c4d614b0c8d02a9220f1614f3c25b271` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/baidu/baidunetdisk/baidunetdisk.list) |
| singbox | `singbox/baidu/baidunetdisk/baidunetdisk.json` | 0 | 139 | `3df566deaf78e0964d4581701a81970be27a93d24ff794f3703bfdbf5d092f96` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/baidu/baidunetdisk/baidunetdisk.json) |
| surge | `surge/baidu/baidunetdisk/baidunetdisk.list` | 2 | 64 | `88bc62517ed3c058d30f3d0d92d818a9c4d614b0c8d02a9220f1614f3c25b271` | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/baidu/baidunetdisk/baidunetdisk.list) |

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