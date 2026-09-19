# Phase L — Canonical Contract Freeze

Phase L freezes the physical Canonical target without activating it.

## Authoritative target

- Runtime root before cutover: `rule/`
- Canonical root after cutover: `rules/`
- Provider aggregate: `rules/{provider}/all`
- Service: `rules/{provider}/{service}`
- China aggregate: `rules/china/all`
- Rule file: `rules/{scope}/rules.yaml`

The authoritative policy files are `config/service_model/directories.yaml` and `config/canonical_root_migration.yaml`.

## Historical design

`docs/V1_MODEL_DEVELOPMENT_PLAN.md` contains an earlier physical sketch using `rule/category/`, `rule/service/`, and `rule/shared/`. That sketch is historical and must not override the frozen physical target.

## Freeze boundary

This phase does not populate `rules/`, switch the loader, delete `rule/`, or authorize retirement. Those are separate gated operations in Phases M–O.
