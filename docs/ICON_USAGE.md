# 图标使用说明 — Current V4

当前 Release：`2026.09.25-prc-icon-matrix-3`

`assets/icons/v4/release-pointer.json` 是当前图标体系入口，指向 V4 10 层 Icon Matrix。

## 当前 10 层

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

## 解析链

```text
Service ID / Rule Path
        ↓
assets/icons/v4/service-index.json
        ↓
primary layer
        ↓
asset URL
```

不要根据服务名猜测图标地址；以 `service-index.json` 的 `raw` 字段为准。

## 选择规则

### 有可信品牌身份

`Official → 已验证 V3 brand asset`

不对真实品牌 Logo 重新做九种 UI 风格仿制。

### 没有可信品牌身份

`9-style semantic fallback`

fallback 是「语义覆盖」，不是品牌认证。

## 安全边界

- 不把 fallback 标记为官方 Logo。
- 不把 favicon 当作永久主图标。
- strategy / network / dataset 不冒充品牌身份。
- 第三方参考库只定义视觉语言，不改变服务身份事实。
- V3 资产仍是品牌图标的 previous-good / compatibility source。

## 当前覆盖

当前 Rule Index 共 262 条，与 Icon Service Index 路径级一一对应，缺失 0、重复 0、额外 0；覆盖率 100%。

详见 `ICON_STYLE_GUIDE_V4.md` 与 `../assets/icons/v4/README.md`。
