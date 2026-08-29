# Icon Schema V2

## verified 拆分

| 维度 | 字段 |
|------|------|
| 身份 | `identity.verified` |
| 来源 | `source.verified` + `source.type` |
| 配色 | `brand.color_verified` |
| 视觉 | `visual.qa_passed` |
| 授权 | `license.reviewed` |

`status` 由系统计算，禁止手写冒充 verified。

## source.type

`official-source` | `official-guideline` | `simple-icons` | `project-redraw` | `project-generated` | `community` | `geometric`

project-redraw + 官方色 ≠ 官方文件。

## variants

```yaml
variants:
  brand: { status, color_mode, svg, png }
  mono:  { status, png }
  dark:  { maps_to: monochrome }  # optional
```

## status

```text
missing → sourced → identity-review → visual-review → verified
```

- simple-icons → **sourced**
- geometric / official-source → **verified**

```bash
python scripts/icon_schema_v2_migrate.py
python scripts/icon_validate.py
python scripts/icon_service_bidirectional.py
```
