# Routing Capability Boundaries

本仓库输出**逻辑规则**（domain / IP / 策略意图）。客户端按自身能力匹配。

## IPv4 / IPv6

| 类 | IPv4 | IPv6 | 路径 |
|----|------|------|------|
| LAN / private / reserved | ✅ RFC1918 等 | ✅ `::1` `fc00::/7` `fe80::/10` 等 | `database/network/lan.txt` `private.txt` |
| GeoIP CN | 视上游 | 视上游 | `database/geoip/` / mmdb |

System 层直连应对称，避免 v4/v6 动作不一致。

## 匹配维度

| 维度 | 仓库 | 说明 |
|------|------|------|
| Domain | ✅ | 主路径 |
| IP/CIDR | ✅ | GeoIP、LAN、provider |
| SNI/Host | ❌ DPI | 客户端可用同一域名规则 |
| QUIC/UDP | ❌ 不拆协议文件 | 规则默认协议无关 |

## DNS

见 `config/resolution_policy.yaml`。DNS 不是 DIRECT/PROXY 同级动作。
