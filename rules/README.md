# Canonical rule directory

This tree is the source-of-truth layout for service rules.

```text
rules/
├── china/
│   └── all/
│       └── rules.yaml
├── apple/
│   ├── all/rules.yaml
│   ├── appstore/rules.yaml
│   ├── testflight/rules.yaml
│   ├── appledev/rules.yaml
│   ├── findmy/rules.yaml
│   ├── applemusic/rules.yaml
│   ├── appletv/rules.yaml
│   └── ...
├── google/
│   ├── all/rules.yaml
│   ├── gmail/rules.yaml
│   └── ...
└── <provider>/
    ├── all/rules.yaml
    └── <service-id>/rules.yaml
```

## Semantics

- `<provider>/all` is the provider-wide aggregate and covers all declared services of that provider.
- Every independently addressable service gets its own directory and its own canonical membership.
- Service directory names use stable service IDs; display names are metadata, not paths.
- `all` is a logical aggregate generated from canonical memberships; it is not a second hand-maintained service source.
- Client-specific files belong under `generated/<client>/` and are produced by the engine; they are never edited as canonical sources.
- Flat service files under a provider root are forbidden.

## China aggregate

`rules/china/all` is the domestic China aggregate. Its input universe is the complete China domain/IP rule universe. Providers explicitly declared as independent service trees are excluded from this aggregate, so their authoritative rules live in their own provider/service trees. China itself has **no** `alibaba/`, `tencent/`, `baidu/`, `jd/`, `meituan/` or other independent-service subdirectories.

The initial independent-provider exclusion set is:

- Alibaba
- Tencent
- Baidu
- JD
- Meituan
- ByteDance
- NetEase
- Huawei
- Xiaomi
- OPPO
- vivo

The exclusion list is configuration, not filename convention. A service is never included or excluded merely because its name happens to contain a provider name.

## Materialization rule

No 100–200 service backfill is performed in this directory-contract phase. New services are added only after the directory contract, generator, and CI gates pass review. Each new service then receives `rules/<provider>/<service-id>/` and a corresponding generated client tree.

> Phase 8 note: `rules/` is a reserved future canonical-rule layout. The active V1 Canonical Service Model is currently rooted at `rule/`. `database/services/` is Legacy Source and `generated/` is distribution output.
