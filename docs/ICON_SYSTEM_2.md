# Icon System 2.0 — 品牌原图优先

## 原则

| 类型 | 规则 |
|------|------|
| Brand | 官方/SI 轮廓 + **品牌色渲染**；github/apple 等 `approved_mono` 可黑 |
| Policy / Dataset | 项目统一几何 |
| 禁止 | AI 造标、错误映射、假 verified、无意义全量 dark/light |

## 渲染（build_icons）

1. 多色 SVG → 原样  
2. 单色黑 SI + brand.color → 着色  
3. approved_mono → 官方黑  
4. monochrome/ 单色导出  

```bash
python scripts/build_icons.py --force
python scripts/icon_qa.py
```
