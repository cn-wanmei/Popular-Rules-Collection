# 客户端 Network Dataset 稳定入口

> **Service Rules** 与 **Network Datasets** 双轨分离。  
> 优先使用本仓库 URL，避免直接依赖上游 `latest`。

前缀：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/`

## GeoIP

| 产物 | 路径 |
|------|------|
| Country.mmdb | `generated/mmdb/Country.mmdb` |
| geoip-lite.dat | `generated/mmdb/geoip-lite.dat` |
| geoip.dat | `generated/mmdb/geoip.dat` |
| 国家 CIDR | `generated/geoip/cn.txt` 等 |

```yaml
# Egern
geoip_db_url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mmdb/Country.mmdb"

# Mihomo
geoip-url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mmdb/geoip-lite.dat"
```

## ASN

| 产物 | 路径 |
|------|------|
| ASN.mmdb | `generated/mmdb/ASN.mmdb`（CI `collect_datasets` 镜像） |
| 元数据 | `database/asn/metadata.yaml`（不可作 rule-set） |

```yaml
asn_db_url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mmdb/ASN.mmdb"
```

## GeoSite

| 产物 | 路径 |
|------|------|
| geosite.dat | `generated/mmdb/geosite.dat` |
| direct/proxy 文本 | `generated/geosite/*.txt` |

```yaml
geosite-url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mmdb/geosite.dat"
```

GeoSite ≠ Service Registry。

## LAN

`generated/network/lan_mihomo.list` → **DIRECT**

## 边界

Service Rules → 产品域名/IP；Network Datasets → GeoIP/GeoSite/ASN/LAN；Provider ≠ Service。
