# 图标使用说明 — Icon System V5

当前架构：**Icon System V5 / Icon Matrix 8**

## 八层

1. Source Original
2. Glassmorphism
3. Soft 3D / Claymorphism
4. Neo-Skeuomorphism
5. Minimalist Glyph & Multi-color Flat
6. Two-tone / Broken Line
7. MBE Illustration
8. Y2K / Synthwave

## Identity 解析

~~~text
Service ID
   ↓
Icon Registry V5
   ↓
Icon Identity
   ↓
Source Original + 7 Derived Variants
~~~

不要根据服务名猜图标 URL。

优先从 Registry 的 source.source_url 以及对应 variant 的 path 读取。

## Source 原则

来源优先级：

Registered Official → Official Declared → Manifest → Official-Origin Favicon → Reviewed Third-Party → Semantic Fallback

注意：

- 官方网站来源 ≠ 自动获得开放许可证。
- favicon 是 official-origin asset 时，也不能自动声称它就是官方品牌 Logo。
- 第三方品牌资产不得标记为 official。
- 无品牌身份的语义 fallback 不得冒充品牌。

## 八层关系

Source Original 是 identity source。

其它七层：

derived_from(source_digest)

不会生成新的 icon_identity。

## Coverage

V5 的正式覆盖口径为 current_run_service_ids，而不是固定写死某一个历史数量。

每个 service：

8 / 8

缺失任何一层：

release = blocked

同时检查：

service → icon

和：

icon → active service

## Run / Lineage

V5 必须绑定：

- run_id
- snapshot_id
- ir_digest
- source_digest
- renderer_version

Source digest 与 Rule digest 分离。

## 客户端

客户端通过 preferred_style 选择视觉层，不重新抓取图标，不改变 Icon Identity。

## 历史版本

V3/V4/Legacy 仅作为历史兼容和回滚依据。

V5 active 后，新的 service icon 只进入 V5。
