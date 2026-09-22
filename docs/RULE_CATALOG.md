# 规则目录与使用场景

## 当前生产目录
规则最终发行结构由 `config/builder_registry.yaml` 与 `generated/manifest.json` 锁定：

```text
generated/
├── mihomo/<ecosystem>/<service-or-all>/rules.yaml
├── singbox/<ecosystem>/<service-or-all>/rules.json
├── surge/<ecosystem>/<service-or-all>/rules.list
├── shadowrocket/<ecosystem>/<service-or-all>/rules.list
├── quantumultx/<ecosystem>/<service-or-all>/rules.list
├── egern/<ecosystem>/<service-or-all>/rules.yaml
└── loon/<ecosystem>/<service-or-all>/rules.list
```

客户端目录名以 Builder Registry 为准：`mihomo`、`singbox`、`surge`、`shadowrocket`、`quantumultx`、`egern`、`loon`。

## 使用原则
1. 规则集负责匹配；DIRECT / PROXY / REJECT 等策略由客户端配置决定。
2. Service Rule 与 Network Dataset 是不同语义层。
3. Provider / ASN / GeoIP / Geosite 不能仅凭出现的域名或 CIDR 证明产品归属。
4. 不得把旧 `generated/sing-box`、`generated/quantumult-x` 或 `database/*` 路径作为当前生产订阅入口。

## Network Dataset
最终 scope：`network`、`geosite`、`geoip`、`provider`、`asn`、`ip`、`policies`、`mmdb`。

## SSOT
V3 Canonical=`data/runs/<run-id>/canonical`；Semantic IR=`data/runs/<run-id>/ir`；最终消费者入口=`generated/`。