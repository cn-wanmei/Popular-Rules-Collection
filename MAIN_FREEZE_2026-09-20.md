# Main Freeze — 2026-09-20

## Freeze Scope

Production main is frozen during Phase 2.

Automated writers disabled:

- Collect → main
- Publish → main
- Generated Status → main
- Icon optimizer → main
- Retention apply

Read-only validation/test workflows may continue.

## Reason

The production tree was receiving frequent automated commits while the Source layer was being re-audited. Phase 2 requires a stable comparison baseline.

## Phase 2 Rule

All new implementation must land through:

~~~text
phase2/* branch
   ↓
Pull Request
   ↓
CI / Gate
   ↓
Review
   ↓
main
~~~

No direct production mutation.

## Important limitation

The connected GitHub integration can read repository administration metadata but cannot write branch-protection/ruleset settings through the available interface. Therefore this freeze stops repository automation writers, but the GitHub UI must still enforce:

- Require pull request
- Require required status checks
- Disable force push
- Disable deletion
- Require linear history where desired

Until those repository rules are enabled, a human with direct push permission could still bypass the soft freeze.

## Unfreeze

Do not restore automated writers until Phase 2 passes the activation checklist.
