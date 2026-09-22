# 生产链严格审计报告 — 2026-09-22

## 审计对象

- `cn-wanmei/Popular-Rules-Source`
- `cn-wanmei/Popular-Rules-Collection`

## 已验证的不变量

- Collection 当前生产日期：2026-09-22。
- Service Rule 客户端固定 7 个：Mihomo、sing-box、Surge、Shadowrocket、Quantumult X、Egern、Loon。
- `generated/manifest.json`：1564 个文件；7 个 client scopes + 8 个 Network Dataset scopes。
- 7 个客户端的 manifest 条目数与实际目录逐一一致，无 missing / extra。
- Collection immutable Source registry 的 8 个 active bindings 全部固定于 Source durable release commit `ffc7375b31080ea735c8bcc8ee59066b969c382f`，逐项核对 checksum / content digest / evidence digest / policy digest / generator digest / release digest。
- Source 在 `ffc737...` 后的 main 提交可以只是 lifecycle / candidate；不能因 SHA 较新就判定生产漂移。
- Icon System 3 当前 release pointer：`2026.09.22-5e0e48ad55c6`；244 entries；Gate / QA PASS；7 个 client index 各 164 个 stable entries。

## 分流规则与目录

当前生产规则目录为：

`generated/<client>/<ecosystem>/<service-or-all>/rules.*`

其中 client 目录固定为：

`mihomo`, `singbox`, `surge`, `shadowrocket`, `quantumultx`, `egern`, `loon`

Network Dataset 独立 scope：

`asn`, `geoip`, `geosite`, `ip`, `mmdb`, `network`, `policies`, `provider`

`rule/` 是 V1 历史浏览/迁移树；`rules/` 是 V3 目录契约；Legacy Source evidence 不属于 V3 Runtime 真源。

## 已确认问题与修复

### 1. Source Scheduled Generate

Run `35701318301` 的 Validate / Generate 全部成功，失败点是 `gh pr create`；根因是仓库级 GitHub Actions PR 创建策略，而非数据或规则生成失败。

已处理：

- PR #27 承接并合入该 run 产生的候选 Source snapshot refresh。
- PR #28 修复 Generate workflow：
  - 增加 concurrency；
  - PR 创建失败不再伪装成数据生成失败；
  - 输出明确 handoff status / error artifact；
  - PR #28 已通过 CI + Phase 2 Source Gate，并已合并，merge SHA `ac853f5e6504168b5242e1fd230a171b9d2ee594`。

### 2. Collection Source Auto Handoff

`.github/workflows/source-auto-handoff.yml` 存在同类 `gh pr create` 风险。

本审计分支已增加 fail-safe handoff：
- PR 创建失败 → 明确 warning；
- 保留 handoff branch；
- 保存 `source-handoff-status.txt` / error / PR URL；
- 上传 artifact；
- 不把仓库权限策略误报为 source data failure。

### 3. 文档路径漂移

原有 `docs/rules/*.md` 出现：
- 旧 client 目录 `generated/sing-box` / `generated/quantumult-x`；
- 旧的扁平 `generated/<client>/<id>.*`；
- 把 Legacy database 路径当运行时真源；
- 引用已不存在的文档生成脚本；
- 过期生产日期。

本审计分支已重建核心 V3 / Icon / Routing / Publish 文档，并按当前 `service_primary.yaml + generated/manifest.json` 重建全部 90 个配置服务说明页；同时恢复完整导航，将另外 118 个历史/聚合页面标注为非当前 90-service SSOT。

### 4. 文档防漂移 Gate

新增 `scripts/docs_ssot_gate.py` 并接入 `Directory Gate`：

- 90 个配置服务必须都有 `docs/rules/<id>.md`；
- 当前生产页不得使用旧 client 目录、旧文档生成器或旧路径作为当前入口；
- 页面引用的 `generated/.../rules.*` 必须实际存在于 `generated/manifest.json`；
- 当前规则索引必须覆盖 90 个配置服务；
- Legacy 路径仅允许在明确“历史/Legacy、非 Runtime 真源”的语境出现。

## 控制面剩余项

GitHub Actions repository-level “Allow GitHub Actions to create and approve pull requests” 仍是自动 PR 创建的外部控制项。工作流中的 `permissions: pull-requests: write` 不能替代该仓库级设置。

## 结论

当前生产规则、Network Dataset、immutable Source lineage、Icon System 3、分流目录契约均有可验证身份链。

代码侧的 CI PR-handoff 已修复并验证；Collection 文档当前 SSOT 已重建并增加防漂移 Gate。唯一尚需仓库 Settings 层完成的动作，是恢复 GitHub Actions 自动创建/批准 PR 的仓库级权限；在该权限未开启期间，workflow 会保留 branch + handoff evidence，而不会把权限阻断误判为生成失败。
