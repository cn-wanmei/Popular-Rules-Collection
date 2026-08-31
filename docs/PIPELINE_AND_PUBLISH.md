# Pipeline & Publish (V2.6)

```bash
python scripts/pipeline.py preflight
python scripts/pipeline.py all
make pipeline
```

Publish lane: `concurrency.group: main-publish` on collect + build.  
Never `git pull --rebase || true` then push.

Size gate SSOT: `config/artifact_layout.yaml` → `max_tracked_tree_mb`.  
Builders: `config/builder_registry.yaml`.
