# NetEase Music

> Current V3 service documentation. Subscription paths are derived from `generated/manifest.json`.

| 项目 | 内容 |
|------|------|
| Rule ID | `neteasemusic` |
| Primary Ecosystem | `netease` |
| Service Type | service |
| Parent Aggregate | `netease` |
| Release Date | — |
| Dedicated client outputs | 0 / 7 |

## 当前生产订阅路径

当前 Release Candidate 尚未完成该服务的独立客户端发行与 immutable Source 绑定；不得根据历史页面或聚合规则猜测订阅地址。

## 当前真源边界

- V3 Canonical：`data/runs/<run-id>/canonical/`
- Semantic IR：`data/runs/<run-id>/ir/`
- 最终发行：`generated/`
- Source 补全：`Popular-Rules-Source/generated/source/neteasemusic/`
- `rule/`：V1 历史浏览/迁移树
- `database/services/`：Legacy evidence，不是 V3 Runtime 真源

## 目录契约

当前客户端目录只能使用 `mihomo`、`singbox`、`surge`、`shadowrocket`、`quantumultx`、`egern`、`loon`。Source Release 通过后才允许进入 Collection immutable binding。

---
_页面日期来源：2026-09-23。生产路径来源：generated/manifest.json。_
