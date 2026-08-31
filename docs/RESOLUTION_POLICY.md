# Resolution Policy（DNS）

与 [ROUTING_CONTRACT.md](ROUTING_CONTRACT.md) **正交**。

```text
域名/意图 → Resolution Policy → DNS 服务器
流量路径  → Routing Contract  → DIRECT | PROXY | REJECT
```

- 注册表：`database/policies/dns/servers.yaml`
- 意图：`config/resolution_policy.yaml`
