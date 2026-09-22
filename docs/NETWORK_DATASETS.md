# Network Datasets

Network Dataset is a first-class companion output of the Collection Release Candidate. It is not a substitute for Service Canonical or Source Evidence.

## Inputs

Collectors refresh committed inputs under `database/` from the registries in `sources/datasets/` and `sources/ip_registry.yaml`.

Build never performs network access for these datasets. `scripts/build_network_bundle.py` materializes only from the collected repository state.

## Output

`generated/` always contains the Network Dataset scopes in the same release tree as the client rules when the required inputs are present:

- `network/` — LAN, private, DNS, NTP and STUN.
- `geosite/` — direct/proxy/reject/china and other configured domain classes.
- `geoip/` — country/region CIDRs.
- `provider/` — provider CIDRs.
- `asn/` — curated ASN metadata.
- `ip/` — audited service IP sets.
- `policies/` — dataset policy manifests.
- `mmdb/` — MMDB/DAT binary distribution.

`network_manifest.json` records the input path, output path, SHA-256 and byte/line counts for every materialized artifact.

## Semantics

Network data is intentionally separate from Service Identity:

`ASN → provider attribution only`

`Provider CIDR → provider infrastructure only`

`GeoIP → geographic addressing only`

`Geosite → domain classification only`

`Service IP → only after explicit Collection ownership audit`

None of the above may be promoted into a Service rule merely because a hostname or CIDR appears in the dataset.

## Former intermittent generation bug

Previously, `collect_datasets.py`, `collect_ip.py`, `collect_providers.py`, `build_network_datasets.py` and `build_network_lan.py` were outside the V3 build DAG. Their outputs could therefore be absent after a clean publish.

Now:

    Collect
      ↓
    database/
      ↓
    build_network_bundle.py
      ↓
    release-candidate/generated/
      ↓
    generated/manifest.json
      ↓
    atomic publish

Missing required network scope is a Release Publish failure, not a silent omission.