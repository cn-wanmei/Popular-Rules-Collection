# Icons

**使用说明（SSOT）→ [docs/ICON_USAGE.md](../../docs/ICON_USAGE.md)**

| 交付 | 路径 |
|------|------|
| PNG | `png/{64,128,256}/{id}.png` |
| SVG | `source/{id}.svg` |
| 元数据 | `manifest.yaml` |

```bash
python scripts/icon_no_black.py
python scripts/build_icons.py --force
python scripts/icon_validate.py
python scripts/icon_cleanup_dirs.py
```

策略：无纯黑品牌图；策略组为几何全彩（direct / proxy / auto / …）。
