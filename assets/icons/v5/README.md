# PRC Icon Library V5

状态：**Bootstrap / Candidate**

V5 是全新的 8-layer Icon Matrix：

1. Source Original
2. Glassmorphism
3. Soft 3D / Claymorphism
4. Neo-Skeuomorphism
5. Minimalist Glyph & Multi-color Flat
6. Two-tone / Broken Line
7. MBE Illustration
8. Y2K / Synthwave

## 身份模型

service_id → one Icon Identity

七个视觉风格都从同一个 Source Snapshot 派生。

## 数据边界

当前 bootstrap 阶段从 rule/_index.yaml 读取 service entities，仅用于初始化覆盖发现。

正式 production run 必须绑定 same Run / Snapshot / IR，并记录：

run_id + snapshot_id + ir_digest + source_digest + renderer_version

## Active / Historical

V5 成为 active library 后：

- v5/ = active
- v4/ = historical compatibility
- v3/ = historical compatibility
- legacy = historical compatibility

## Acquisition

官方源优先：

registered official → official declared icon → manifest → official favicon → reviewed third-party → semantic fallback

官方来源不自动等同于开放许可证；Registry 必须保留 rights / redistribution 状态。

## Build

~~~bash
python scripts/icon_system_v5.py contract
python scripts/icon_system_v5.py discover --rule-index rule/_index.yaml --out build/icon-v5/service-discovery.json
python scripts/icon_system_v5.py build --rule-index rule/_index.yaml --out build/icon-v5 --strict
python scripts/icon_system_v5.py gate --registry build/icon-v5/registry.json --strict
~~~

在完整 acquisition 未执行完成前，不得把 V5 标记为 100% release。
