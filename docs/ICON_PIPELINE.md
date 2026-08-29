# Icon Asset Pipeline（与规划对齐 · 已锁）

> **暂不盲目补图。** 管线定型后再批量替换。

## 定型链路

```text
Service Registry (explicit icon_id)
        ↓
Icon Registry (variant roles)
        ↓
Source Priority P0→P4 (metadata/source_priority.yaml)
        ↓
Normalize (path fills kept; SI mono → brand.color)
        ↓
Variants: brand | simple | mono | network | placeholder
        ↓
PNG 64/128/256 (+ optional monochrome/)
        ↓
Icon QA (validate + identity + visual)
        ↓
Client Adapter (URL map only — never inside rule lists)
```

## 与提案对照

| 提案 | 仓库现状 |
|------|----------|
| 禁止生成器猜 Logo | ✅ service_icon_map 显式 |
| Source 分级 | ✅ source_priority.yaml + provenance |
| 黑色单色不作为默认 brand | ✅ build_icons 保留多色；SI 用 brand.color |
| Brand vs Strategy vs Dataset | ✅ type=service / policy / network / dataset |
| Variant 多套 | ✅ registry roles（light/dark/compact 预留） |
| 不要 JPG | ✅ SVG master + PNG |
| Client Adapter | ✅ client_profiles + icon_client_adapter.py |
| Icon Coverage | ✅ icon_coverage.py |
| 目录拆 brands/strategies/… | ⏸ 暂缓（避免打断 Raw URL） |

## 命令

```bash
python scripts/icon_coverage.py
python scripts/icon_client_adapter.py
python scripts/icon_resolver.py google --profile client
python scripts/icon_validate.py
python scripts/icon_identity_audit.py
```

## 本阶段明确不做

- 批量重下 100～200 个 Logo
- 迁目录破坏现有 Raw 链接
- icon 写入规则正文
- light/dark/compact 全量实体文件
