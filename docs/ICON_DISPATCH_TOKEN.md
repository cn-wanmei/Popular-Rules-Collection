# Cross-repo identity dispatch setup

The Icon identity snapshot is immutable when its content matches the current Collection index. A Publish run does **not** need a cross-repository token when the existing Icon snapshot already matches.

## Required secret (only when synchronization is needed)

Configure a fine-grained PAT or GitHub App token named \`ICON_DISPATCH_TOKEN\`:

- In **Popular-Rules-Collection** repository secrets: permits \`repository_dispatch\` to \`cn-wanmei/Popular-Rules-Icon\`.
- In **Popular-Rules-Icon** repository secrets: permits the Identity Freshness workflow to create/push its snapshot branch and open a pull request.

Target repository permissions on Icon:
- Contents: read and write
- Pull requests: read and write
- Actions: read/write only if required by the selected dispatch integration

The Collection Publish preflight first compares the live Icon pin with the exact current Collection index. It only needs the token when a mismatch must be dispatched for repair. If the pin already matches, Publish proceeds without a needless token smoke-test.

## If the token is unavailable

- A matching Icon pin can still pass Publish's identity preflight.
- If the pin is stale, Collection refuses promotion until identity is synchronized.
- Collection's push notification workflow and Icon's drift-remediation job report the missing credential; scheduled Identity Freshness comparisons still run, but cannot create/merge a repair PR without the Icon-side credential.

## Verify

After configuring the secret in both repositories, trigger the Icon Identity Freshness workflow and confirm that its latest run succeeds with \`drift=false\` and \`content_match=true\`.
