# Icon System Final Freeze

**不换风格、不重绘品牌、不换整体方向。** 只闭环规则。

## 冻结范围

| 冻结 | 内容 |
|------|------|
| 方向 | Dark Surface 语境 + 几何策略标 |
| 尺寸 | 64 / 128 / 256 |
| 架构 | source → normalized → png / rendered |
| 策略语义色 | direct 绿 / proxy 蓝 / reject 红 等 |

## P0 已落地

1. **Source 与 Render 分离**  
   `icon_no_black.py` **不再改写** `source/*.svg`。  
   仅写 `brand.source_color` / `brand.display_color` / `brand.color_policy`。

2. **颜色字段**  
   - `source_color`：官方/SI 身份色  
   - `display_color`：交付色（Dark Surface / no-black）  
   - `color`：兼容字段，等于 `display_color`  
   - `color_policy`：`identity` | `lift-black` | `brand-accent`

3. **Monochrome 重定义**  
   单色 = **单一非黑品牌色（display_color）**，≠ 纯黑剪影。  
   `themes.yaml` / `profiles.yaml` 已更新。

4. **Render 修复**  
   `icon_engine` 在 normalize 后再次应用 tint，避免 nested SVG 丢 fill。

5. **QA**  
   `metadata/qa.yaml`：`near_black` / `content_ratio` 等核心项 **level: fail**。

6. **Optical overrides**  
   `metadata/optical_overrides.yaml`（人工 scale 表）。

## 使用路径

见 [ICON_USAGE.md](ICON_USAGE.md)。

## 禁止

- 再改整体网格风格 / 白底大换肤  
- 直接改 `source` 品牌路径为展示色  
- 恢复纯黑 PNG 交付  
