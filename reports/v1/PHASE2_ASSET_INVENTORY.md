# V1 Phase 2 — Legacy Asset Inventory

> Status: Phase 2 execution baseline
>
> This document records the first repository-backed inventory pass. It is intentionally an audit artifact, not a migration approval.

## 1. Repository evidence

The repository currently contains a legacy `rule/` tree with ecosystem/service directories such as `AI`, `Alibaba`, `Amazon`, `Apple`, `Baidu`, `ByteDance`, `China`, `Developer`, `Finance`, `Gaming`, `Google`, and `12306`. The complete tree must be treated as legacy source inventory until each asset is mapped to a V1 Service Entity.

The `docs/rules/` tree also contains a large flat documentation catalog, including `12306.md`, `abc.md`, `acfun.md`, `adblock*.md`, `adobe.md`, `ai.md`, `airbnb.md`, `aisuite.md`, `akamai.md`, `alibaba.md`, and many additional rule descriptions.

The V3 source tree already separates canonical, ingest, hierarchy, IR, adapters, diff, golden, and release concerns. `src/engine/canonical/store.py` currently emits a canonical rule store with `rules.jsonl`, `memberships.jsonl`, `errors.jsonl`, and `manifest.json`.

## 2. Initial findings

### 2.1 Legacy service hierarchy exists

Google is already represented as a multi-level legacy ecosystem:

```text
rule/Google/
├── Google/
├── YouTube/
├── YouTubeMusic/
├── Firebase/
└── GoogleFCM/
```

The legacy Google aggregate metadata declares `google` as an aggregate with children `youtube`, `googlefcm`, `googledrive`, `firebase`, and `gcp` and reports 1,093 domains plus 5 IPv4/CIDR entries. This proves that the historical repository already contains Parent/Child/Aggregate semantics, although they are encoded through legacy metadata rather than the V1 Service schema.

### 2.2 Legacy metadata is useful migration evidence, not V1 schema

Existing `metadata.yaml` files contain fields such as:

- `id`
- `name`
- `primary_category`
- `categories`
- `service_type`
- `parent`
- `children`
- `rule.has_domain`
- `rule.has_ip`
- `generated_files`
- `statistics`
- `sources`
- `clients`
- `updated_at`
- `auto_generated`

These fields should be imported into the migration inventory where applicable, but must not be treated as the final V1 contract.

### 2.3 Legacy rule files are already multi-format

A Google aggregate currently contains:

- `google.list`
- `google_domain.list`
- `google_ip.list`
- `metadata.yaml`
- documentation

A Google YouTube child similarly contains mixed/domain/IP outputs. Therefore the migration must identify the canonical semantic assets beneath generated/legacy formats instead of simply copying `.list` files into V1.

## 3. V1 mapping rules

Every discovered legacy entity must be assigned one of:

1. `service`
2. `parent-service`
3. `child-service`
4. `shared-component`
5. `category`
6. `aggregate`
7. `network-dataset`
8. `legacy-unknown`
9. `deprecated`
10. `duplicate`

No legacy path is deleted during Phase 2.

## 4. Google migration seed

The current V1 bootstrap should be reconciled with the actual legacy inventory before expanding the child list.

Confirmed legacy Google children observed in the repository:

```text
Google
YouTube
YouTubeMusic
Firebase
GoogleFCM
```

The legacy metadata additionally references:

```text
Google Drive
GCP
```

Those references require asset-level verification before becoming V1 Child Services.

## 5. Important discrepancy found

The V1 design currently uses:

```text
rule/service/google/
```

while the legacy repository uses:

```text
rule/Google/Google/
```

This is expected and should be handled by an explicit migration mapping rather than by renaming legacy files in place.

## 6. Phase 2 next actions

- Enumerate every first-level legacy `rule/` directory.
- Recursively enumerate all rule files and metadata.
- Enumerate every `docs/rules/*.md` entry.
- Parse legacy metadata into an inventory table.
- Extract service IDs and parent/child relationships.
- Extract category memberships.
- Extract generated-file relationships.
- Identify aggregate rules.
- Identify IP/CIDR-bearing rules.
- Identify possible shared infrastructure.
- Compare legacy memberships against V3 canonical memberships.
- Produce `SERVICE_CATALOG` only after the inventory is complete.
- Produce a separate coverage matrix and conflict report.

## 7. Non-goals in this phase

Phase 2 does not:

- delete legacy rules;
- replace generated artifacts;
- invent missing domains;
- declare a service complete because a legacy directory exists;
- classify provider/ASN infrastructure as a commercial service without evidence;
- make policy decisions;
- change client strategy semantics.
