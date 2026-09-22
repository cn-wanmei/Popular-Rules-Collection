# Client Network Dataset URLs

`Service Rules` and `Network Datasets` are separate semantic layers but are published from the same immutable Release Candidate.

Prefix: `https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/`

## GeoIP

| Artifact | Path |
|---|---|
| Country.mmdb | `generated/mmdb/Country.mmdb` |
| ASN.mmdb | `generated/mmdb/ASN.mmdb` |
| geoip-lite.dat | `generated/mmdb/geoip-lite.dat` |
| geoip.dat | `generated/mmdb/geoip.dat` |
| Country CIDR | `generated/geoip/<country>.txt` |

## ASN

| Artifact | Path |
|---|---|
| ASN.mmdb | `generated/mmdb/ASN.mmdb` |
| Metadata | `generated/asn/metadata.yaml` |

ASN metadata is provider attribution only; it is never Service Identity evidence.

## GeoSite

| Artifact | Path |
|---|---|
| geosite.dat | `generated/mmdb/geosite.dat` |
| text datasets | `generated/geosite/<name>.txt` |
| Mihomo projection | `generated/geosite/<name>_mihomo.list` |

## Network

`generated/network/` contains LAN/private/DNS/NTP/STUN materializations. Network datasets are generated together with the client rule release and are represented in `generated/manifest.json`.

## Provider / Service IP

`generated/provider/` contains provider CIDRs; `generated/ip/` contains explicitly collected service/country/carrier IP sets. Neither provider nor GeoIP data may be interpreted as product ownership.

## Boundary

Service Rules → product-scoped domains/IPs.

Network Datasets → GeoIP/GeoSite/ASN/LAN/provider/policy support data.