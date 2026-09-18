# Phase 1 — V1 SoT Resolver

## Objective

建立明确、可审计、可回滚的 V1 Service Source-of-Truth（SoT）解析边界，为后续 Service Model Unification 与 Runtime Cutover 提供唯一入口。

## Ownership

- `rule/<service>/` 是 V1 canonical service source。
- `generated/` 仅为发布投影，Resolver 永不读取。
- `database/services/` 属于 Legacy migration boundary；默认禁止参与 V1 runtime resolution。
- Legacy 访问必须显式 `allow_legacy=True`，且结果标记为 `legacy_migration_only`，不得伪装成 V1 SoT。

## Resolver contract

`SoTResolver.resolve(service)` 必须：

1. 对 service 名称执行路径安全校验。
2. 优先且唯一解析 `rule/<service>/`。
3. 返回稳定排序后的文件集合。
4. V1 服务不存在时返回 `unresolved`，不静默回退到 generated 或 Legacy。
5. 不复制、不修改、不生成服务资产。

## Exit criteria

- V1 service resolution 不再依赖 `generated/`。
- 默认运行路径不读取 `database/services/`。
- Resolver 有回归测试覆盖 V1、generated 隔离、Legacy opt-in 与路径逃逸。
- 后续 Phase 2–5 均通过该 resolver 作为服务发现边界，不重新引入第二套 SoT。

## Non-goals

- 本阶段不删除 Legacy。
- 本阶段不统一全部 Service Model。
- 本阶段不执行 Runtime Cutover。
- 本阶段不改变现有客户端 adapter 行为。
