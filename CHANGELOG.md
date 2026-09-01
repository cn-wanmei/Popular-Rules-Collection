# Changelog

## [1.0.0] - 2026-09-01

### V3 Engine → `src.engine` 正式迁移 & 1.0 发布

#### Breaking Changes
- 引擎包路径正式确立为 `src.engine`（代号 v3，非路径）
- `src/v3`、`data/v3`、`config/v3`、`tests/v3`、`reports/v3` 全部移除
- `src.v3` Python 包已不存在；所有导入路径切换至 `src.engine.*`

#### Added
- `src/engine/validation/naming_gate.py`：HARD 命名门，禁止 v3 路径/包重新出现
- `src/engine/pipeline/run.py`：新增 `naming_gate` + `publish` 阶段，完整 12-stage 管道
- `src/engine/release/cutover.py`：`publish_artifacts_to_production()` 支持 dry-run 和空文件保护
- `tests/engine/unit/`：迁移并更新 test_resolver / test_identity / test_golden_levels
- `tests/engine/contract/`：contract smoke 更新至 `data/generated/` 路径

#### Fixed
- `src/v3/__init__.py` 的 `from src.engine import *` 转发层已随旧包一并删除（根本解决，非 workaround）
- IR builder 的 `_invert_memberships` 提取重构；`build_ir` 中 `if not full:` 嵌套条件理清
- `snapshot/engine.py` 默认输出路径由 `data/v3/snapshots/` 修正为 `data/generated/snapshots/`
- `golden/runner.py` 数据路径由 `data/v3/` 修正为 `data/generated/`

#### Pipeline
```
naming_gate → canonical → hierarchy → ir → ir_full → adapters → diff
→ snapshot → quarantine → golden → release → publish
```

#### Gates (全部通过)
- naming_gate: errors=0
- canonical: unique_rules=251728 memberships=291190
- hierarchy: 8 aggregates resolved
- ir: rules=7109 (focus) + 251728 (full)
- adapters: 7 clients (egern / loon / mihomo / quantumultx / shadowrocket / singbox / surge)
- golden: pass=True hard=0 (L1–L7)
- release: status=RC_READY
- publish: ok=True copied=56 files across 7 clients

#### Tests
8/8 passed (tests/engine/unit + tests/engine/contract)

## [1.1.0] - 2026-09-01

### V3 Engine 完全接管 Build — V2 脚本构建退场

#### 架构变更
- `collect.yml`：重写为 8 阶段结构化 pipeline
  - Phase 1: Naming gate（fail-fast）
  - Phase 2: Upstream collect（V2脚本，保留）
  - Phase 3: Normalize + Deduplicate（V2脚本，保留）
  - Phase 4: **V3 Engine build**（canonical→hierarchy→ir→adapters→diff→snapshot→quarantine→golden→release→publish）
  - Phase 5-7: Validation / Reporting / Icon（软门）
  - Phase 8: Commit with diff summary in message
- `build.yml`：完全走 `src.engine.cli`，新增 `dry_run` 输入参数
- `test.yml`：engine 测试优先，legacy 测试 soft

#### New: Engine Diff Module (`src/engine/diff/engine.py`)
- 基于 `identity_key`（SHA256-stable）的精准规则级 diff
- 维护 `data/generated/diff/baseline.jsonl` 跨 run 持久化基线
- 输出 `data/generated/reports/diff/latest.json` + `reports/release/diff_latest.json`
- 首次运行自动 bootstrap；后续每次采集后精准报告 `+N/-M rules`
- commit message 自动携带 diff 摘要（如 `+3/-1 rules`）

#### Deprecated
- `scripts/build_mihomo.py` 等 7 个 V2 build shim 已标记废弃
- `config/builder_registry.yaml` 升级至 version 3，engine_entry 明确为 `python -m src.engine.cli all`

#### Tests: 8/8 passed
