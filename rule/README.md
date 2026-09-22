# Rule Browse Distribution

This directory is a **generated, human-facing release tree** for browsing, searching and selecting rules.

It is produced from the same immutable Semantic IR Run as `generated/`:

```text
data/runs/<run>/canonical
        ↓
data/runs/<run>/ir
        ├──→ rule/
        └──→ generated/
```

`rule/` is client-neutral and is never used as V3 Engine input. Do not hand-edit its rule files. Build and Publish replace `rule/` and `generated/` together; rollback restores both from the same Run.

The first post-cutover Build will replace this bootstrap metadata with the current Run-derived rule tree.