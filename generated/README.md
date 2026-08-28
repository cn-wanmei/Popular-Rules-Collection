# generated/ 客户端规则总览

本目录是 **可直接订阅的规则产物**。请按客户端进入子目录 README，避免在仓库里盲目搜索文件名。

## 按客户端进入

| 客户端 | 目录 | 说明文档 |
|--------|------|----------|
| Mihomo / Clash Meta | [`mihomo/`](./mihomo/) | [使用说明](./mihomo/README.md) |
| sing-box | [`sing-box/`](./sing-box/) | [使用说明](./sing-box/README.md) |
| Surge | [`surge/`](./surge/) | [使用说明](./surge/README.md) |
| Shadowrocket | [`shadowrocket/`](./shadowrocket/) | [使用说明](./shadowrocket/README.md) |
| Quantumult X | [`quantumult-x/`](./quantumult-x/) | [使用说明](./quantumult-x/README.md) |
| Egern | [`egern/`](./egern/) | [使用说明](./egern/README.md) |
| Loon | [`loon/`](./loon/) | [使用说明](./loon/README.md) |

## 网络 / 基础设施（非业务服务）

| 目录 | 内容 |
|------|------|
| [`geoip/`](./geoip/) | 国家/地区 CIDR |
| [`geosite/`](./geosite/) | 策略 geosite |
| [`network/`](./network/) | LAN / DNS / NTP |
| [`provider/`](./provider/) | 云厂商 IP 段（≠ 电商） |

## 热门规则直链（Mihomo）

| ID | 策略 | Raw |
|----|------|-----|
| china | DIRECT | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/china.yaml |
| google | PROXY | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google.yaml |
| youtube | PROXY | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/youtube.yaml |
| ai | PROXY | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ai.yaml |
| apple | 按需 | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple.yaml |
| telegram | PROXY | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/telegram.yaml |
| github | PROXY | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/github.yaml |
| adblock-light | REJECT | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/adblock-light.yaml |
| restricted | PROXY | https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/restricted.yaml |

## 文档

- [USAGE.md](../docs/USAGE.md)
- [docs/rules/](../docs/rules/README.md) — 每服务一页含全客户端链接
- [`subscription_links.json`](./subscription_links.json)

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/<client>/<service_id>.<ext>
```
