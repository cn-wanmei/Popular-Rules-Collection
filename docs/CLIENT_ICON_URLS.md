> **完整说明见 [ICON_USAGE.md](ICON_USAGE.md)**（路径、流水线、硬约束）。

# 客户端 Icon URL（独立资产，非规则文件）

图标与 7 Client 规则解耦。规则 Builder **不**嵌入图标。

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/256/{id}.png
```

| 尺寸 | 路径 |
|------|------|
| 64 / 128 / 256 | `assets/icons/png/{size}/{id}.png` |
| SVG | `assets/icons/source/{id}.svg` |
| 主题渲染（可选） | `assets/icons/rendered/{transparent,light,dark}/{size}/{id}.png` |

## 渲染规则（V2）

1. SVG 已有 path fill（多色 Logo）→ **原样保留**
2. 无 fill / currentColor → 使用 `manifest.brand.color`（Simple Icons 主色）
3. Network / Policy → 项目几何色，不强制品牌
4. **禁止纯黑品牌图**（见 ICON_NO_BLACK.md）；原黑标已改为流行色

## 构建

```bash
python scripts/icon_policy_set.py
python scripts/icon_no_black.py
python scripts/build_icons.py --force
python scripts/icon_engine.py --force
python scripts/icon_cleanup_dirs.py
python scripts/icon_validate.py
```

Surge / Loon / Egern 等：按服务 id 拉取 `png/128/{id}.png` 即可。
