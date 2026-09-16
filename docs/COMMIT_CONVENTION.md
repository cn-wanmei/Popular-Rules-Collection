# Commit Convention

本项目自 V3 治理阶段起采用 Conventional Commits 风格，并要求一个提交只表达一个逻辑变化。历史提交不重写、不 rebase、不 force-push；规范只约束后续提交。

## Format

```text
<type>(<scope>): <imperative summary>
```

常用类型：

- `feat`：新增能力
- `fix`：缺陷修复
- `refactor`：结构治理、无行为目标变化
- `test`：测试与质量门禁
- `docs`：文档
- `chore`：维护、清理、生成状态
- `ci`：工作流与 CI/CD

## Examples

```text
fix(ci): stabilize collection date propagation
fix(status): generate publish status from release evidence
feat(retention): add historical snapshot lifecycle
refactor(health): separate source lifecycle from raw telemetry
chore(v3): remove archived migration layer
test(architecture): enforce legacy reference gate
```

## Repository rule

- 不为了“整理历史”而重写已经进入 `main` 的提交。
- 一个提交不要同时混入无关的健康治理、Retention 与业务规则变更。
- 自动生成文件使用 `chore(status): ...` / `chore(retention): ...`。
- 破坏性历史数据清理由独立 Retention workflow 执行，不与 Collection 提交绑定。
