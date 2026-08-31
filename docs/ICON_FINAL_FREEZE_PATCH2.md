# Icon Final Freeze Patch 2

设计方向继续冻结。本补丁只修**实现闭环断点**。

## 对照审计的修正

| 审计主张 | 相对最新 main |
|----------|----------------|
| engine keep_black 白名单 | **已过时** — 当前始终 tint + display_color |
| QA fail 不入 hard | **已过时** — 已认 fail/hard |
| near_black 仅 verified | **已过时** — 已查全部 brand |
| identity_si_refresh 改 source fill | **仍成立** → 本补丁去掉 force_fill |
| CI 全 soft / baseline 自覆盖 | **仍成立** → QA 硬门禁；禁止 CI write-baseline |
| Contact 优先 legacy png | **仍成立** → 优先 rendered |
| Optical 未进 engine | **已过时** — engine 已读 optical_overrides |

## 本补丁

1. `icon_identity_si_refresh.py`：source 只写 SI 身份，不 force_fill
2. `icon_contact_sheet.py`：优先 `rendered/{surface}/`
3. `icon_visual_regression.py`：`--write-baseline` 需 `ALLOW_BASELINE_UPDATE=1`
4. Collect：Icon QA 硬门禁；CI 不再 write-baseline
5. QA 指标说明：occupancy vs fill_density

## 仍冻结（不改）

Dark Surface、几何策略色、64/128/256、source→normalize→render、不重绘品牌。
