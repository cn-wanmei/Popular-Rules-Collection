# PRC Icon Engine

**官方身份 + 仓库统一视觉**。

```text
Source SVG → Normalize (512, ~82% safe) → Render
  transparent  (= assets/icons/png/{size}/ 客户端主路径)
  light tile / dark tile / monochrome
```

| mode | 用途 |
|------|------|
| brand_preserve | 保留品牌色；单色黑 SI 着色 |
| semantic | Policy/Dataset 几何 |

```bash
python scripts/icon_engine.py --force
python scripts/icon_contact_sheet.py
```

禁止：AI 造标、假 verified、打断旧 URL。
