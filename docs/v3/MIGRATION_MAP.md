# Migration Map

| Legacy | Target | Status |
|--------|--------|--------|
| scripts/collect.py | src/fetch | legacy |
| scripts/normalize.py | src/normalize | legacy |
| scripts/hierarchy_*.py | src/hierarchy | legacy |
| scripts/build_mihomo.py | src/adapters/mihomo | legacy |
| scripts/pipeline.py | CLI entry | active |

V3+: new core logic in src/; scripts = CLI/shim only.
