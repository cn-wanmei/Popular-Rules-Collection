# Legacy V1 Rule Tree

`rule/` 是历史 V1 Canonical Service Model 的保留浏览树，用于迁移、审计和兼容性追踪。

它**不是**当前 V3 Runtime 的生产真源，也不是 `generated/` 的编译输入。

当前 V3 真源：

```text
backup/<date>
  ↓
data/runs/<run-id>/canonical
  ↓
data/runs/<run-id>/ir
  ↓
generated/<client>/
```

## 目录语义

- `rule/category/`：历史 Category 实体。
- `rule/service/`：历史 Service / Parent / Child 实体。
- `rule/shared/`：历史共享组件。
- `database/`：Network Dataset 中间层。
- `generated/`：最终发行层。

## 为什么不会和 generated 一致

`rule/` 保留的是历史 V1 结构；`generated/<client>/` 是 V3 Semantic IR 经客户端 Adapter 编译后的投影。两者不是 1:1 文件复制，因此内容不应要求逐文件相同。

## 变更原则

不得因为 `rule/` 与 `generated/` 不一致而直接手工修改生成物。应修改其真实上游输入，重新运行 V3 Engine 并让 CI 生成新的 Release Candidate。
