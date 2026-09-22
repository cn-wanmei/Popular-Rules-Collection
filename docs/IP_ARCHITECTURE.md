# IP Architecture

IP data is a separate evidence scope from Service Domain Identity.

| Scope | Meaning | Service rule eligibility |
|---|---|---|
| `service` | Addresses verified as belonging only to that product | Yes, after ownership proof |
| `provider` | Cloud/CDN/operator infrastructure | No |
| `country` | Geographic aggregate | No direct service attribution |
| `carrier` | ISP/carrier ranges | Dedicated carrier scope only |
| `infrastructure` | DNS/STUN/NTP/private ranges | Dedicated infrastructure scope only |

## Pipeline

    sources/ip_registry.yaml
        ↓
    validate_ip_registry
        ↓
    collect_ip
        ↓
    database/ips + provenance
        ↓
    build_network_bundle
        ↓
    generated/ip
        ↓
    generated/manifest.json
        ↓
    immutable Release Candidate

## Important distinction

`generated/geoip` is geographic address space.

`generated/provider` is provider infrastructure.

`generated/asn` is provider attribution metadata.

`generated/ip` contains only IP sets that Collection explicitly accepts under its IP ownership/scope rules.

ASN → Provider and Provider CIDR → Service are forbidden inferences.