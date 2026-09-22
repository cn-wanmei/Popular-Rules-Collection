# Icons

**使用说明（SSOT）→ [docs/ICON_USAGE.md](../../docs/ICON_USAGE.md)**

| 交付 | 路径 |
|------|------|
| Legacy PNG | `png/{64,128,256}/{id}.png` |
| Legacy SVG | `source/{id}.svg` |
| Legacy 元数据 | `manifest.yaml` |
| Icon System 3 Registry | `v3/registry.yaml` |
| Icon System 3 Release | `v3/releases/latest/` |
| Icon System 3 客户端索引 | `v3/releases/latest/index/clients/` |
| Icon System 3 总预览 | `v3/releases/latest/previews/{style}/master-all.svg` |

## Icon System 3.0

新生产链为：

```text
Service Catalog
  ↓
Icon Identity
  ↓
Source / License / Provenance
  ↓
Role Binding
  ↓
Official / Gradient / Liquid Glass / Soft 3D / Minimal / Dark-Neon / Monochrome
  ↓
Visual + Identity + Client QA
  ↓
Master / Role / Legibility Review
  ↓
7 Client Index
  ↓
Immutable Release
```

V3 不直接覆盖 Legacy 图标目录。Legacy 资产继续作为 previous-good / rollback 基线，直到 V3 完成覆盖、审阅和稳定发布。

策略组、客户端策略组使用独立的 semantic Icon Identity；真实品牌图标使用 Service Identity。两者禁止通过文件名隐式复用。

旧版手工写入 main 的 Icon workflow 已退出生产写入路径；V3 workflow 在 PR 上执行 fail-closed QA，Release 使用受控 workflow 生成不可变版本。

### Legacy 本地命令

```bash
python scripts/icon_no_black.py
python scripts/build_icons.py --force
python scripts/icon_validate.py
python scripts/icon_cleanup_dirs.py
```
