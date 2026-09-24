# 文档与生产 / 规则使用入口

> 当前文档体系以 2026-09-24 Release 为基线；Icon Library V4 在 2026-09-25 进行了独立视觉重构。历史 Phase / V1 / V2 / Freeze 文档仅用于追溯，不覆盖当前 SSOT。

## 当前 SSOT

| 用途 | 入口 |
|---|---|
| 项目 / 快速入口 | [根 README](../README.md) |
| 服务 / 子服务全量目录 | [SERVICE_CATALOG.md](SERVICE_CATALOG.md) |
| 每个服务独立说明 | [services/](services/) |
| 规则语义索引 | [rule/_index.yaml](../rule/_index.yaml) |
| 客户端文件清单 | [generated/manifest.json](../generated/manifest.json) |
| Network Dataset provenance | [generated/network_manifest.json](../generated/network_manifest.json) |
| 当前 Icon Usage | [ICON_USAGE.md](ICON_USAGE.md) |
| 当前 Icon Style Guide | [ICON_STYLE_GUIDE_V4.md](ICON_STYLE_GUIDE_V4.md) |

## 文档分层

```text
当前 Release
├── README.md
├── docs/SERVICE_CATALOG.md
├── docs/services/**/README.md
├── docs/RULE_USAGE_GUIDE.md
├── docs/GENERATED_OUTPUTS.md
├── docs/NETWORK_DATASETS.md
├── docs/ARCHITECTURE.md
├── docs/ICON_USAGE.md
└── docs/ICON_STYLE_GUIDE_V4.md

图标 SSOT
└── assets/icons/v4/
    ├── release-pointer.json
    ├── manifest.json
    ├── service-index.json
    └── styles/<style>/service.svg

历史 / 兼容
└── assets/icons/v3/
    └── 作为品牌原生图标来源与回滚兼容层保留
```

## 防止漂移

服务页、服务目录和根 README 的服务快捷目录按当前 Release 数据维护。不要手工改发行数字、Raw URL、SHA-256 或图标路径。

图标必须遵循 `assets/icons/v4/release-pointer.json → manifest.json / service-index.json` 的 SSOT 链路。任何服务的最终图标地址以 `service-index.json` 为准，不根据文件名自行推断。
