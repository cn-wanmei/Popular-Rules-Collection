# 图标使用说明（Current V3 SSOT）

`assets/icons/v3/release-pointer.json` 是当前生产 Icon System 3 入口，指向不可变 release；release 内含完整 `manifest.json`、QA / Gate 证据和 7 个客户端 index。

准确图标 URL 与 digest 必须从对应 client index 获取，不得根据旧目录猜路径。

旧 `assets/icons/manifest.yaml`、`assets/icons/registry.yaml` 等仅用于兼容/历史追踪，不代表当前 V3 发布状态。

硬约束：
1. service_id → icon identity 显式绑定。
2. stable release 具备 source / provenance / license。
3. strategy / network / dataset 图标不得冒充品牌 Logo。
4. Builder 不得猜测 Logo。
5. 当前生产图标必须通过 Icon System 3 Gate / QA。