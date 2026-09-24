# PRC Icon Library V4 — Style Guide

当前体系：9 种主流开放图标设计语言的**本地风格适配层** + 1 个品牌原生 / 官方优先层。公开的 2026 图标生态资料持续将其中多套列为主流集合。

## 10 种风格

| 层 | 风格 | 视觉方向 | License | 适合场景 |
|---|---|---|---|---|
| Official | Brand Native | 保留品牌原生身份 | 按来源 | 品牌服务首选 |
| 1 | Lucide | 轻量 outline | ISC | 主界面、信息密集目录 |
| 2 | Tabler | 清晰 outline / filled | MIT | Dashboard、服务目录 |
| 3 | Phosphor | 多字重 | MIT | 层级、状态、强调 |
| 4 | Material Symbols | outlined / rounded / sharp | Apache-2.0 | 通用 UI |
| 5 | Fluent | regular / filled | MIT | 企业化、管理面板 |
| 6 | Heroicons | outline / solid | MIT | 现代 Web UI |
| 7 | Remix | line / fill | Apache-2.0 | 服务 / 状态双态 |
| 8 | Bootstrap | outline / fill | MIT | 高兼容 UI |
| 9 | Solar | multi-weight | CC-BY-4.0 | 特色主题、强调图形 |

## 核心原则

真实品牌图标优先保留。九种风格只作为 UI / semantic fallback 视觉层，不把品牌 Logo 仿造成另一套库的 Logo。

当规则服务没有可信品牌图标时，系统从九种设计语言中确定性选择一个**本仓库自有 semantic glyph**，从而保证 100% 图标覆盖。

## 当前覆盖

Rule Index：262 条。
当前 V4：262 / 262 图标可解析。
可信品牌图精确复用 V3：85。
可信品牌图安全继承基础服务：49。
九风格本地 semantic fallback：128。

## SSOT

- assets/icons/v4/release-pointer.json
- assets/icons/v4/manifest.json
- assets/icons/v4/service-index.json
- assets/icons/v4/styles/<style>/service.svg

## 参考源

- Lucide：https://lucide.dev/icons/
- Tabler：https://tabler.io/icons
- Phosphor：https://phosphoricons.com/
- Material Symbols：https://fonts.google.com/icons
- Fluent UI：https://github.com/microsoft/fluentui-system-icons
- Heroicons：https://heroicons.com/
- Remix：https://remixicon.com/
- Bootstrap：https://icons.getbootstrap.com/
- Solar：https://solar-icons.com/
