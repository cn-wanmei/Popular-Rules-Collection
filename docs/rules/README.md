# Rules Index

当前 V3 规则说明索引的权威来源是生产配置与 `generated/manifest.json`。本目录是人类可读派生文档，不是规则正文数据库。

## 当前客户端
`mihomo`、`singbox`、`surge`、`shadowrocket`、`quantumultx`、`egern`、`loon`

## 当前路径模型
`generated/<client>/<ecosystem>/<service-or-all>/rules.*`

旧 `generated/sing-box`、`generated/quantumult-x`、扁平 `generated/<client>/<id>.*` 与 `database/services/*` 均属于旧模型，不得作为新的订阅入口。

## 真源边界
- V3 Canonical：`data/runs/<run-id>/canonical/`
- Semantic IR：`data/runs/<run-id>/ir/`
- 最终发行：`generated/`
- `rule/`：V1 历史浏览/迁移树
- `rules/`：V3 目录契约
