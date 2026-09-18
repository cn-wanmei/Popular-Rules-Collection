# Phase 8 P0 — Intentional Orphan Cleanup

## Result

| Metric | Before | After |
|--------|--------|-------|
| registered | 184 | 218 |
| intentional orphans | 37 | **0** |
| Coverage | 100% (of 184) | **100%** (of 218) |
| Fake domains added | — | **0** |

## Decisions

### B — Remove from intentional (not in V1 catalogue)

| id | reason |
|----|--------|
| `applications` | generic_bucket_not_in_v1_catalogue |
| `lan` | local_network_not_in_v1_catalogue |
| `ntp` | protocol_service_not_in_v1_catalogue |

### A — Register in `_index.yaml` + keep intentional (domains=0, ips=0, path="")

No `.list` files and **no fake domains**. Coverage credit comes from intentional codes only.

| id | category | intentional code |
|----|----------|------------------|
| amazonaws | amazon | COVERED_BY_AGGREGATE |
| baidumap / baidupan | baidu | COVERED_BY_AGGREGATE |
| googledrive / googlemaps / gcp | google | COVERED_BY_AGGREGATE / NO_UPSTREAM |
| jdfinance | jingdong | COVERED_BY_AGGREGATE |
| qq / tencentmeeting / wecom / yuanbao | tencent | mixed |
| quickpass | unionpay | COVERED_BY_AGGREGATE |
| siri | apple | COVERED_BY_AGGREGATE |
| steamcn / blizzard / origin | gaming | COVERED_BY_AGGREGATE / MAPS_TO |
| temu | other | COVERED_BY_AGGREGATE |
| aliexpress | alibaba | NO_UPSTREAM |
| asana / npm / pypi / supabase | developer | NO_UPSTREAM |
| kimi / midjourney / mistral / qwen | ai | NO_UPSTREAM |
| crunchyroll / discoveryplus | streaming | NO_UPSTREAM |
| + etsy, expedia, lyft, revolut, bosszhipin, wenxiaoyan | … | NO_UPSTREAM / COVERED_BY_AGGREGATE |

### C — Rename

None (no case mismatch between intentional keys and index ids).

## Next

1. Phase 7 unexplained_removed gate  
2. Phase 3.2 graph acyclic  
3. Phase 4 golden  
4. Only then `switch_sot_to_v1`
