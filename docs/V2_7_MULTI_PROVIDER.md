# V2.7 Multi-Provider

8 aggregates: google apple microsoft tencent alibaba baidu amazon bytedance.

Core = legacy `database/services/{id}.yaml`; exclusives candidate-only.

```bash
python scripts/hierarchy_validate.py
python scripts/resolve_hierarchy.py
python scripts/hierarchy_golden.py
python scripts/hierarchy_coverage.py
```
