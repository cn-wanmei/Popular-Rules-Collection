# 策略 / 网络类图标

策略与网络数据集 **不使用品牌 Logo**，统一使用本仓库几何图标（`status: verified`，CC0-1.0）。

| icon_key | 用途 | 推荐策略语境 |
|----------|------|----------------|
| `direct` | 直连 | LAN / China / 国内媒体 |
| `proxy` | 代理 | 海外 Service |
| `reject` | 拒绝 | 广告 / 部分 restricted |
| `dns` | DNS | DNS 相关规则 |
| `lan` | 局域网 | RFC1918 等 |
| `china` | 国内汇总 | China Domain / CIDR |
| `geoip` | GeoIP | 国家库 |
| `geosite` | GeoSite | 分类域名库 |
| `asn` | ASN | ASN 元数据 / MMDB |
| `global` | 全球 | 兜底 |
| `placeholder` | 占位 | 尚无品牌图的服务 |

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/256/direct.png
```

Service 品牌图标见 [ICON_REGISTRY.md](./ICON_REGISTRY.md)；规则页由 `generate_rule_pages.py` 自动挂载。
