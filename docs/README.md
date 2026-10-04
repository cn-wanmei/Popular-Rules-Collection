# 文档与生产 / 规则使用入口

> **当前**说明以 `rule/_index.yaml`、`generated/manifest.json`、`SERVICE_CATALOG.generated.md` 与 CI 状态为准。  
> 日期快照与手写数量不是权威。Icon System **6.0** 为当前视觉体系。

## 当前 SSOT

| 用途 | 入口 |
|---|---|
| 项目 / 快速入口 | [根 README](../README.md) |
| **服务身份权威** | [rule/_index.yaml](../rule/_index.yaml) |
| **当前服务目录（机器生成）** | [SERVICE_CATALOG.generated.md](SERVICE_CATALOG.generated.md) |
| 客户端文件清单 | [generated/manifest.json](../generated/manifest.json) |
| 动态发布状态 | [PUBLISH_STATUS.md](../PUBLISH_STATUS.md) |
| Network Dataset provenance | [generated/network_manifest.json](../generated/network_manifest.json) |
| 文档总索引 | [INDEX.md](INDEX.md) |
| Icon System 6.0 | [Popular-Rules-Icon](https://github.com/cn-wanmei/Popular-Rules-Icon) |
| Icon V6 cutover | [ICON_V6_CUTOVER.md](ICON_V6_CUTOVER.md) |

## 文档分层

```text
当前体系
├── README.md（制度与入口，不写权威数字）
├── docs/INDEX.md
├── docs/SERVICE_CATALOG.generated.md  ← 当前目录
├── rule/_index.yaml                   ← Identity SSOT
├── generated/manifest.json            ← 客户端产物清单
├── docs/services/** · docs/rules/**
└── docs/archive/ · SERVICE_CATALOG.md  ← 历史
```

## 历史说明

- [SERVICE_CATALOG.md](SERVICE_CATALOG.md) — 旧静态快照，**勿作当前权威**
- [RULE_USAGE_GUIDE.md](RULE_USAGE_GUIDE.md) — 用法说明；文中旧数字请以 SSOT 为准
