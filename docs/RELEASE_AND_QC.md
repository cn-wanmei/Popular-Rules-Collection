# Release & QC — Popular Rules Collection

## Release Candidate Hard Bar

~~~text
Validation Errors = 0
Schema Errors = 0
Generated Empty = 0
Stale Files = 0
Broken Links = 0
Builder Coverage = 100% × 7 clients
~~~

## Current Clients

mihomo / singbox / surge / shadowrocket / quantumultx / egern / loon。

## Popular-Rules-Source

PRS 已注册但当前 disabled。

重新启用必须同时满足：

~~~text
official evidence only
+
service boundary
+
exclusion
+
conflict = 0
+
deterministic snapshot
+
collection reconciliation
~~~

Authoring seed、test fixture、未经验证第三方规则不能直接进入 Production。

## Daily Coverage

Daily Coverage 不能把 raw materialized / registered 直接解释为 Missing。

Intentional SSOT：

config/intentional_unmaterialized.yaml

## Phase 8

Catalogue Coverage 100% 不足以授权 Legacy 删除。

Deletion-ready 仍要求：

- Legacy Asset Equivalence = 100%
- zero missing Legacy AssetKeys
- Golden 完整
- 7-client artifacts 完整
- 同一 immutable Snapshot 的三次确定性构建
- zero unexplained removed assets
- v2_runtime_dependency = 0
- evidence 绑定当前 commit
- explicit operator action

## Current

Phase O 尚未执行完成，Legacy 继续受控保留。

历史工作流与报告只作为审计证据，不能改变当前 Production State。
