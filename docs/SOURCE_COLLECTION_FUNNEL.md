# Source → Collection 晋升漏斗（运营 SSOT）

> **Source lifecycle ≠ Collection production。**  
> 用户可见服务身份以 Collection `rule/_index.yaml` + `PUBLISH_STATUS.md` 为准。  
> 本文件只约束证据侧晋升节奏与阻塞处理。

## 状态机

`review → verified → canary → production`（另有 `blocked`）

| 阶段 | 含义 | 禁止 |
|---|---|---|
| REVIEW | 证据候选 | 不得宣称 Collection production |
| VERIFIED | 证据完整，可候选 canary | 不得跳级到 production |
| CANARY | Source 试运行 / 可 handoff | 无 Collection canary 证据不得标 production |
| PRODUCTION | Source durable + Collection 绑定 | 必须有 immutable binding 证据 |
| BLOCKED | 证据断流 / domains=0 / 策略禁止 | 不得自动晋升 |

## 周度配额（A）

- **目标**：每周从 **VERIFIED** 晋升 ≥ **8** 个服务到 Source **canary**（再经 Collection Auto Handoff → Collection canary）。
- **禁止跳级**：VERIFIED 不得直接改 production。
- **本周批次（2026-10-03）**：`appledev` `appstore` `icloud` `applemusic` `applemedia` `azure` `openai` `claude` → Source canary（`reason: weekly_funnel_quota_2026-10-03`）。

## 阻塞看板（B）

Source 仓生成：

```bash
python scripts/source_blocked_board.py
# docs/BLOCKED_BOARD.md + reports/blocked_board.json
```

优先级：`BLOCKED` → `domains=0` → Collection Source health failed → 长期 REVIEW。

## 与 Collection 交接

```text
Source canary/production seal
  → Collection Auto Handoff PR
  → Source Gate → Collection canary → production
```
