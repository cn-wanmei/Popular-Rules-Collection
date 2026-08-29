# Icon P2 详细规划（严格审计稿）

> 状态：**方案审计，未执行**。

## 1. 目标

在 P0/P1 锁定 SSOT + CDN + QA 后做**按需**深化，不进全量造图。

## 2. 做

| 编号 | 项 |
|------|----|
| P2.1 | dark/light **仅白名单**（浅色/白标在深色 UI 不可见） |
| P2.2 | 物理目录**双写**（旧路径保留 ≥1 大版本） |
| P2.3 | SI `upstream_version` + `retrieved_at` 钉扎 |
| P2.4 | content-ratio 可配置 HARD（默认 WARN） |
| P2.5 | 官方包入口 `assets/icons/official/{id}.svg` |

## 3. 不做

- 全量 dark/light
- 自动搜 Logo
- 打断 raw URL 的一次性改目录
- 图标写入 ruleset JSON
- favicon 作主资产

## 4. dark/light 条件（须全满足）

1. official_whitelist 或 approved_mono
2. QA near_white/black_ratio 超阈且主题需要
3. 人工 `approved_theme_variant: true`

## 5. 执行顺序

```text
P2.3 钉扎 → P2.5 官方包入口 → P2.1 主题变体
     → P2.4 QA 开关 → P2.2 双写（最后、可选）
```

## 6. 验收

- dark/light 数量 ≤ 白名单子集
- 旧 PNG URL 200
- icon_qa hard=0 · Wrong Identity=0
- statistics 含 theme_variant 计数

**结论：** P2 是运营级深化，不是再开一轮补图标。
