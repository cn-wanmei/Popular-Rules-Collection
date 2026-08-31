# Icon P2 — Final Freeze 收尾（光学 / 对比度 / QA）

> 在 [ICON_FINAL_FREEZE.md](ICON_FINAL_FREEZE.md) 之后的 polish。**不换风格、不重绘品牌。**

## 范围

| ID | 项 | 状态 |
|----|----|------|
| P2.1 | Optical override 接入 `icon_engine` normalize scale | ✅ |
| P2.2 | Dark Surface 对比度审计 `icon_dark_contrast_audit.py` | ✅ |
| P2.3 | QA `level: fail` 生效（content_ratio / near_black） | ✅ |
| P2.4 | source_color / display_color 元数据闭环 | ✅ via `icon_no_black.py` |

## 冻结（禁止再动）

- 深色整体方向、几何策略标、语义色
- 64/128/256、source→normalized→png/rendered
- 品牌路径识别形态、Grid 容器方式

## 命令

```bash
python scripts/icon_no_black.py
python scripts/icon_engine.py --force
python scripts/icon_dark_contrast_audit.py
python scripts/icon_qa.py
python scripts/icon_contact_sheet.py
```

光学微调只改 `assets/icons/metadata/optical_overrides.yaml`，不要批量改 Logo。
