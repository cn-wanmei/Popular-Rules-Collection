# Universal Rule Schema V2

See project README for architecture.

Service documents live in `database/services/`.
Large domain aggregates live in `database/domains/` and `database/ips/`.

Conflict levels: CRITICAL / HIGH / MEDIUM / LOW.
Empty-rule protection: collectors must not overwrite good data with empty bodies.
