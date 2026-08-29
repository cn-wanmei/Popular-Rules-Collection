# 客户端 Icon URL（独立资产，非规则文件）

图标与 7 Client 规则解耦。规则 Builder **不**嵌入图标。

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/256/{id}.png
```

| 尺寸 | 路径 |
|------|------|
| 64 / 128 / 256 | `assets/icons/png/{size}/{id}.png` |
| SVG | `assets/icons/source/{id}.svg` |
| Mono（可选） | `assets/icons/monochrome/{size}/{id}.png` |

## 渲染规则（V2）

1. SVG 已有 path fill（多色 Logo）→ **原样保留**
2. 无 fill / currentColor → 使用 `manifest.brand.color`（Simple Icons 主色）
3. Network / Policy → 项目几何色，不强制品牌
4. GitHub / Apple 等官方单色 → monochrome 合法

## 构建

```bash
python scripts/icon_governance_apply.py
python scripts/sync_service_icons.py
python scripts/build_icons.py --force
python scripts/build_icons.py --force --monochrome
python scripts/icon_validate.py
```

Surge / Loon / Egern 使用 `icon-url` 指向 Raw 或 jsDelivr；**不要**写入 `generated/*.list` 规则正文。
