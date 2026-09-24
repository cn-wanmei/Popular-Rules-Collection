# 图标库 — Current Icon System 3

## SSOT

当前入口：`assets/icons/v3/release-pointer.json` → 不可变 Release `2026.09.22-5e0e48ad55c6`。Release 内含 manifest、QA/Gate 证据和 7 个客户端 index。

## 服务页

服务说明页使用 service_id → icon identity 的显式绑定，页面记录 identity、role、style、path、digest，不猜测 Logo。

## 语义边界

- brand：服务品牌身份
- strategy：DIRECT / PROXY / REJECT 等策略语义
- dataset / network：China / GeoIP / ASN / LAN 等数据语义
- placeholder：没有独立且已验证品牌身份时的显式占位

Legacy `assets/icons/manifest.yaml`、`registry.yaml`、旧 profiles 与旧 PNG 路径继续作为兼容/历史资产，不代表当前 V3 发布状态。