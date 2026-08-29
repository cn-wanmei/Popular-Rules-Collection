# Icon P2 详细规划与落地状态

## 落地状态（2026-08-30）

| ID | 状态 |
|----|------|
| P2.3 | ✅ SI `upstream_version` + `retrieved_at` |
| P2.5 | ✅ `assets/icons/official/` + `icon_import_official.py` |
| P2.1 | ✅ theme roles `dark→monochrome`（approved_mono） |
| P2.4 | ✅ `metadata/qa.yaml` level warn\|hard |
| P2.2 | ✅ dual-write strategies/datasets；legacy `png/` primary；brands 需 `P2_DUAL_BRANDS=1` |

```bash
python scripts/icon_p2_apply.py
python scripts/icon_qa.py
```

## 原则

- 不猜 Logo、不 bulk 造 dark/light PNG
- 旧 URL 不打断
- SI 不标 verified
