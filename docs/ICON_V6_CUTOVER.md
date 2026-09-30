# Icon V6 R5 Cutover

**Date:** 2026-09-30  
**Default provider:** `v6`  
**Active dist release:** `icon-2026.09.30.r14`  
**Manifest:** `manifests/icon-2026.09.30.r14.json`  
**Canonical Collection service universe:** 394

## Current verified state

当前 Icon dist manifest 含 482 个条目。与 Collection 当前 `rule/_index.yaml` 的 canonical `entity: service` 集合对比：393/394 个 canonical service_id 存在；89 个 dist 条目不属于当前 Collection service universe；`ai` 缺失。

因此当前状态是：

- V6 已作为默认生产 provider；
- V6 身份覆盖尚未达到 100%；
- V5 仍保留为临时 rollback/fallback 安全网；
- 不得清理 V5。

## 已修正的配置漂移

原配置/文档混用了 `icon-2026.09.30.styles8`、`icon-2026.09.30.freeze1` 与实际 dist release `icon-2026.09.30.r14`。当前以 `r14` 为唯一已验证发布指针。

## 已发现的生产链路问题

实际 dist manifest 的 variant `path` 记录为 `.bin`，而 dist 物理文件是 `.png`；resolver 当前直接生成 `.png` URL。该元数据不一致必须由 release gate 阻断，不能继续扩大。

Icon Repository 当前 `release.yml` 与 `incremental.yml` 仍属于 placeholder/scaffold，说明完整的可重复 release writer 尚未在主线固化。因此不能把当前 dist 存在误认为生产链路已经完整健康。

## V5 removal gate

只有以下条件全部满足，才能删除 `assets/icons/v5`：

1. Collection canonical services = V6 entries = 100%；
2. production dist 中 zero orphan entries；
3. zero production fallback to V5；
4. resolver 能在固定 manifest 上成功解析；
5. manifest path 与物理对象扩展名完全一致；
6. Icon Repository 有可重复的 release writer + validation workflow；
7. Collection 全仓库无 V5 active reference；
8. 回滚方案已经迁移到独立 immutable release，而不依赖 V5 本地资产。

在上述条件满足前，V5 必须保留，但不得继续扩充。