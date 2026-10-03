# Security Policy

> **Status: Current**  
> Popular-Rules-Collection is the identity / rule / client publish authority in the Popular Rules ecosystem.

## Reporting

Report security issues via GitHub private vulnerability reporting or the repository owner. Do not open public issues for credential or supply-chain exploits.

## Controls

| Topic | Policy |
|-------|--------|
| Actions permissions | Per-job minimum; no blanket write on read-only gates |
| Action versions | Full SHA pin — see `docs/ACTIONS_SHA_PIN.md` |
| Dependencies | Locked installs where CI builds run (`requirements.lock` when present) |
| Immutable artifacts | Build Run ID + Head SHA bind Release Candidates; Publish is fail-closed |
| Cross-repo trust | Source handoff is Collection-owned; no cross-repo Secrets |
| Secrets | Actions Secrets only; never commit tokens |
| Release integrity | Manifest digests; user GitHub Releases are manual `workflow_dispatch` only |

## Related

- Source: [Popular-Rules-Source/docs/SECURITY.md](https://github.com/cn-wanmei/Popular-Rules-Source/blob/main/docs/SECURITY.md)
- Icon: consumer of Collection identity; same pin table
