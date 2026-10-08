# Cross-repo identity dispatch setup

Collection workflow `.github/workflows/notify-icon-identity.yml` fires when `rule/_index.yaml` changes.

## Required secret (Collection repo)

| Name | Scope | Purpose |
|------|--------|---------|
| `ICON_DISPATCH_TOKEN` | PAT or GitHub App token | `repository_dispatch` on `cn-wanmei/Popular-Rules-Icon` |

### Token permissions

- `repo` (or fine-grained: Actions write + Contents read on Icon)
- Target event: `collection-identity-changed` (handled by Icon `identity-freshness.yml`)

### Without secret

Workflow exits 0 and logs skip. Icon still runs daily schedule freshness.

### Verify

```bash
gh secret set ICON_DISPATCH_TOKEN --repo cn-wanmei/Popular-Rules-Collection
# then touch rule/_index.yaml on main or workflow_dispatch notify job
```
