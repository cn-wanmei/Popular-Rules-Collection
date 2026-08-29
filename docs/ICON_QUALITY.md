# Icon Quality（产品质量阶段）

> 不改 Rule / Primary / Builder。图标进入 **Quality / Delivery**，不是重新设计架构。

## 现状结论

| 层 | 评价 |
|----|------|
| Icon Schema / manifest | 已有 SSOT |
| Simple Icons 批量 | 工程可用，**视觉偏单色** |
| Policy / Dataset 几何标 | 方向正确，保持 project |
| 真彩色品牌 | 需 P0 精选升级，禁止无脑扩 mono PNG |

## 来源优先级

```text
P0  官方色 / 项目维护的品牌色标（identification）
P1  高质量彩色第三方
P2  Simple Icons（monochrome third_party）
P3  placeholder
```

**不强制一切彩色**：Apple / GitHub 等官方常为单色 → `color_mode: monochrome` 合法。

## Manifest 字段（B）

```yaml
source:
  provider: project-brand | simple-icons | project
  provenance: official-colors | third_party | project
  verified: true|false
visual:
  style: brand | geometric
  color_mode: color | monochrome
  background: transparent
  variants: [color, monochrome]
```

## 阶段

| Phase | 内容 | 状态 |
|-------|------|------|
| A Audit | `reports/*/icon_audit.json` | 进行中 |
| B Schema | visual + provenance | 进行中 |
| C P0 彩色 | Google/Microsoft/YouTube/… | 首批已写入 |
| D 产品化 | Rule Page / CDN / regression | 部分（Rule Page 已挂图） |

## 命令

```bash
python scripts/sync_service_icons.py   # 仅补缺，不覆盖 project-brand
python scripts/build_icons.py --force  # 需 cairosvg
python scripts/icon_validate.py
```

`sync_service_icons` **不得覆盖** `provenance: official-colors` 的 SVG。
