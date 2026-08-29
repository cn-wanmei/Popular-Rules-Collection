# 图标库方案（当前终态说明）

## 1. 定位

图标是与 **Service Rules / Network Datasets** 并列的**第三条产品资产管线**，不进入 `database/`，不写入规则正文。

```text
service_id  →  icon_id  →  manifest 实体  →  variants  →  PNG/SVG URL
config/icons.yaml          assets/icons/
```

## 2. 目录与 SSOT

| 路径 | 职责 |
|------|------|
| `config/icons.yaml` | service→icon 绑定、类别、禁止事项 |
| `assets/icons/manifest.yaml` | 图标实体、provenance、文件路径 |
| `assets/icons/registry.yaml` | variant 角色解析 |
| `assets/icons/profiles.yaml` / `themes.yaml` | Profile/Theme |
| `assets/icons/client_profiles.yaml` | 七客户端 URL 模板 |
| `assets/icons/source/*.svg` | SVG Master |
| `assets/icons/png/{64,128,256}/` | 客户端主资产 |
| `assets/icons/monochrome/{size}/` | mono 变体 |

## 3. 类别

| 类别 | 规则 |
|------|------|
| **brand** | 官方色 / Simple Icons；禁止瞎搜 |
| **strategy** | 项目统一几何语言（DIRECT/PROXY/…） |
| **dataset** | China/LAN/GeoIP/ASN…；禁止企业 Logo |
| **pending** | placeholder 显式决策 |

## 4. Variant

| 角色 | 状态 |
|------|------|
| brand（默认） | ✅ |
| mono | ✅ `monochrome/` |
| compact | ✅ 使用 `png/64` |
| dark / light | 预留，未批量造图 |

## 5. 质量门禁

```bash
python scripts/icon_qa.py
python scripts/icon_validate.py
python scripts/icon_identity_audit.py
python scripts/icon_coverage.py
python scripts/icon_resolver.py google --profile client
```

## 6. 客户端

仅 URL 适配。**sing-box 不把图标写入 ruleset。**

## 7. Phase

| Phase | 状态 |
|-------|------|
| I Registry+QA | ✅ |
| II 核心 brand | ✅ |
| III strategy/dataset 统一 | ✅ |
| IV QA hard=0 | ✅ |
| V mono+compact | ✅ |

## 8. 禁止事项

见 `docs/ICON_ARCHITECTURE.md` 十条。
