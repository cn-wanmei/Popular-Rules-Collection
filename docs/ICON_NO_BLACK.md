# No pure-black brand icons

仓库策略：**不允许纯黑品牌图标**。

| 原官方黑 | 流行色 |
|----------|--------|
| Apple | `#86868B` 灰 |
| GitHub | `#6E5494` 紫 |
| X / Twitter | `#1D9BF0` 蓝 |
| Notion | `#E1622F` 橙 |
| Vercel | `#0070F3` 蓝 |
| Steam | `#66C0F4` 浅蓝 |
| TikTok / Douyin | `#FE2C55` 粉红 |
| Uber | `#276EF1` 蓝 |

```bash
python scripts/icon_no_black.py
python scripts/build_icons.py --force
```

多色 Logo（Google/Microsoft）保持原色。
