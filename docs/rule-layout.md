# Rule Layout

当前规则目录采用 **Directory Layout v2**。

- Provider 聚合：`rule/{provider}/{aggregate}/{aggregate}.yaml`
- 子服务：`rule/{provider}/{service}/{service}.yaml`
- `rule/` 只用于人工浏览与选择，不作为客户端运行时输入。
- 聚合与同名子服务可以同时存在，因为使用不同的实体 ID 与目录层。

示例：

```text
rule/acfun/acfun_aggregate/acfun_aggregate.yaml
rule/acfun/acfun/acfun.yaml
```

详细规范见 [docs/layout.md](layout.md) 与 [rule/_index.yaml](../rule/_index.yaml)。
