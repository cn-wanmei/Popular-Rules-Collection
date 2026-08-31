# Client Capability Matrix (2026-08-31)

- version: **2** (expected-artifact checks)
- clients: **7** · datasets: **9** · gaps: **19**
- builders present: **7/7**

Legend: `Y`=ok · `c`=cap only · `d`=no export · `i`=invalid · `-`=no capability

| dataset | data | mihomo | sing-box | surge | shadowrocket | quantumult-x | egern | loon |
|---------|------|------|------|------|------|------|------|------|
| service_rules | Y | Y | Y | Y | Y | Y | Y | Y |
| service_ip | Y | Y | Y | Y | Y | Y | Y | Y |
| lan | Y | Y | Y | Y | Y | Y | Y | Y |
| geosite_policy | Y | Y | Y | Y | Y | Y | Y | Y |
| geoip_country | Y | Y | Y | Y | Y | Y | Y | Y |
| geoip_mmdb | Y | Y | Y | - | - | - | - | - |
| provider | Y | Y | Y | Y | Y | Y | Y | Y |
| asn_metadata | Y | - | - | - | - | - | - | - |
| policy | Y | - | - | - | - | - | - | - |

## Gaps

- `geoip_mmdb` × `surge`: **no_capability**
- `geoip_mmdb` × `shadowrocket`: **no_capability**
- `geoip_mmdb` × `quantumult-x`: **no_capability**
- `geoip_mmdb` × `egern`: **no_capability**
- `geoip_mmdb` × `loon`: **no_capability**
- `asn_metadata` × `mihomo`: **no_capability**
- `asn_metadata` × `sing-box`: **no_capability**
- `asn_metadata` × `surge`: **no_capability**
- `asn_metadata` × `shadowrocket`: **no_capability**
- `asn_metadata` × `quantumult-x`: **no_capability**
- `asn_metadata` × `egern`: **no_capability**
- `asn_metadata` × `loon`: **no_capability**
- `policy` × `mihomo`: **no_capability**
- `policy` × `sing-box`: **no_capability**
- `policy` × `surge`: **no_capability**
- `policy` × `shadowrocket`: **no_capability**
- `policy` × `quantumult-x`: **no_capability**
- `policy` × `egern`: **no_capability**
- `policy` × `loon`: **no_capability**
