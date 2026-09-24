# PRC Icon Library V4 — Style Guide

当前体系：**9 种主流开放图标设计语言的本地风格适配层 + 1 个品牌原生 / 官方优先层**。本次视觉修订重点不是简单换线宽，而是重新建立统一的「规则服务」图形语法：**外框 / 容器 + 服务结构 + 路由节点 + 留白**。

## 10 种风格

| 层 | 风格 | 新视觉方向 | 核心识别点 |
|---|---|---|---|
| Official | Brand Native | 保留品牌原生身份 | 真实品牌 Logo，不二次仿制 |
| 1 | Lucide | refined-outline | 大留白、圆角容器、轻量连接节点 |
| 2 | Tabler | precision-outline | 网格化结构、细线、双层信息 |
| 3 | Phosphor | bold-geometric | 六边 / 几何容器、粗轮廓、实心节点 |
| 4 | Material Symbols | rounded-filled | 块面、圆角、强弱层级、双节点 |
| 5 | Fluent | layered-soft | 前后叠层、柔和圆角、企业 UI 感 |
| 6 | Heroicons | shield-outline | Shield / 安全边界 / 中心路由节点 |
| 7 | Remix | stacked-linefill | line + fill、层叠数据块 |
| 8 | Bootstrap | balanced-outline | 圆形容器、稳定比例、小尺寸清晰 |
| 9 | Solar | radial-accent | 中心焦点、轨道、放射连接 |

## 本次优化解决的问题

旧 V4 的主要问题是：**每个风格只有一个过于简单的通用图形，虽然完成了 100% 覆盖，但视觉信息量不足，实际观感不如 V3 品牌图标。**

因此本次不再追求“像某个图标库”，而改为：

1. **保留 V3 品牌图标的优先级**：可信品牌身份仍然直接使用 V3 已发布品牌资产。
2. **九风格统一设计语言**：每个 fallback 都拥有明确的几何骨架，而不是简单的方框 + 三条线。
3. **小尺寸优先**：64×64 SVG 在 16 / 20 / 24 / 32 px 下仍保留主轮廓和识别节点。
4. **禁止假品牌**：fallback 只表达“服务 / 规则 / 路由”的语义，不冒充官方 Logo。
5. **统一视觉重量**：不同风格可以有不同性格，但都遵循相近的视觉占比、边距和中心重心。
6. **避免装饰过度**：不加入会干扰规则目录检索的复杂纹理和文字。

## 当前覆盖

Rule Index：262 条。
当前 V4：262 / 262 图标可解析。
可信品牌图精确复用 V3：85。
可信品牌图安全继承基础服务：49。
九风格本地 semantic fallback：128。

## SSOT

- `assets/icons/v4/release-pointer.json`
- `assets/icons/v4/manifest.json`
- `assets/icons/v4/service-index.json`
- `assets/icons/v4/styles/<style>/service.svg`

## 资产原则

九种风格均为**本仓库自有 semantic glyph**。Lucide、Tabler、Phosphor、Material Symbols、Fluent、Heroicons、Remix、Bootstrap、Solar 只作为设计语言参考；不把第三方原始 SVG 冒充为本仓库资产。

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
