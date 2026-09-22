# V3 Rule Directory Contract

`rules/` 是 V3 目录契约的保留结构，用于描述 Canonical Provider / Service / Aggregate 的目标路径。

当前生产运行的 Canonical 数据保存在 `data/runs/<run-id>/canonical`，因此 `rules/` 不应被理解成另一套独立的 Runtime 数据库。

```text
backup/<date>
    ↓
data/runs/<run-id>/canonical   ← V3 canonical truth
    ↓
data/runs/<run-id>/ir
    ↓
generated/<client>/<provider>/<service>/...
```

## 与 rule/ 的区别

- `rule/`：历史 V1 Canonical 浏览/迁移树。
- `rules/`：V3 目录契约目标与结构约束。
- `data/runs/<run>/canonical`：当前 V3 运行时 Canonical 真源。
- `generated/`：最终客户端和 Network Dataset 发行层。

因此 `rule/`、`rules/`、`generated/` 三者不承担相同职责，也没有逐文件一致性要求。

## Service 与 Network 的边界

Service Rule 进入 `generated/<client>/...`；Network Dataset 进入：

`generated/network/`、`generated/geosite/`、`generated/geoip/`、`generated/provider/`、`generated/asn/`、`generated/ip/`、`generated/policies/`、`generated/mmdb/`。

Provider、ASN、GeoIP、Geosite 都不得反向推导为 Service Identity。
