# Universal Rule Schema V2+

## Registry (`sources/registry.yaml`) = Source + Fetcher + Manifest

```yaml
sources:
  - id: blackmatrix7
    fetch:
      type: github_raw
      owner: blackmatrix7
      repo: ios_rule_script
      branch: master
    rules:
      - path: rule/Clash/OpenAI/OpenAI.yaml
        name: openai          # canonical service id
        local: Clash_OpenAI.yaml  # optional local backup name
```

Adding a service = edit **only** `registry.yaml` (not collect.py / normalize.py).

## Service document (`database/services/{id}.yaml`)

```yaml
id: google
name: Google
category: service
policy:
  default: proxy   # proxy | direct | reject
source:
  - id: loyalsoldier
    priority: 98
rules:
  - type: domain_suffix
    value: google.com
```

## Conflict model

| Kind | Meaning |
|------|---------|
| CRITICAL | same match, **different policy** |
| HIGH | parent/child domain, opposing policy |
| MEDIUM | domain vs domain_suffix same value |
| LOW | multi-source same match+policy (duplicate) |

## Pipeline roles

| Script | Mutates DB? | Output |
|--------|-------------|--------|
| deduplicate.py | yes → canonical + domains/ips | database/canonical/ |
| conflict_detector.py | no | reports/.../conflicts/ |
| provenance.py | provenance only | database/provenance/ |
| builder_validate.py | no | reports/.../builder-validation.json |
| statistics.py | no | reports/.../statistics.json |
