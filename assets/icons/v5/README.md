# Icon System V5 — Legacy Fallback Archive

**Status:** `legacy_fallback_only`

V5 已退出正常生产路径。Collection 当前默认使用 Icon System V6：
`config/icon_v6.yaml` → `cn-wanmei/Popular-Rules-Icon@dist`。

本目录暂时保留的目的仅为：

- V6 身份边界迁移期间的回滚；
- V6 生产链故障时的临时兜底；
- 历史审计与可复现证据。

禁止继续运行 V5 自动补全、质量重抓或 promote 工作流。

历史 V5 曾以 146 service 为 bootstrap 基准；该数字不代表当前 Collection service universe。
当前 canonical service universe 由 Collection `rule/_index.yaml` 决定。