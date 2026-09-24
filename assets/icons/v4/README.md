# PRC Icon Library V4

当前 active matrix：**9 个主流开放图标设计语言 + 1 个品牌原生 / 官方优先层**。

## 10 层

1. Official / Brand Native
2. Lucide
3. Tabler Icons
4. Phosphor
5. Material Symbols
6. Fluent UI System Icons
7. Heroicons
8. Remix Icon
9. Hugeicons
10. Solar Icons

本次 V4 视觉重构不追求让 fallback “像某个第三方图标库”，而是分别吸收其视觉语法，再由仓库自有 semantic glyph 重新构建。这样能避免九个风格退化成同一个通用模板，也能保持品牌身份与 fallback 的边界。

## Active 风格

| 风格 | 视觉关键词 | 参考源 |
|---|---|---|
| Lucide | refined outline / browser container | https://lucide.dev/icons/ |
| Tabler | precision stack / small nodes | https://tabler.io/icons |
| Phosphor | bold geometric / solid focus | https://phosphoricons.com/ |
| Material Symbols | rounded filled / large mass | https://fonts.google.com/icons |
| Fluent | layered soft / enterprise UI | https://github.com/microsoft/fluentui-system-icons |
| Heroicons | secure outline / network center | https://heroicons.com/ |
| Remix | line + fill / stacked focus | https://remixicon.com/ |
| Hugeicons | bulk rounded / compact layers | https://hugeicons.com/icons |
| Solar | radial orbit / central focus | https://solar-icons.com/ |

Hugeicons 官方免费集合目前说明包含 6,000+ 免费图标，并提供 Stroke Rounded 等免费风格；本仓库仅把它作为视觉参考层，本地提交仍为自有 CC0 semantic glyph。citeturn670966search2

## 品牌图标原则

真实品牌图标优先保留，不使用九种 UI 风格重新发明品牌 Logo。没有可信品牌身份时使用 semantic fallback，仅用于视觉覆盖，不代表官方品牌标识。

## 当前覆盖

- Rule Index：262
- Icon Index：262
- 唯一 Icon Path：262
- 缺失：0
- 重复：0
- 多余：0
- Official / V3 brand asset：134
- 精确复用：85
- 安全继承：49
- 九风格 semantic fallback：128
- V4 Release：`2026.09.25-prc-icon-matrix-3`

## 文件

- `assets/icons/v4/release-pointer.json`
- `assets/icons/v4/manifest.json`
- `assets/icons/v4/service-index.json`
- `assets/icons/v4/styles/<style>/service.svg`

## 兼容说明

Bootstrap 不再属于 active matrix。旧 `assets/icons/v4/styles/bootstrap/service.svg` 暂保留，供历史 Raw URL 兼容，但当前 SSOT 不再引用。

## 资产原则

九种 active fallback 均为本仓库自有 CC0 semantic asset；参考库仅定义视觉语言，不直接复制第三方图标源码。
