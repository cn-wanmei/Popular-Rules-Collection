# 王者荣耀（国服）

| 项目 | 内容 |
|---|---|
| Rule ID | `honorofkings_cn` |
| Service Type | service |
| Current SSOT | `config/service_primary.yaml` |
| Runtime manifest | `generated/manifest.json` |

## 说明

本页是当前独立子服务的文档入口。域名规则不在文档页重复维护，实际订阅内容以当前生成 manifest 与发布产物为准。

## 客户端路径模型

`generated/<client>/<ecosystem>/<service-or-all>/rules.*`

支持客户端：Mihomo、sing-box、Surge、Shadowrocket、Quantumult X、Egern、Loon。

## 生命周期

Source 的 immutable lineage 与 Collection 的 registry 共同决定可发布状态；候选或审核状态不会在本页被误标为 Production。

