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
