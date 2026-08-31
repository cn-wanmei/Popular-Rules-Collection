# Builders 与 Decision SSOT

| 产物 | 输入 | 用途 |
|------|------|------|
| `generated/{client}/{service}.*` | rule_loader | 按服务订阅 |
| `generated/routing/decisions.jsonl` | routing_emit | 域名最终动作 SSOT |
| `generated/policies/{direct,proxy,reject}/` | decision 派生 | 策略规则集 |

**不**用 decision 替换 service builder，以免破坏订阅模型。
