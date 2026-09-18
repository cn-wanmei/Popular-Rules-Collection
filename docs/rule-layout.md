# rule/ layout (Primary Ecosystem)

Physical path is derived **only** from `primary_category` + display names.

```text
config/categories.yaml          # category definitions
config/service_primary.yaml     # service identity / primary category
rule/_index.yaml + rule/{Ecosystem}/{Service}/  # V1 Canonical Service Model
database/services/*.yaml        # Legacy Source; not a V3 runtime input
```

Examples:

| Service | Path |
|---------|------|
| wechat | `rule/Tencent/WeChat/` |
| alipay | `rule/Alibaba/Alipay/` |
| douyin | `rule/ByteDance/Douyin/` |
| icbc (future) | `rule/UnionPay/ICBC/` |
| xbox | `rule/Microsoft/Xbox/` |

Do not treat `database/services/` as a V3 runtime source. V1 model changes must pass the final migration gate.

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
