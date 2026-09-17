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
│   ├── developer/rules.yaml
│   ├── findmy/rules.yaml
│   ├── music/rules.yaml
│   ├── tv/rules.yaml
│   └── ...
├── google/
│   ├── all/rules.yaml
│   ├── gmail/rules.yaml
│   └── ...
└── <provider>/
    ├── all/rules.yaml
    └── <service>/rules.yaml
```

## Semantics

- `<provider>/all` is the provider-wide aggregate and covers all declared services of that provider.
- Every independently addressable service gets its own directory and its own canonical membership.
- `all` is a logical aggregate, not a second hand-maintained copy of service rules.
- Client-specific files belong under `generated/<client>/` and are produced by the engine; they are never edited as canonical sources.
- Flat service files under a provider root are forbidden.

## China aggregate

`rules/china/all` is the domestic China aggregate. Its input universe is the China domain/IP rule universe. Providers explicitly declared as having independent service trees are excluded from this aggregate, so their authoritative rules live in their own provider/service trees. This exclusion is deliberate and is enforced by CI.

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
