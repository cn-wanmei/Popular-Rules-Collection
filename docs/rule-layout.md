# rule/ layout (Primary Ecosystem)

Physical path is derived **only** from `primary_category` + display names.

```text
config/categories.yaml          # ecosystem id → display_name
config/service_primary.yaml     # service id → primary_category, display_name, tags
database/services/*.yaml        # data
        ↓
scripts/generate_rule_pages.py
        ↓
rule/{Ecosystem}/{Service}/
```

Examples:

| Service | Path |
|---------|------|
| wechat | `rule/Tencent/WeChat/` |
| alipay | `rule/Alibaba/Alipay/` |
| douyin | `rule/ByteDance/Douyin/` |
| icbc (future) | `rule/UnionPay/ICBC/` |
| xbox | `rule/Microsoft/Xbox/` |

Do not hand-edit `rule/`.

## Phase 8 source-of-truth boundary

The V1 Canonical Service Model is rooted at `rule/`. The historical `database/services/` tree is Legacy Source evidence and is not a V3 runtime input.

```text
config/categories.yaml
config/service_primary.yaml
        ↓
rule/_index.yaml + rule/{Ecosystem}/{Service}/
        ↓
V1 Canonical Service Model
        ↓
V3 Engine
```

Do not reintroduce `database/services/` as a V3 runtime dependency. Changes to the V1 model must pass the final migration gate.
