# 生产链严格审计报告 — 2026-09-22

## 审计对象
- `cn-wanmei/Popular-Rules-Source`
- `cn-wanmei/Popular-Rules-Collection`

## 已验证的不变量
- Collection 当前生产日期为 2026-09-22。
- Service Rule 客户端固定为 7 个：Mihomo、sing-box、Surge、Shadowrocket、Quantumult X、Egern、Loon。
- `generated/manifest.json` 当前为 1564 个文件，并覆盖 7 个 client scope 与 8 个 Network Dataset scope。
- 7 个客户端的 manifest 条目数与实际生成树逐一一致，无 missing / extra。
- Collection immutable Source registry 的 8 个绑定均固定在 Source durable release commit `ffc7375b31080ea735c8bcc8ee59066b969c382f`；逐项核对 release checksum 与 content / evidence / policy / generator / release digest 均一致。
- Source 后续 main commit 不自动等同于生产漂移；候选 snapshot 必须经过 durable release / Collection Source Gate。
- Icon System 3 当前 release pointer 为 `2026.09.22-5e0e48ad55c6`；244 entries，Gate / QA PASS；7 个 client index 各 164 个 stable entries。

## CI 缺陷

### Source Generate run 35701318301
Validate / Generate 成功，失败集中在 `gh pr create`：GitHub Actions token 被仓库级策略禁止创建/批准 Pull Request。

代码侧已处理：
- PR #27 承接该失败 run 已生成的候选刷新分支。
- PR #28 将 PR 创建失败改为显式 handoff evidence，不再伪装成数据生成失败。
- 增加 concurrency，避免 schedule / manual 并发生成。
- PR #28 已通过 Source CI 与 Phase 2 Gate 并已合并。

永久控制面仍需：Settings → Actions → General → Workflow permissions → 开启允许 GitHub Actions 创建和批准 Pull Requests。

### Collection Source Auto Handoff
发现同类潜在阻断：`.github/workflows/source-auto-handoff.yml` 同样使用 `gh pr create`。本审计分支已增加同样的 fail-safe handoff evidence，避免未来 Source durable seal 有变化时把权限策略误报为生产失败。

## 文档 / 路径漂移

已确认旧说明层存在：
- `generated/sing-box` / `generated/quantumult-x` 等旧客户端目录名；
- 扁平 `generated/<client>/<id>.*` 假设，而当前真实结构是 `generated/<client>/<ecosystem>/<service-or-all>/rules.*`；
- 将 `database/services/*` 描述为运行时数据来源；
- 历史文档仍引用已不存在的 `scripts/generate_docs.py` / `scripts/generate_rule_pages.py`；
- Icon 历史文档仍把旧 V1/V2 脚本当作当前生产链。

本审计分支已修订核心生产 / 架构 / 发布 / Icon SSOT 文档，并新增 8 个当前 Source 服务的规则说明页：
`1688`、`cainiao`、`dingding`、`qqmail`、`qqmusic`、`taobao`、`tencentcloud`、`tmall`。

## 尚未宣称为“完全清理”的部分

旧 `docs/rules/*.md` 中仍有历史页需要继续按 `generated/manifest.json` 批量再生；本 PR 不会把未完成的历史页伪装成已经清零。当前 SSOT 已明确要求：出现旧路径时以 V3 manifest 为准。

## 结论

生产规则、Network Dataset、immutable Source binding、Icon System 3 release 的内部身份链当前可被精确核验。剩余真正的外部阻断是 GitHub repository-level Actions PR permission；文档层的当前核心入口已纠正，历史逐服务页的全面再生属于后续专门文档生成任务。