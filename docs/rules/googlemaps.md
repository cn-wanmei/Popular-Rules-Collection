# Google Maps

| 项目 | 内容 |
|---|---|
| Rule ID | `googlemaps` |
| Service Type | service |
| Current SSOT | `config/service_primary.yaml` |
| Source lifecycle | `config/service_production_gate.yaml` |

## 说明

本页属于当前 Service SSOT 的独立子服务入口。域名与各客户端可订阅文件以当前 `generated/manifest.json` 及发布流水线产物为准；本页不复制域名清单，避免与运行时数据产生第二真源。

## 当前路径模型

客户端规则统一使用：

`generated/<client>/<ecosystem>/<service-or-all>/rules.*`

客户端目录：

`mihomo` · `singbox` · `surge` · `shadowrocket` · `quantumultx` · `egern` · `loon`

## 生命周期

Source 与 Collection 的 immutable lineage 未完成精确绑定前，本页只作为服务身份与导航入口，不将候选状态误标为 Production。

