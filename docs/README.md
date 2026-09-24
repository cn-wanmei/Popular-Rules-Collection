# 文档与生产 / 规则使用入口

> 当前文档体系以 2026-09-24 Release 为基线。历史 Phase / V1 / V2 / Freeze 文档仅用于追溯，不覆盖当前 SSOT。

## 当前 SSOT

| 用途 | 入口 |
|---|---|
| 项目 / 快速入口 | [根 README](../README.md) |
| 服务 / 子服务全量目录 | [SERVICE_CATALOG.md](SERVICE_CATALOG.md) |
| 每个服务独立说明 | [services/](services/) |
| 规则语义索引 | [rule/_index.yaml](../rule/_index.yaml) |
| 客户端文件清单 | [generated/manifest.json](../generated/manifest.json) |
| Network Dataset provenance | [generated/network_manifest.json](../generated/network_manifest.json) |
| 当前 Icon System 3 | [ICON_USAGE.md](ICON_USAGE.md) |

## 文档分层

```text
当前 Release
├── README.md                    项目首页 / 服务快捷目录
├── docs/SERVICE_CATALOG.md      262 条规则的全量服务目录
├── docs/services/**/README.md   每个服务 / 子服务独立说明
├── docs/RULE_USAGE_GUIDE.md     面向使用者的完整教程
├── docs/GENERATED_OUTPUTS.md    最终发行结构
├── docs/NETWORK_DATASETS.md     Network Dataset
└── docs/ARCHITECTURE.md         当前生产架构

历史记录
└── docs/PHASE* / V1 / V2 / Freeze / dated reports
```

## 防止漂移

服务页、服务目录和根 README 的服务快捷目录按当前 Release 数据维护。不要手工改发行数字、Raw URL、SHA-256 或图标路径。

## 图标体系

当前服务图标入口：[Icon Library V4](../assets/icons/v4/README.md) · [Style Guide](ICON_STYLE_GUIDE_V4.md)。V3 作为现有品牌资产来源与兼容层保留。
