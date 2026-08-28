# Client Capability Matrix (2026-08-28)

- clients: **7** · datasets: **9** · gaps: **19**
- service builders present: **7/7**

Legend: `Y` = ok · `c` = capability only · `d` = data no export · `-` = no capability

| dataset | data | mihomo | sing-box | surge | shadowrocket | quantumult-x | egern | loon |
|---------|------|------|------|------|------|------|------|------|
| service_rules | Y | Y | Y | Y | Y | Y | Y | Y |
| service_ip | Y | Y | Y | Y | Y | Y | Y | Y |
| lan | Y | Y | Y | Y | Y | Y | Y | Y |
| geosite | Y | Y | Y | Y | Y | Y | Y | Y |
| geoip_country | Y | Y | Y | Y | Y | Y | Y | Y |
| geoip_mmdb | Y | Y | Y | - | - | - | - | - |
| provider | Y | Y | Y | Y | Y | Y | Y | Y |
| asn | Y | - | - | - | - | - | - | - |
| policy | Y | - | - | - | - | - | - | - |

## Gaps

- `geoip_mmdb` × `surge`: **no_capability**
- `geoip_mmdb` × `shadowrocket`: **no_capability**
- `geoip_mmdb` × `quantumult-x`: **no_capability**
- `geoip_mmdb` × `egern`: **no_capability**
- `geoip_mmdb` × `loon`: **no_capability**
- `asn` × `mihomo`: **no_capability**
- `asn` × `sing-box`: **no_capability**
- `asn` × `surge`: **no_capability**
- `asn` × `shadowrocket`: **no_capability**
- `asn` × `quantumult-x`: **no_capability**
- `asn` × `egern`: **no_capability**
- `asn` × `loon`: **no_capability**
- `policy` × `mihomo`: **no_capability**
- `policy` × `sing-box`: **no_capability**
- `policy` × `surge`: **no_capability**
- `policy` × `shadowrocket`: **no_capability**
- `policy` × `quantumult-x`: **no_capability**
- `policy` × `egern`: **no_capability**
- `policy` × `loon`: **no_capability**
