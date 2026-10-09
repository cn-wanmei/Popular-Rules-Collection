# Architecture — Compatibility Entry

> **Non-authoritative alias.** Canonical architecture document:
> [`ARCHITECTURE.md`](ARCHITECTURE.md)
>
> This file exists so older links that used a lowercase path still resolve.
> Prefer linking to `ARCHITECTURE.md` in all new documentation.
>
> Renamed from `architecture.md` (2026-10-09) to avoid case-only path
> conflicts on case-insensitive filesystems (Windows / macOS default).

```text
Upstream
  ↓
Collect → immutable backup/<date>
  ↓
V3 Engine
  ↓
Canonical → Semantic IR
  ├── rule/               human browse / service selection
  └── generated/          client + Network Dataset
  ↓
Deterministic Release Candidate → Atomic Publish
```

Current rule index: `rule/_index.yaml`  
Client distribution manifest: `generated/manifest.json`
