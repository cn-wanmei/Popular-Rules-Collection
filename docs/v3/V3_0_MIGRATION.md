# V3.0 Builder Migration

7 builders live in `src/adapters/*/build.py`. `scripts/build_*.py` are shims.
`rule_loader` → `src/adapters/_common/rule_loader.py`.
Output paths unchanged. Canonical Store / full scripts move still phased.
