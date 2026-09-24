# 文档一致性审计

> 审计基线：2026-09-24 Release；当前规则与发行数据直接读取 `rule/_index.yaml`、`generated/manifest.json` 和 Icon Library V4 当前 Release。

## 1. 发行快照

| 指标 | 当前值 |
|---|---|
| Collection Date | **2026-09-24** |
| Generated At | `2026-09-24T04:39:15.367236+00:00` |
| Run ID | `20260924T043120249584Z-run` |
| IR Digest | `f39d8eb0fd3bf922caafbad6d67ba140a004fa131751fc99221d268deaa6cca7` |
| Rule Index entries | **262** |
| Top-level service sets | **116** |
| Generated files | **1984** |
| Service docs | **264** |

## 2. 本次重构

已建立 `docs/services/**/README.md` 独立服务文档体系，包含服务集、独立服务、子服务、七客户端 Raw、rule_count、SHA-256、更新时间、Run/IR、Icon System 3 身份和使用方式。

已建立 `docs/SERVICE_CATALOG.md`，按顶级服务集组织 262 条规则索引记录。

## 3. 已修正的当前文档

- `docs/README.md`：改为当前 SSOT / 文档入口。
- `docs/RULE_CATALOG.md`：删除旧规则布局叙述，指向当前服务目录。
- `docs/USAGE.md`：修正七客户端实际目录与使用方式。
- `docs/architecture.md`：修正 `rule/manifest.json` 漂移，当前索引为 `rule/_index.yaml`。
- `docs/rule-layout.md`：标记为历史 V1 Reference，避免与当前 V3 混淆。
- `docs/CLIENT_ICON_PROFILES.md`、`docs/CLIENT_ICON_URLS.md`：切换到 Current Icon System 3。
- `docs/ICON_LIBRARY.md`、`docs/ICON_ENGINE.md`、`docs/POLICY_ICONS.md`：更新 Current V3 SSOT 边界。
- `docs/RULE_USAGE_GUIDE.md`：更新为服务目录驱动的当前使用说明。

## 4. 统计口径特别说明

`rule/_index.yaml` 的 `rule_count` 是当前服务的**语义规则数量**，也是服务页主要使用的规则数量。

`generated/manifest.json` 中客户端文件的 `rule_count` 是发行清单记录字段。当前 **262 个 sing-box 客户端规则条目该字段全部为 0**；抽查当前 `generated/singbox/12306/12306.json` 可见其 `rules` 数组实际包含 `domain_suffix` 数据。因此文档不会把 sing-box Manifest 的 0 当成“该服务没有规则”，也不会擅自修改生成产物统计。

## 5. 历史文档处理

带有 Phase、V1、V2、Freeze 或明确历史日期的文档属于演进记录。本次不把历史结论伪装成当前规范，而是保留其历史证据属性，并要求当前使用优先从根 README、SERVICE_CATALOG、RULE_USAGE_GUIDE、ARCHITECTURE 和 ICON_USAGE 进入。

## 6. 统一 SSOT

- 规则服务语义索引：`rule/_index.yaml`
- 客户端最终文件清单：`generated/manifest.json`
- Network Dataset 清单：`generated/network_manifest.json`
- 当前图标 SSOT：`assets/icons/v4/release-pointer.json`
- 服务说明页：`docs/services/**/README.md`
- 全量服务目录：`docs/SERVICE_CATALOG.md`

## 7. Icon V4 重构

当前 Rule Index 262 条记录实现 100% 图标覆盖：86 条可信品牌图精确复用、49 条可信品牌图安全继承、127 条九风格 semantic fallback。缺失身份不使用假品牌 Logo。
