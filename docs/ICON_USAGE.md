# 图标使用说明 — Current V4

assets/icons/v4/release-pointer.json 是当前服务图标体系入口，指向 V4 10 层 Icon Matrix。

## 当前 10 层

1. Official / Brand Native
2. Lucide
3. Tabler Icons
4. Phosphor
5. Material Symbols
6. Fluent UI System Icons
7. Heroicons
8. Remix Icon
9. Bootstrap Icons
10. Solar Icons

## 服务图标解析

Service ID → assets/icons/v4/service-index.json → primary layer → asset URL。

## 安全边界

- 有可信品牌身份：优先使用品牌原生 / 已验证图标。
- 无可信品牌身份：使用九风格 semantic fallback。
- 不把 fallback 标记为官方 Logo。
- 不用 favicon 作为永久主图标。
- strategy / network / dataset 不冒充品牌身份。

详见 ICON_STYLE_GUIDE_V4.md 与 assets/icons/v4/README.md。
