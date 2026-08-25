# BlackMatrix7 `rule/Clash/` Candidate Gap Report

**Scan date:** 2026-08-25  
**Upstream:** https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash  
**Status:** Candidate only — **NOT** imported into Registry.

| Metric | Count |
|--------|------:|
| Clash top-level dirs | 668 |
| Already covered (or alias) | 17 |
| Meta/aggregate (skip or special) | ~21 |
| Remaining candidates | ~630 |

## Already covered (do not re-add)

Apple, BiliBili, China (+ ChinaIPs/ChinaMax aliases), Discord, Disney, GitHub, Google, Microsoft, Netflix, OpenAI, Steam, Telegram, TikTok, Twitter, YouTube

## Recommended next batch (P1) — pick 5–10 after review

| Dir | Category | Policy | ~Size | ~Rules |
|-----|----------|--------|------:|-------:|
| Claude | ai | proxy | 265 | 3 |
| Gemini | ai | proxy | 666 | 13 |
| Copilot | ai | proxy | 1991 | 51 |
| Spotify | streaming | proxy | 1317 | 30 |
| Twitch | streaming | proxy | 882 | 22 |
| HBO | streaming | proxy | 1928 | 48 |
| Whatsapp | social | proxy | 708 | 17 |
| Instagram | social | proxy | 312 | 4 |
| Facebook | social | proxy | 19424 | 570 |
| Reddit | social | proxy | 467 | 8 |
| Developer | developer | proxy | 2614 | 70 |
| GitLab | developer | proxy | 383 | 6 |
| Cloudflare | developer | proxy | 2303 | 65 |
| Epic | game | proxy | 657 | 15 |
| Nintendo | game | proxy | 4622 | 126 |
| PlayStation | game | proxy | 325 | 4 |
| PayPal | payment | proxy | 8821 | 247 |
| OneDrive | service | proxy | 816 | 18 |
| iCloud | service | proxy | 2130 | 61 |
| Amazon | service | proxy | 6972 | 203 |

### Example registry snippet (review before commit)

```yaml
      - { path: rule/Clash/Claude/Claude.yaml, name: claude, local: Clash_Claude.yaml }
      - { path: rule/Clash/Gemini/Gemini.yaml, name: gemini, local: Clash_Gemini.yaml }
      - { path: rule/Clash/Copilot/Copilot.yaml, name: copilot, local: Clash_Copilot.yaml }
      - { path: rule/Clash/Spotify/Spotify.yaml, name: spotify, local: Clash_Spotify.yaml }
      - { path: rule/Clash/Twitch/Twitch.yaml, name: twitch, local: Clash_Twitch.yaml }
      - { path: rule/Clash/Whatsapp/Whatsapp.yaml, name: whatsapp, local: Clash_Whatsapp.yaml }
      - { path: rule/Clash/Reddit/Reddit.yaml, name: reddit, local: Clash_Reddit.yaml }
      - { path: rule/Clash/Cloudflare/Cloudflare.yaml, name: cloudflare, local: Clash_Cloudflare.yaml }
```

## Do NOT bulk-add

- **Advertising / EasyPrivacy / Hijacking** — overlap AdBlock stack (Hagezi/anti-AD)
- **Global / GlobalMedia / Proxy / ProxyLite / Direct** — composites, policy ambiguous
- **ChinaIPsBGP** etc. — IP dumps, handle under china/cidr carefully
- **Empty / 2-line stubs** — low value noise

## Process

```
This candidate list
  → human pick 5–10
  → registry.yaml rules:
  → Collect Upstream CI
  → conflicts / builder_validate / statistics
  → keep or revert
```
