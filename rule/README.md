# V1 Rule Model

`rule/` 是 V1 Canonical Service Rule 模型的主入口。

```text
rule/
├── category/   # 分类实体
├── service/    # 服务实体
└── shared/     # 共享组件实体
```

## Entity Boundary

- `category/`：Category，不拥有 Service Canonical Assets。
- `service/`：Service / Parent Service / Child Service。
- `shared/`：跨服务复用的 Shared Component。
- `database/`：Network Dataset，不属于本目录。
- `generated/`：客户端编译产物，不属于 Canonical Source。

## Service Semantics

一个 Service 可以属于多个 Category。

Parent Service 可以同时拥有自己的 assets，并聚合 Child Services：

```text
Parent own assets
+ Child aggregates
+ requires closure
→ canonical dedup
→ artifact
```

## Migration Rule

现有 legacy `rule/<Name>/` 资产在完成审计前不得删除。迁移必须先建立 Service Identity，再建立 Canonical Asset Mapping。

## V3 Contract

V3 Engine 消费 V1 Model，完成 dependency resolution、aggregate resolution、canonical dedup、IR 与客户端 adapter；V1 不直接生成客户端策略。
