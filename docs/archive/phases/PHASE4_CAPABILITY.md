# Phase 4 — Client Capability Matrix

Separates three questions:

| Question | Field |
|----------|--------|
| Client *supports* this data kind? | `capability` |
| Source data present? | `data_available` |
| Exported under `generated/`? | `export` |

Gap codes: `none` · `no_capability` · `no_data` · `no_export`

## Files

- `config/client_capabilities.yaml`
- `scripts/client_capability_matrix.py`
- `reports/<date>/client_capability.json` · `.md`

## Non-goals

- No Builder rewrite
- Not every dataset × all 7 clients
- Policy/DNS capability stays false until Policy Layer deepens
