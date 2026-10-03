# Source → Collection 晋升漏斗

> 可视化 Source lifecycle 与 Collection 生产绑定的差距。数据以 Source README 生成表与 Collection `rule/_index.yaml` 为准。

## 阶段定义

| 阶段 | 含义 | 责任仓 |
|---|---|---|
| REVIEW | 证据候选，未达 Source release 门槛 | Source |
| VERIFIED | 证据完整，可候选 Collection canary | Source |
| PRODUCTION (Source) | Source 侧 durable release / seal | Source |
| Collection canary | Collection 绑定试运行 | Collection |
| Collection production | 进入 canonical + 客户端发行 | Collection |

## 使用

```bash
# 在 Source 仓
python -m source_engine health
python -m source_engine qualify

# 在 Collection 仓对照
# rule/_index.yaml 中 entity=service 数量 = 当前用户可见服务身份
```

## 运营建议

1. **每周目标**：从 VERIFIED 晋升 ≥ N 个服务到 Collection canary（N 按人力设定，建议 5–10）。
2. **阻塞看板**：Source 中 `BLOCKED` / domains=0 的服务单独列表，优先修 adapter。
3. **禁止跳级**：无 Collection production 证据不得标 PRODUCTION。
4. **单一事实源**：生命周期表由 Source CI 生成嵌入 README；勿手写覆盖。

## 当前已知结构问题

- Source 侧大量服务停在 REVIEW/CANDIDATE，与 Collection 394 canonical 不对齐 → 证据产能未充分转化为用户规则。
- Collection source health 仍可能出现 stale/failed → Publish 前以 `PUBLISH_STATUS.md` 与 immutable lineage gate 为准。
