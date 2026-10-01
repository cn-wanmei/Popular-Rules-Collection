# Phase 2 Main Replacement Feasibility

## 结论

技术上可行，且风险可控，但必须是**正常 PR 合并 / fast-forward**，而不是强制替换 main ref。

## 推荐顺序

1. main 保持冻结。
2. Phase 2 完成并在独立分支跑全量 CI。
3. Source Release 先走单 Service Canary。
4. Collection 完成一次完整 V3 Build。
5. 7 客户端语义回归通过。
6. 验证 rollback。
7. Merge Phase 2 PR 到 main。
8. 验证 main SHA 与已通过 Gate 的提交一致。
9. 最后才恢复 production writers。

## 为什么不直接替换 main

当前生产证据带有 commit / run 绑定。直接 force-replace 可能：

- 破坏证据链的 commit identity
- 绕过 PR 审计记录
- 与正在保留的 Legacy / Phase O 状态产生不一致
- 增加 rollback 难度

所以正常 Merge 是更稳定的生产切换路径。

## 可并行范围

可以并行：

- 8 个服务 Source 补全
- Candidate Ledger
- Official Adapter
- Boundary / Exclusion
- Reconciliation
- Collection Canary
- 7-client Regression

不能并行绕开的部分：

- Production Gate
- Source Release
- Reconciliation
- Main Activation

## 当前前置条件

PRS Registry 当前必须保持 disabled。

当前 main 也处于生产写入冻结状态。
