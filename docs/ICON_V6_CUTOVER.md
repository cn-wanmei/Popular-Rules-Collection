# Icon V6 R5 Cutover

**Date:** 2026-09-30  
**Default provider:** `v6`  
**Active dist release:** `icon-2026.09.30.r14.1`  
**Manifest:** `manifests/icon-2026.09.30.r14.1.json`  
**Canonical Collection service universe:** 394

## Current verified state

当前 Icon dist manifest 含 482 个条目。与 Collection 当前 `rule/_index.yaml` 的 canonical `entity: service` 集合对比：393/394 个 canonical service_id 存在；89 个 dist 条目不属于当前 Collection service universe；`ai` 缺失。

因此当前状态是：

- V6 已作为默认生产 provider；
- V6 身份覆盖尚未达到 100%；
- V5 仍保留为临时 rollback/fallback 安全网；
- 不得清理 V5。

## 已修正的配置漂移

原配置/文档混用了 `icon-2026.09.30.styles8`、`icon-2026.09.30.freeze1` 与实际 dist release `icon-2026.09.30.r14.1`。当前以 `r14.1` 为唯一已验证发布指针。

## 已发现的生产链路问题

原 R14 manifest 的 variant `path` 曾记录为 `.bin`，而 dist 物理文件是 `.png`；R14.1 已修正为 `.png`。resolver 当前生成 `.png` URL，后续必须由 release gate 持续验证两者一致。

Icon Repository 已将 `release.yml` 固化为 fail-closed V6 release writer，并在主线 CI 中通过 L0-L1；但当前 state snapshot 仍缺少 canonical `ai`，因此 writer 在实际发布时会按设计阻断。`incremental.yml` 仍是 scaffold，因此完整的 acquisition→state→release 生产链尚未端到端闭环。

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