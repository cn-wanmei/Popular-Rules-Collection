# Popular-Rules-Collection

> 规则数据供应链 + 标准化中间库 + 多客户端构建系统

## 当前生产定位

Service Rules 的生产构建统一由 V3 Engine 执行：

~~~text
Upstream / Source Registry
  → collect
  → immutable snapshot
  → ingest
  → quarantine
  → canonical
  → hierarchy / decision
  → IR
  → 7 client adapters
  → diff
  → golden
  → release gate
  → atomic promotion
  → generated/
~~~

Network Dataset 为独立轨道，不进入 V3 Service Rule Runtime。

## 当前 7 个生产客户端

mihomo、singbox、surge、shadowrocket、quantumultx、egern、loon。

历史文档中的 Clash Meta 不再作为独立生产 Adapter 计数。

## Popular-Rules-Source 状态

Popular-Rules-Source 已注册到 Source Registry，但当前入口为 disabled。

原因：

- PRS 当前仍处于 Source Candidate / Review 阶段。
- 首批服务历史上存在 Seed / Fixture 参与生成的问题，已在 Source 仓库中清理。
- 正式启用前必须通过 official-evidence-only、Boundary、Exclusion、Conflict、Determinism 与 Reconciliation Gate。

首批目标服务：

1688、cainiao、dingding、qqmail、qqmusic、taobao、tencentcloud、tmall。

其中 Tencent Cloud 当前为 PARTIAL，因为 Collection 已存在对应 Registry 映射，只做补充。

## 目录

| 路径 | 用途 |
|---|---|
| rule/ | V1 Canonical / 人读浏览 |
| database/ | Network Dataset 中间库 |
| generated/ | 当前发布投影 |
| sources/ | Source / Dataset Registry 与健康信息 |
| data/runs/ | V3 immutable run 与 release evidence |
| src/engine/ | 唯一 Service Rule Production Engine |
| config/ | Pipeline / Capability / Intentional / Production Policy |
| reports/ | 覆盖、质量、生产门禁与发布证据 |
| tests/ | Contract / Regression Tests |

## Legacy

database/services/ 是 Phase 8 Legacy Source，不是 V3 Runtime 输入。

rule/ 是当前 V1 Canonical Service Model。

Legacy 自动删除不是默认行为；删除必须经过独立、显式、当前 HEAD 绑定的迁移 Gate。

## 开发者快速开始

~~~bash
pip install -r requirements.lock
python scripts/collect.py

DAY=$(date -u +%Y-%m-%d)
PYTHONPATH=. python -m src.engine.cli all --sources "backup/$DAY" --data data

PYTHONPATH=. python -m src.engine.cli --version
PYTHONPATH=. python -m src.engine.cli naming_gate
~~~

## 发布原则

- generated/ 不是 Source of Truth。
- Build 成功不等于 Legacy 已删除。
- Source Health 与 Service Coverage 分开判断。
- 单次 upstream failure 不等于生产失败。
- 所有生产声明必须绑定 immutable run、release evidence 与当前 commit。
