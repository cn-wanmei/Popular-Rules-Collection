# 网络数据集使用说明（LAN / GeoIP / GeoSite / ASN / Provider）

> **与 Service 规则严格分离。** 本数据用于路由兜底 / 基础设施，不是淘宝、Google 搜索等产品规则。

总览：[`generated/README.md`](../generated/README.md)

## 类目一览

| 类目 | 配置 | 数据 | 生成 | 策略 |
|------|------|------|------|------|
| LAN/Private/DNS/NTP/STUN | `sources/datasets/network.yaml` | `database/network/` | `generated/network/` | DIRECT |
| GeoIP 国家 | `sources/datasets/geoip.yaml` | `database/geoip/` | `generated/geoip/` | CN→DIRECT 等 |
| GeoSite 策略域名 | `sources/datasets/geosite.yaml` | `database/geosite/` | `generated/geosite/` | direct/proxy/reject |
| Provider 云 IP | `sources/datasets/provider.yaml` | `database/provider/` | `generated/provider/` | 按需，勿绑产品 |
| ASN 元数据 | `sources/datasets/asn.yaml` | `database/asn/metadata.yaml` | — | 仅参考 |
| MMDB | geoip artifact | — | `generated/mmdb/Country.mmdb` | 客户端库 |

## LAN

`database/network/lan.txt`：RFC1918、CGNAT、文档地址、ULA 等 → **必须 DIRECT**。

## GeoIP

上游 Loyalsoldier/geoip。已启用：`cn hk tw jp kr sg us de gb au my in id vn th private` + `Country.mmdb`。

```text
GEOIP,CN,DIRECT
```

## GeoSite

| 集 | 策略 |
|----|------|
| direct / china / apple-cn / google-cn | DIRECT |
| proxy | PROXY |
| reject | REJECT |

`geosite/china` ≠ Service `china`（ChinaMax）。

## Provider

Cloudflare / AWS / Google Cloud / goog / Oracle。**禁止**把 `aws` 整表映射到 Amazon 购物。

## ASN

仅 `database/asn/metadata.yaml` 标注运营商与云厂商，不自动生成规则。

## 推荐顺序

```text
REJECT ← reject / adblock
DIRECT ← lan + private
DIRECT ← geosite-direct / Service china
PROXY  ← Service google/ai… 或 geosite-proxy
GEOIP CN → DIRECT
MATCH → PROXY
```

## 更新

```bash
python scripts/collect_datasets.py
python scripts/collect_providers.py
python scripts/build_network_datasets.py
python scripts/build_provider_datasets.py
```

与 Service `collect.py` 分离。
