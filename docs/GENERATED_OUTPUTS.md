# Generated Output Contract

## Two production output classes

### 1. Service Rule Projections

`generated/<client>/...` contains V3-compiled rules for Mihomo, sing-box, Surge, Shadowrocket, Quantumult X, Egern and Loon.

These files are projections of Semantic IR. They are not canonical authoring files.

### 2. Network Dataset Distribution

`generated/<scope>/...` contains companion datasets used by clients for routing and network classification.

| Scope | Meaning |
|---|---|
| `network` | LAN, private, DNS, NTP, STUN and other network primitives |
| `geosite` | Domain classification datasets |
| `geoip` | Country/region CIDR datasets |
| `provider` | Provider CIDR datasets |
| `asn` | ASN/provider attribution metadata |
| `ip` | Service IP datasets after Collection audit |
| `policies` | Dataset-level routing policy compositions |
| `mmdb` | MMDB / DAT binary artifacts |

These are not Service Identity evidence. Provider CIDR, ASN metadata, GeoIP ranges and generic Geosite lists must not be used to claim product ownership.

## One release, one inventory

Every Release Candidate must contain:

- `generated/manifest.json` — complete file inventory.
- `generated/network_manifest.json` — Network Dataset provenance and input mapping.
- Seven configured client output trees.
- All required Network Dataset scopes.

The same generated tree is the input to atomic publish. This removes the former failure mode where a legacy network script produced files that were not part of the V3 release candidate.

## Why `generated/` and `rule/` differ

They represent different layers:

    rule/                 legacy V1 model
            ↓
    V3 migration / Canonical
            ↓
    Semantic IR
            ↓
    generated/<client>/   client-specific compiled rules

Therefore file names, grouping, aggregates and syntax can differ.

## Reproducibility

Network generation is deliberately a pure materialization step: it reads committed `database/` inputs and performs no network access. Refresh happens in Collect; publication happens in Build/Publish. The same Collection commit therefore produces the same Network Dataset tree.