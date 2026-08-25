# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

## Pipeline

**Actions → Collect Upstream → Run workflow**

```
collect → normalize → deduplicate → conflict_detector → provenance
       → build×6 → validate → builder_validate → statistics → commit
```

## Hagezi

Registry currently collects **Light + Pro + Ultimate** (`adblock/light|pro|ultimate.txt`).
All feed into the `adblock` service (union). Profiles (minimal/balanced/full) are a later layer.

## Registry V3

`rules: [{path, name, local?}]` — single place to add services. No `SOURCE_FILES` in code.
